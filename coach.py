"""
De coach-logica: prompts bouwen, filosofen kiezen, en modellen aanroepen.
Ondersteunt Ollama (lokaal) en Gemini (online).
"""

import os
import time
import requests

# ============================================================
# Configuratie
# ============================================================
OLLAMA_URL = "http://localhost:11434/api/chat"


def _laad_gemini_key():
    """Laadt de Gemini API-sleutel uit Streamlit secrets of omgeving.

    Zoekt op drie plekken:
    1. Onder [connections.aurelius] (nieuwe locatie)
    2. Op de root van secrets (oude locatie)
    3. In omgevingsvariabelen
    """
    try:
        import streamlit as st

        try:
            return st.secrets["connections"]["aurelius"]["GEMINI_API_KEY"]
        except (KeyError, Exception):
            pass

        try:
            return st.secrets["GEMINI_API_KEY"]
        except (KeyError, Exception):
            pass
    except Exception:
        pass

    return os.environ.get("GEMINI_API_KEY", "")


# ============================================================
# Ollama
# ============================================================
def chat_ollama(model, messages, system_prompt=None, temperature=0.8, timeout=240):
    """Stuurt een chatverzoek naar Ollama."""
    msgs = []
    if system_prompt:
        msgs.append({"role": "system", "content": system_prompt})
    msgs.extend(messages)

    payload = {
        "model": model,
        "messages": msgs,
        "stream": False,
        "options": {"temperature": temperature},
        "think": False,
    }

    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=timeout)
        r.raise_for_status()
        return r.json()["message"]["content"]
    except requests.exceptions.ReadTimeout:
        return "⚠️ Het model deed er te lang over. Probeer het opnieuw."
    except requests.exceptions.ConnectionError:
        return "⚠️ Geen verbinding met Ollama. Draait `ollama serve`?"
    except Exception as e:
        return f"⚠️ Fout: {e}"


# ============================================================
# Gemini
# ============================================================
def chat_gemini(model, messages, system_prompt=None, temperature=0.8, retries=4):
    """
    Stuurt een chatverzoek naar Gemini, met retry bij 500 en 503.
    Wacht steeds langer tussen de pogingen.
    """
    api_key = _laad_gemini_key()
    if not api_key:
        return "⚠️ Geen Gemini API-sleutel gevonden."

    laatste_fout = None

    for poging in range(retries):
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=api_key)

            contents = []
            for m in messages:
                rol = "user" if m["role"] == "user" else "model"
                contents.append(
                    types.Content(role=rol, parts=[types.Part(text=m["content"])])
                )

            config = types.GenerateContentConfig(
                temperature=temperature,
                system_instruction=system_prompt,
            )

            response = client.models.generate_content(
                model=model,
                contents=contents,
                config=config,
            )

            return response.text

        except Exception as e:
            laatste_fout = e
            fout = str(e)

            # 500, 503 en interne fouten: opnieuw proberen
            if ("500" in fout or "503" in fout or "INTERNAL" in fout
                    or "overloaded" in fout.lower()):
                if poging < retries - 1:
                    # Exponentiële wachttijd: 2, 4, 8 seconden
                    time.sleep(2 ** (poging + 1))
                    continue

            # Andere fouten: meteen terugkeren
            return f"⚠️ Gemini fout: {e}"

    # Alle pogingen mislukt
    return f"⚠️ Gemini fout: {laatste_fout}"


# ============================================================
# Algemene chat-functie
# ============================================================
def chat(model, messages, system_prompt=None, temperature=0.8, provider="ollama"):
    """Kiest tussen Ollama en Gemini op basis van de provider."""
    if provider == "gemini":
        return chat_gemini(model, messages, system_prompt, temperature)
    return chat_ollama(model, messages, system_prompt, temperature)


# ============================================================
# Filosoof kiezen
# ============================================================
def kies_filosoof(profiel, pantheon, gebruikers_input):
    """Kiest een filosoof op basis van het profiel en de input."""
    from filosofen import FILOSOFEN

    invoer = gebruikers_input.lower()

    for naam in pantheon:
        filosoof = FILOSOFEN[naam]
        for thema in filosoof.get("themas", []):
            if thema in invoer:
                return naam

    return pantheon[0] if pantheon else "aurelius"


def kies_filosoof_met_verdeling(profiel, pantheon, gebruikers_input, voorzitter, teller):
    """
    Kiest een filosoof voor een gewone beurt.
    De voorzitter doet alleen de inleiding, de wendingen en de afsluiting.
    De andere filosofen reageren op basis van thema-match.
    """
    if not pantheon:
        return "marcus_aurelius"

    # De voorzitter doet niet mee aan gewone beurten.
    deelnemers = [f for f in pantheon if f != voorzitter]

    if not deelnemers:
        return voorzitter or "marcus_aurelius"

    invoer = gebruikers_input.lower()

    # 1. Zoek een filosoof wiens thema past bij wat de gebruiker zegt.
    from filosofen import FILOSOFEN
    for naam in deelnemers:
        filosoof = FILOSOFEN.get(naam)
        if not filosoof:
            continue
        for thema in filosoof.get("themas", []):
            if thema in invoer:
                teller[naam] = teller.get(naam, 0) + 1
                return naam

    # 2. Anders: de filosoof die het minst gesproken heeft.
    minst = min(deelnemers, key=lambda f: teller.get(f, 0))
    teller[minst] = teller.get(minst, 0) + 1
    return minst


def bouw_coach_prompt(filosoof, profiel, fase=None, incheck=None, wending=None, is_voorzitter=False, stijl=3):
    """Bouwt de system prompt voor de coach."""
    naam = filosoof.get("naam", "de filosoof")
    stem = filosoof.get("prompt", f"Je bent {naam}.")
    stroming = filosoof.get("stroming", "")
    filosoof_stijl = filosoof.get("stijl", [])
    themas = filosoof.get("themas", [])

    # --- Stem ---
    stem_blok = f"[DE STEM DIE JE NU SPREEKT]\n{stem}"

    # --- Stroming ---
    stroming_blok = ""
    if stroming:
        stroming_blok = (
            f"[STROMING]\n"
            f"Je komt uit de traditie van: {stroming}.\n"
            f"Maar je bent {naam}, geen andere filosoof uit die traditie."
        )

    # --- Stijl ---
    stijl_blok = ""
    if filosoof_stijl:
        regels = "\n".join(f"- {w.capitalize()}: {u}" for w, u in filosoof_stijl)
        stijl_blok = (
            f"[STIJL — DIT IS BELANGRIJK]\n"
            f"{regels}\n\n"
            f"Als je deze stijl niet volgt, dan ben je niet {naam}."
        )

    # --- Inhoud ---
    inhoud_blok = ""
    if themas:
        inhoud_blok = f"[INHOUD]\nJe spreekt graag over: {', '.join(themas)}."

    # --- Basis ---
    basis_blok = (
        "[BASIS]\n"
        "Je bent een filosofische gesprekspartner. Je luistert meer dan je spreekt. "
        "Je oordeelt niet. Je geeft geen advies. Je vleit niet. "
        "Geen 'wat een fascinerende visie'. Geen superlatieven."
    )

    # --- Lengte ---
    if is_voorzitter:
        limiet = 100
        rol_uitleg = (
            "Je bent de voorzitter van dit gesprek. Je mag iets meer zeggen "
            "omdat je het gesprek leidt, maar nog steeds bondig."
        )
    else:
        limiet = 60
        rol_uitleg = (
            "Je bent één van de filosofen in het pantheon. Je brengt één "
            "gedachte, één vraag, één observatie."
        )

    lengte_blok = (
        f"[LENGTE — STRIKT]\n"
        f"{rol_uitleg}\n\n"
        f"Antwoord in maximaal {limiet} woorden. Niet {limiet + 1}. "
        f"Niet {limiet + 10}. Maximaal {limiet}.\n"
        f"Eén gedachte per beurt. Geen opsommingen. Geen kopjes. "
        f"Geen herhaling van wat de gebruiker al zei. "
        f"Korter is beter dan langer."
    )

    # --- Coach-stijl ---
    if stijl == 1:
        coach_stijl_blok = (
            "[COACH-STIJL — ZACHT]\n"
            "Je bent een zachte coach. Je troost. Je legt uit. "
            "Je geeft ruimte. Je stelt makkelijke vragen. "
            "Je duwt niet. Je laat de gebruiker ademen."
        )
    elif stijl == 2:
        coach_stijl_blok = (
            "[COACH-STIJL — COACH]\n"
            "Je bent een coach. Je helpt. Je vertaalt. "
            "Je stelt vragen. Je duwt een beetje. "
            "Maar je blijft vriendelijk."
        )
    elif stijl == 4:
        coach_stijl_blok = (
            "[COACH-STIJL — FILOSOOF]\n"
            "Je bent een filosoof. Je duwt. Je vraagt door. "
            "Je confronteert voorzichtig. "
            "Je laat de gebruiker niet wegkomen met een vaag antwoord."
        )
    elif stijl == 5:
        coach_stijl_blok = (
            "[COACH-STIJL — HARD]\n"
            "Je bent een harde filosoof. Je confronteert. Je schuurt. "
            "Je laat niet los. Je daagt uit. "
            "Je bent respectvol, maar onverbiddelijk."
        )
    else:
        coach_stijl_blok = ""

    # --- Incheck ---
    incheck_blok = ""
    if incheck:
        regels = "\n".join(f"- {k}: {v}" for k, v in incheck.items())
        incheck_blok = (
            f"[INCHECK]\n"
            f"De gebruiker heeft het volgende ingevuld:\n{regels}\n\n"
            f"Verwijs hier af en toe naar. Niet elke beurt. Maar wel een paar keer."
        )

    # --- Fase ---
    fase_blok = ""
    if fase:
        fase_blok = f"[FASE]\nJe zit nu in de fase: {fase}."

    # --- Wending ---
    wending_blok = ""
    if wending:
        wending_blok = (
            f"\n\n[WENDING: {wending['naam'].upper()}]\n"
            f"{wending['instructie']}\n\n"
            f"Negeer je standaard coach-instructies voor deze ene beurt. "
            f"Doe alleen wat hierboven staat."
        )

    # --- Alles samenvoegen ---
    blokken = [
        stem_blok,
        stroming_blok,
        stijl_blok,
        inhoud_blok,
        basis_blok,
        lengte_blok,
        coach_stijl_blok,
        incheck_blok,
        fase_blok,
    ]
    tekst = "\n\n".join(b for b in blokken if b)
    tekst += wending_blok

    return tekst


def bouw_eerste_vraag_prompt(incheck, filosoof=None):
    """Bouwt de prompt voor de eerste vraag."""
    regels = "\n".join(f"- {k}: {v}" for k, v in incheck.items())

    naam = filosoof.get("naam", "de filosoof") if filosoof else "de filosof"

    return (
        f"De gebruiker heeft net de incheck ingevuld:\n{regels}\n\n"
        f"Jouw taak: open het gesprek als {naam}. "
        f"Gebruik de incheck als achtergrond, niet als script. "
        f"Herhaal de incheck niet. Vat hem niet samen. "
        f"Open met een uitnodiging, niet met een vraag die de incheck "
        f"herhaalt. Zeg bijvoorbeeld: 'Wil je het hebben over [iets uit "
        f"de incheck], of heb je iets anders dat je aandacht vraagt?' "
        f"Of: 'Is er iets dat je bezighoudt?' "
        f"Open in jouw eigen stijl: als je Socrates bent, open je met "
        f"een vraag over een woord. Als je Nietzsche bent, open je met "
        f"een uitdaging. Als je de Boeddha bent, open je met een beeld. "
        f"Kort, direct, uitnodigend. Maximaal 60 woorden. "
        f"Geen opsomming, geen herhaling, geen samenvatting."
    )
