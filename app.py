"""
Aurelius — een filosofische coach-app.
Start met: python -m streamlit run app.py

Deze versie werkt met een staat-machine.
Elke staat is een scherm.
Elke overgang is een functie.
"""

import streamlit as st
import time
from datetime import datetime


# ============================================================
# Configuratie
# ============================================================
st.set_page_config(
    page_title="Aurelius",
    page_icon="🏛️",
    layout="centered"
)


# ============================================================
# Database-check
# ============================================================
def check_database():
    try:
        secrets = st.secrets["connections"]["aurelius"]
    except KeyError:
        return False, (
            "**Database-configuratie niet gevonden.**\n\n"
            "Ga naar **Settings → Secrets** in Streamlit Cloud en zorg dat er staat:\n"
            "```toml\n[connections.aurelius]\nurl = \"libsql://...\"\n"
            "auth_token = \"...\"\n```\n\n"
            "**Belangrijk:** klik daarna op **Reboot**."
        )
    if "url" not in secrets:
        return False, "De sleutel `url` ontbreekt."
    if "auth_token" not in secrets:
        return False, "De sleutel `auth_token` ontbreekt."
    return True, None


db_ok, db_fout = check_database()
if not db_ok:
    st.error("⚠️ **Database niet beschikbaar**")
    st.markdown(db_fout)
    st.stop()

from opslag import (
    initialiseer, laad_profiel, bewaar_profiel,
    bewaar_bericht, laad_gesprek, wis_gesprek,
    bewaar_sessie, laad_sessies, laad_sessie,
)

try:
    initialiseer()
except Exception as e:
    st.error(f"⚠️ **Database-fout:** {e}")
    st.stop()

api_key = st.secrets["connections"]["aurelius"]["GEMINI_API_KEY"]


# ============================================================
# De staten
# ============================================================
STATEN = [
    "inloggen",
    "welkom",
    "geen_sessie",
    "parameters",
    "incheck",
    "gesprek",
    "afsluiting",
    "eindevaluatie",
    "archief",
    "betalen",
]

# ============================================================
# De sessie-state
# ============================================================
def initialiseer_state():
    """Zet alle session_state-variabelen op hun beginwaarde."""

    # De staat
    if "staat" not in st.session_state:
        st.session_state.staat = "inloggen"

    # Het profiel
    if "profiel" not in st.session_state:
        st.session_state.profiel = None

    # De gebruiker
    if "gebruiker_id" not in st.session_state:
        st.session_state.gebruiker_id = ""

    # De sessie-state
    if "geschiedenis" not in st.session_state:
        st.session_state.geschiedenis = []
    if "incheck" not in st.session_state:
        st.session_state.incheck = {}
    if "incheck_vragen" not in st.session_state:
        st.session_state.incheck_vragen = []
    if "incheck_stap" not in st.session_state:
        st.session_state.incheck_stap = 0
    if "pantheon" not in st.session_state:
        st.session_state.pantheon = []
    if "voorzitter" not in st.session_state:
        st.session_state.voorzitter = None
    if "gespreksvorm" not in st.session_state:
        st.session_state.gespreksvorm = "coach_sessie"
    if "sessie_duur" not in st.session_state:
        st.session_state.sessie_duur = 10
    if "sessie_start" not in st.session_state:
        st.session_state.sessie_start = 0
    if "sessie_tijd" not in st.session_state:
        st.session_state.sessie_tijd = 0
    if "is_proefsessie" not in st.session_state:
        st.session_state.is_proefsessie = False
    if "evaluatie" not in st.session_state:
        st.session_state.evaluatie = {}
    if "evaluatie_stap" not in st.session_state:
        st.session_state.evaluatie_stap = 0

    # UI-state
    if "toon_dashboard" not in st.session_state:
        st.session_state.toon_dashboard = False
    if "toon_privacy" not in st.session_state:
        st.session_state.toon_privacy = False
    if "toon_voorwaarden" not in st.session_state:
        st.session_state.toon_voorwaarden = False
    if "acceptatie_gedaan" not in st.session_state:
        st.session_state.acceptatie_gedaan = False

    # Model
    if "model_naam" not in st.session_state:
        st.session_state.model_naam = "gemini-3.1-flash-lite"
    if "provider_key" not in st.session_state:
        st.session_state.provider_key = "gemini"

    # Wendingen
    if "wendingen_geweest" not in st.session_state:
        st.session_state.wendingen_geweest = []

# ============================================================
# De overgangen
# ============================================================
def naar_inloggen():
    st.session_state.staat = "inloggen"


def naar_welkom():
    st.session_state.staat = "welkom"


def naar_geen_sessie():
    st.session_state.staat = "geen_sessie"


def naar_parameters():
    st.session_state.staat = "parameters"


def naar_incheck():
    st.session_state.staat = "incheck"


def naar_gesprek():
    st.session_state.staat = "gesprek"


def naar_afsluiting():
    st.session_state.staat = "afsluiting"


def naar_eindevaluatie():
    st.session_state.staat = "eindevaluatie"


def naar_archief():
    st.session_state.staat = "archief"


def naar_betalen():
    st.session_state.staat = "betalen"


def eindig_sessie():
    """Reset de sessie-state en ga terug naar geen_sessie."""
    st.session_state.geschiedenis = []
    st.session_state.incheck = {}
    st.session_state.incheck_vragen = []
    st.session_state.incheck_stap = 0
    st.session_state.pantheon = []
    st.session_state.voorzitter = None
    st.session_state.gespreksvorm = "coach_sessie"
    st.session_state.sessie_duur = 10
    st.session_state.sessie_start = 0
    st.session_state.sessie_tijd = 0
    st.session_state.is_proefsessie = False
    st.session_state.evaluatie = {}
    st.session_state.evaluatie_stap = 0
    st.session_state.wendingen_geweest = []
    naar_geen_sessie()


def herstel_staat():
    """
    Bepaalt de staat op basis van het profiel.
    Wordt aangeroepen na het inloggen.
    """
    profiel = st.session_state.profiel

    if not profiel:
        naar_inloggen()
        return

    # Als de sessie is afgerond: geen_sessie
    if profiel.get("sessie_afgerond", True):
        naar_geen_sessie()
        return

    # Als de sessie loopt: gesprek
    naar_gesprek()


# ============================================================
# De schermen
# ============================================================
def toon_inloggen():
    st.title("🏛️ Aurelius")
    st.caption("Een filosofische coach, geïnspireerd door Marcus Aurelius.")
    st.markdown("---")

    st.markdown("### 👋 Welkom")
    st.markdown(
        "Vul je naam in om te beginnen. "
        "Als je nieuw bent, kies dan een naam die je wilt gebruiken. "
        "Als je al eerder bent geweest, vul dan dezelfde naam in."
    )

    with st.form("inloggen_form"):
        naam = st.text_input("Jouw naam", value="")
        verzonden = st.form_submit_button("Verder", type="primary")

    if verzonden:
        if not naam.strip():
            st.warning("Vul een naam in.")
            return

        st.session_state.gebruiker_id = naam.strip()

        with st.spinner("Profiel laden..."):
            profiel = laad_profiel(naam.strip())

        if profiel.get("_is_fallback"):
            st.error(
                "⚠️ **Je profiel kon niet worden geladen.**\n\n"
                "Dit kan komen door een database-storing of een tijdelijk probleem. "
                "Probeer de pagina te verversen. Als het probleem blijft, "
                "probeer het dan later opnieuw."
            )
            st.stop()

        st.session_state.profiel = profiel

        # Nieuwe gebruiker? Toon het welkomstscherm.
        if not profiel.get("welkom_geweest", False):
            naar_welkom()
            st.rerun()
            return

        # Bestaande gebruiker: herstel de staat.
        herstel_staat()
        st.rerun()

def toon_welkom():
    st.title("🏛️ Welkom bij Aurelius")
    st.markdown("---")

    st.markdown("**Marcus Aurelius:**")
    st.markdown(
        "Ik ben Marcus Aurelius. Ik was keizer van Rome, en ik schreef "
        "elke dag aan mezelf — over wat ik wel en niet in de hand had, "
        "over wat ik kon veranderen en wat ik moest laten.\n\n"
        "Deze app is geen therapeut, geen adviseur, geen antwoordenmachine. "
        "Het is een plek om te denken. Met filosofen die je uitnodigen om "
        "zelf te kijken, zelf te vragen, zelf te kiezen.\n\n"
        "Elke sessie nodigen we een pantheon van filosofen uit. Ze komen "
        "uit verschillende tradities, en elk kijkt op een andere manier "
        "naar wat je meebrengt. Je hoeft ze niet te kennen. Je hoeft het "
        "niet eens te zijn. Je hoeft alleen maar te luisteren, en te "
        "antwoorden.\n\n"
        "Ik raad je aan om alle filosofen eens te proberen. Niet omdat ze "
        "allemaal gelijk hebben, maar omdat elke stem je iets laat zien "
        "dat je alleen niet zo snel zou zien.\n\n"
        "Begin rustig. Er is geen goed of fout gesprek. Er is alleen wat "
        "je opmerkt, en wat je ermee doet.\n\n"
        "Welkom."
    )

    st.markdown("---")

    if st.button("Verder", type="primary"):
        st.session_state.profiel["welkom_geweest"] = True
        bewaar_profiel(st.session_state.profiel)
        naar_geen_sessie()
        st.rerun()


def toon_geen_sessie():
    profiel = st.session_state.profiel
    level = profiel.get("level", 1)
    tier = profiel.get("tier", "sessie")

    st.title("🏛️ Aurelius")
    st.caption(f"Welkom terug, {st.session_state.gebruiker_id}.")
    st.markdown(f"### 🎯 Level {level}")
    st.caption(f"Tier: {tier}")

    st.markdown("---")

    # Check of de gebruiker nog mag
    if tier == "sessie":
        gesprekken_gehad = profiel.get("gesprekken_gehad", 0)
        sessies_gekocht = profiel.get("sessies_gekocht", 1)
        if gesprekken_gehad >= sessies_gekocht:
            _toon_sessie_op()
            return

    # Gewone knoppen
    if st.button("🚀 Nieuwe sessie", type="primary", use_container_width=True):
        naar_parameters()
        st.rerun()

    if tier == "sessie":
        if st.button("⭐ Abonnement nemen", use_container_width=True):
            naar_betalen()
            st.rerun()
    else:
        if st.button("👑 Upgrade naar Gold", use_container_width=True):
            naar_betalen()
            st.rerun()

    if st.button("📊 Dashboard", use_container_width=True):
        st.session_state.toon_dashboard = True
        st.rerun()


def _toon_sessie_op():
    """Toont het scherm als de sessie op is."""
    st.markdown("## 🕊️ Je sessie is gebruikt")
    st.markdown(
        "Je hebt je sessie al gebruikt. Om verder te gaan, kun je "
        "een nieuwe sessie kopen, of een abonnement nemen."
    )

    st.markdown("### Wat wil je doen?")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🛒 Nog een sessie kopen", use_container_width=True):
            naar_betalen()
            st.rerun()

    with col2:
        if st.button("⭐ Basic abonnement", use_container_width=True):
            naar_betalen()
            st.rerun()

    st.markdown("---")

    if st.button("📊 Dashboard", use_container_width=True):
        st.session_state.toon_dashboard = True
        st.rerun()


def toon_parameters():
    profiel = st.session_state.profiel
    tier = profiel.get("tier", "sessie")
    level = profiel.get("level", 1)

    st.title("🕐 Parameters voor een nieuw gesprek")
    st.caption("Kies hoe lang het gesprek mag duren, en met wie je wilt spreken.")

    st.markdown("---")

    # ============================================================
    # Duur
    # ============================================================
    st.markdown("### Duur")
    duur = st.radio(
        "Duur",
        ["Flitsgesprek (5 min)", "Kort gesprek (10 min)",
         "Standaard (20 min)", "Diep (30 min)"],
        label_visibility="collapsed",
        key="duur_keuze",
    )

    st.markdown("---")

    # ============================================================
    # Gespreksvorm
    # ============================================================
    st.markdown("### Gespreksvorm")

    from gespreksvormen import GESPREKSVORMEN, beschikbare_vormen

    vormen = beschikbare_vormen(profiel)

    if len(vormen) == 1:
        st.caption(f"_(alleen '{GESPREKSVORMEN[vormen[0]]['naam']}' beschikbaar op level {level})_")

    vorm_labels = {
        naam: f"{GESPREKSVORMEN[naam]['icoon']} {GESPREKSVORMEN[naam]['naam']}"
        for naam in vormen
    }

    vorm_keuze = st.radio(
        "Gespreksvorm",
        vormen,
        format_func=lambda x: vorm_labels.get(x, x),
        label_visibility="collapsed",
        key="vorm_keuze",
    )

    st.markdown("---")

    # ============================================================
    # Pantheon
    # ============================================================
    st.markdown("### Pantheon")

    from tiers import heeft_toegang, beschikbare_filosofen
    from filosofen import FILOSOFEN, PANTHEON_PER_LEVEL

    mag_eigen_pantheon = heeft_toegang(tier, level, "eigen_pantheon")

    if mag_eigen_pantheon:
        pantheon_keuze = st.radio(
            "Pantheon",
            ["standaard", "eigen"],
            format_func=lambda x: (
                "Standaard pantheon van dit level"
                if x == "standaard"
                else "Mijn eigen pantheon"
            ),
            label_visibility="collapsed",
            key="pantheon_keuze",
        )
    else:
        pantheon_keuze = "standaard"
        st.caption("_(eigen pantheon beschikbaar vanaf level 2)_")

    # Als de gebruiker een eigen pantheon wil
    if pantheon_keuze == "eigen":
        opties = beschikbare_filosofen(tier, level)

        if not opties:
            st.warning("Je hebt nog geen filosofen vrijgespeeld.")
        else:
            st.markdown("**Kies een voorzitter:**")
            voorzitter = st.selectbox(
                "Voorzitter",
                opties,
                format_func=lambda x: f"{FILOSOFEN[x]['emoji']} {FILOSOFEN[x]['naam']}" if x in FILOSOFEN else x,
                label_visibility="collapsed",
                key="voorzitter_keuze",
            )

            st.markdown("**Kies 4 filosofen:**")
            gekozen = []
            for i in range(4):
                keuze = st.selectbox(
                    f"Filosoof {i + 1}",
                    opties,
                    format_func=lambda x: f"{FILOSOFEN[x]['emoji']} {FILOSOFEN[x]['naam']}" if x in FILOSOFEN else x,
                    label_visibility="collapsed",
                    key=f"eigen_filosoof_{i}",
                )
                gekozen.append(keuze)

    st.markdown("---")

    # ============================================================
    # Knoppen
    # ============================================================
    col1, col2 = st.columns(2)

    with col1:
        if st.button("← Terug", use_container_width=True):
            naar_geen_sessie()
            st.rerun()

    with col2:
        if st.button("Start gesprek", type="primary", use_container_width=True):
            # Sla de duur op
            duur_map = {
                "Flitsgesprek (5 min)": 5,
                "Kort gesprek (10 min)": 10,
                "Standaard (20 min)": 20,
                "Diep (30 min)": 30,
            }
            st.session_state.sessie_duur = duur_map.get(duur, 10)

            # Sla de gespreksvorm op
            st.session_state.gespreksvorm = vorm_keuze

            # Sla het pantheon op
            if pantheon_keuze == "eigen":
                st.session_state.pantheon = [voorzitter] + gekozen
                st.session_state.voorzitter = voorzitter
            else:
                start_pantheon = PANTHEON_PER_LEVEL.get(level, PANTHEON_PER_LEVEL.get(1, []))
                st.session_state.pantheon = start_pantheon
                st.session_state.voorzitter = start_pantheon[0] if start_pantheon else None

            naar_incheck()
            st.rerun()

def toon_incheck():
    from incheck_vragen import kies_random_vragen

    # Kies eenmalig 3 vragen
    if not st.session_state.get("incheck_vragen"):
        st.session_state.incheck_vragen = kies_random_vragen()
        st.session_state.incheck_stap = 0

    vragen = st.session_state.incheck_vragen
    stap = st.session_state.incheck_stap
    totaal = len(vragen)

    st.title("👋 Welkom")
    st.caption("Even een paar vragen voordat we beginnen.")

    st.progress(
        stap / totaal,
        text=f"Vraag {stap + 1} van {totaal}" if stap < totaal else "Klaar",
    )

    # ============================================================
    # Vraag tonen
    # ============================================================
    if stap < totaal:
        vraag = vragen[stap]
        st.markdown(f"**{vraag['vraag']}**")

        if vraag["type"] == "tekst":
            antwoord = st.text_input(
                "Antwoord",
                placeholder=vraag.get("placeholder", ""),
                label_visibility="collapsed",
                key=f"incheck_{vraag['sleutel']}",
            )
            if st.button("Volgende ➡️", type="primary"):
                if antwoord.strip():
                    st.session_state.incheck[vraag["sleutel"]] = antwoord.strip()
                    st.session_state.incheck_stap += 1
                    st.rerun()
                else:
                    st.warning("Vul iets in.")

        elif vraag["type"] == "slider":
            if vraag.get("toelichting"):
                st.caption(vraag["toelichting"])
            antwoord = st.slider(
                "Score",
                vraag["min"],
                vraag["max"],
                vraag["default"],
                label_visibility="collapsed",
                key=f"incheck_{vraag['sleutel']}",
            )
            if st.button("Volgende ➡️", type="primary"):
                st.session_state.incheck[vraag["sleutel"]] = antwoord
                st.session_state.incheck_stap += 1
                st.rerun()

        elif vraag["type"] == "keuze":
            antwoord = st.radio(
                "Keuze",
                vraag["opties"],
                label_visibility="collapsed",
                key=f"incheck_{vraag['sleutel']}",
            )
            if st.button("Volgende ➡️", type="primary"):
                st.session_state.incheck[vraag["sleutel"]] = antwoord
                st.session_state.incheck_stap += 1
                st.rerun()

        st.markdown("---")

        if st.button("← Terug", key="incheck_terug"):
            if stap > 0:
                st.session_state.incheck_stap -= 1
                st.rerun()
            else:
                naar_parameters()
                st.rerun()

    # ============================================================
    # Klaar
    # ============================================================
    else:
        st.markdown("### ✅ Klaar")
        st.markdown("Je antwoorden:")
        for sleutel, waarde in st.session_state.incheck.items():
            st.markdown(f"- **{sleutel}**: {waarde}")

        st.markdown("---")

        if st.button("🚀 Start gesprek", type="primary"):
            naar_gesprek()
            st.rerun()


def toon_gesprek():
    from coach import bouw_coach_prompt, chat
    from filosofen import FILOSOFEN
    from wendingen import kies_random_wending, moet_wending_komen
    from datetime import datetime
    import time

    profiel = st.session_state.profiel
    sessie_duur = st.session_state.sessie_duur
    pantheon = st.session_state.pantheon
    voorzitter = st.session_state.voorzitter
    gespreksvorm = st.session_state.gespreksvorm

    if not pantheon:
        start_pantheon = profiel.get("eigen_pantheon", [])
        if not start_pantheon:
            from filosofen import PANTHEON_PER_LEVEL
            level = profiel.get("level", 1)
            start_pantheon = PANTHEON_PER_LEVEL.get(level, PANTHEON_PER_LEVEL.get(1, []))
        st.session_state.pantheon = start_pantheon
        pantheon = start_pantheon

    if not voorzitter:
        st.session_state.voorzitter = pantheon[0] if pantheon else "marcus_aurelius"
        voorzitter = st.session_state.voorzitter

    # Start de timer als die nog niet loopt
    if not st.session_state.sessie_start:
        st.session_state.sessie_start = time.time()
        st.session_state.sessie_tijd = 0

    # Update de sessietijd
    nu = time.time()
    laatste = profiel.get("laatste_bericht", nu)
    verschil = nu - laatste
    if verschil < 90:
        st.session_state.sessie_tijd += verschil
    else:
        st.session_state.sessie_tijd += 30
    profiel["laatste_bericht"] = nu

    minuten = st.session_state.sessie_tijd / 60
    percentage = minuten / sessie_duur if sessie_duur > 0 else 1

    # Bepaal de fase
    if percentage < 0.10:
        fase = "opening"
    elif percentage < 0.30:
        fase = "verkennen"
    elif percentage < 0.60:
        fase = "verdiepen"
    elif percentage < 0.80:
        fase = "verbreden"
    elif percentage < 0.92:
        fase = "integreren"
    else:
        fase = "afsluiten"

    # Toon de statusbalk
    st.title("🕐 Gesprek")
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        st.markdown(f"**🕐 {minuten:.1f}** van **{sessie_duur}** min")
    with col2:
        st.markdown(f"**📍 Fase:** {fase.capitalize()}")
    with col3:
        resterend = max(0, sessie_duur - minuten)
        st.markdown(f"⏳ **{resterend:.1f}** min")

    st.markdown("---")

    # Toon de geschiedenis
    gesprek_container = st.container()
    with gesprek_container:
        for b in st.session_state.geschiedenis:
            with st.chat_message(b["naam"], avatar=b.get("icoon", "🏛️")):
                st.markdown(f"**{b['naam']}**")
                st.markdown(b["tekst"])

    # Eerste beurt: de coach opent
    if not st.session_state.geschiedenis:
        filosoof_naam = voorzitter or "marcus_aurelius"
        filosoof = FILOSOFEN.get(filosoof_naam, FILOSOFEN["marcus_aurelius"])

        from coach import bouw_eerste_vraag_prompt

        eerste_vraag_prompt = bouw_eerste_vraag_prompt(st.session_state.incheck)

        system_prompt = bouw_coach_prompt(
            filosoof=filosoof,
            profiel=profiel,
            fase="opening",
            incheck=st.session_state.incheck,
        )

        with st.spinner(f"{filosoof['naam']} denkt na..."):
            antwoord = chat(
                model=st.session_state.get("model_naam", "gemini-3.1-flash-lite"),
                messages=[{"role": "user", "content": eerste_vraag_prompt}],
                system_prompt=system_prompt,
                provider=st.session_state.get("provider_key", "gemini"),
            )

        st.session_state.geschiedenis.append({
            "naam": filosoof["naam"],
            "tekst": antwoord,
            "icoon": filosoof["emoji"],
            "tijd": datetime.now().strftime("%H:%M"),
        })

        try:
            bewaar_bericht(st.session_state.gebruiker_id, filosoof["naam"], "assistant", antwoord)
        except Exception:
            pass

        st.rerun()

    # Invoer van de gebruiker
    gebruiker_input = st.chat_input("Waar wil je het over hebben?")

    if gebruiker_input:
        tijd = datetime.now().strftime("%H:%M")
        st.session_state.geschiedenis.append({
            "naam": "Jij",
            "tekst": gebruiker_input,
            "icoon": "🧑",
            "tijd": tijd,
        })
        try:
            bewaar_bericht(st.session_state.gebruiker_id, "Jij", "user", gebruiker_input)
        except Exception:
            pass

        # Kies een filosoof
        from coach import kies_filosoof

        if pantheon and voorzitter:
            filosoof_naam = kies_filosoof(profiel, pantheon, gebruiker_input)
        else:
            filosoof_naam = "marcus_aurelius"

        filosoof = FILOSOFEN.get(filosoof_naam, FILOSOFEN["marcus_aurelius"])

        # Wending?
        wending = None
        drempel = moet_wending_komen(
            minuten, sessie_duur,
            profiel.get("wendingen_geweest", []),
        )
        if drempel is not None:
            wending = kies_random_wending()
            profiel.setdefault("wendingen_geweest", []).append(drempel)

        # Bouw de prompt
        system_prompt = bouw_coach_prompt(
            filosoof=filosoof,
            profiel=profiel,
            fase=fase,
            incheck=st.session_state.incheck,
            wending=wending,
        )

        # Bouw de context
        context_msgs = st.session_state.geschiedenis[-12:]
        messages = []
        for b in context_msgs[:-1]:
            rol = "assistant" if b["naam"] != "Jij" else "user"
            messages.append({"role": rol, "content": b["tekst"]})
        messages.append({"role": "user", "content": gebruiker_input})

        with st.spinner(f"{filosoof['naam']} denkt na..."):
            antwoord = chat(
                model=st.session_state.get("model_naam", "gemini-3.5-flash-lite"),
                messages=messages,
                system_prompt=system_prompt,
                provider=st.session_state.get("provider_key", "gemini"),
            )

        st.session_state.geschiedenis.append({
            "naam": filosoof["naam"],
            "tekst": antwoord,
            "icoon": filosoof["emoji"],
            "tijd": datetime.now().strftime("%H:%M"),
        })
        try:
            bewaar_bericht(st.session_state.gebruiker_id, filosoof["naam"], "assistant", antwoord)
        except Exception:
            pass

        # Sla het profiel op
        try:
            bewaar_profiel(profiel)
        except Exception:
            pass

        st.rerun()

    # Check of de sessie voorbij is
    if minuten >= sessie_duur:
        st.markdown("---")
        st.markdown("### De tijd is om")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🕊️ Afronden", use_container_width=True, type="primary"):
                naar_afsluiting()
                st.rerun()


def toon_afsluiting():
    from coach import bouw_coach_prompt, chat
    from filosofen import FILOSOFEN
    from incheck_vragen import kies_inzicht_vragen
    from datetime import datetime

    profiel = st.session_state.profiel
    pantheon = st.session_state.pantheon
    voorzitter = st.session_state.voorzitter

    st.title("🕊️ Afsluiting")
    st.markdown("---")

    # ============================================================
    # Stap 1: de filosoof rondt af
    # ============================================================
    if not st.session_state.get("afsluiting_gedaan"):
        filosoof_naam = voorzitter or "marcus_aurelius"
        filosoof = FILOSOFEN.get(filosoof_naam, FILOSOFEN["marcus_aurelius"])

        afsluit_prompt = (
            "Het gesprek is voorbij. Rond het af met een korte, "
            "concluderende gedachte. Geen afscheid, maar een laatste "
            "overweging. Maximaal 3 zinnen."
        )

        system_prompt = bouw_coach_prompt(
            filosoof=filosoof,
            profiel=profiel,
            fase="afsluiten",
            incheck=st.session_state.incheck,
        )

        with st.spinner(f"{filosoof['naam']} rondt af..."):
            antwoord = chat(
                model=st.session_state.get("model_naam", "gemini-3.1-flash-lite"),
                messages=[{"role": "user", "content": afsluit_prompt}],
                system_prompt=system_prompt,
                provider=st.session_state.get("provider_key", "gemini"),
            )

        st.session_state.geschiedenis.append({
            "naam": filosoof["naam"],
            "tekst": antwoord,
            "icoon": filosoof["emoji"],
            "tijd": datetime.now().strftime("%H:%M"),
        })

        try:
            bewaar_bericht(st.session_state.gebruiker_id, filosoof["naam"], "assistant", antwoord)
        except Exception:
            pass

        st.session_state.afsluiting_gedaan = True
        st.rerun()

    # ============================================================
    # Toon de afsluiting
    # ============================================================
    for b in st.session_state.geschiedenis[-3:]:
        if b["naam"] != "Jij":
            with st.chat_message(b["naam"], avatar=b.get("icoon", "🏛️")):
                st.markdown(b["tekst"])

    st.markdown("---")

    # ============================================================
    # Stap 2: de inzichtvragen
    # ============================================================
    if not st.session_state.get("inzicht_vragen"):
        st.session_state.inzicht_vragen = kies_inzicht_vragen()
        st.session_state.inzicht_stap = 0

    vragen = st.session_state.inzicht_vragen
    stap = st.session_state.inzicht_stap
    totaal = len(vragen)

    st.markdown("### 💡 Inzicht")
    st.caption("Even stilstaan. Wat neem je mee?")

    st.progress(
        stap / totaal,
        text=f"Vraag {stap + 1} van {totaal}" if stap < totaal else "Klaar",
    )

    if stap < totaal:
        vraag = vragen[stap]
        st.markdown(f"**{vraag['vraag']}**")

        antwoord = st.text_area(
            "Antwoord",
            placeholder=vraag.get("placeholder", ""),
            label_visibility="collapsed",
            key=f"inzicht_{vraag['sleutel']}",
        )

        if st.button("Volgende ➡️", type="primary"):
            if antwoord.strip():
                st.session_state.setdefault("inzicht", {})[vraag["sleutel"]] = antwoord.strip()
                st.session_state.inzicht_stap += 1
                st.rerun()
            else:
                st.warning("Vul iets in.")

    else:
        st.markdown("### ✅ Klaar")
        st.markdown("Je inzichten zijn opgeslagen.")
        st.markdown("---")

        if st.button("Naar het eindgesprek", type="primary"):
            naar_eindevaluatie()
            st.rerun()


def toon_eindevaluatie():
    from evaluatie import (
        haal_reacties_op,
        bouw_context,
        bepaal_meest_gesproken,
        verzamel_alle_reacties,
        bereken_leestijd,
        EVALUATIE_RONDE_1,
        EVALUATIE_RONDE_2,
        EVALUATIE_AFSLUITER,
    )
    from filosofen import FILOSOFEN
    import time

    profiel = st.session_state.profiel
    geschiedenis = st.session_state.geschiedenis
    pantheon = st.session_state.pantheon
    voorzitter = st.session_state.voorzitter

    st.title("🕊️ Eindgesprek")
    st.caption("De filosofen kijken terug op wat er is gezegd.")

    st.markdown("---")

    # ============================================================
    # Stap 1: de rondes ophalen
    # ============================================================
    if not st.session_state.get("evaluatie_rondes"):
        with st.spinner("De filosofen denken na..."):
            try:
                context = bouw_context(profiel, geschiedenis, pantheon)

                # Voeg de voorzitter toe aan de context
                if voorzitter and voorzitter in FILOSOFEN:
                    context += (
                        f"\n\n--- VOORZITTER ---\n"
                        f"De voorzitter van deze sessie is "
                        f"{FILOSOFEN[voorzitter]['naam']}. "
                        f"Laat de voorzitter NIET meedoen in ronde 1 en ronde 2. "
                        f"De voorzitter komt alleen terug in de afsluiter."
                    )

                # Ronde 1
                data1 = haal_reacties_op(
                    st.session_state.get("model_naam", "gemini-2.5-flash-lite"),
                    st.session_state.get("provider_key", "gemini"),
                    EVALUATIE_RONDE_1,
                    context,
                )
                rondes = {"ronde_1": (data1 or {}).get("reacties", [])}

                # Ronde 2
                context2 = context + "\n\n--- RONDE 1 ---\n"
                for r in rondes["ronde_1"]:
                    context2 += f"{r['naam']}: {r['tekst']}\n\n"

                data2 = haal_reacties_op(
                    st.session_state.get("model_naam", "gemini-2.5-flash-lite"),
                    st.session_state.get("provider_key", "gemini"),
                    EVALUATIE_RONDE_2,
                    context2,
                )
                rondes["ronde_2"] = (data2 or {}).get("reacties", [])

                st.session_state.evaluatie_rondes = rondes

            except Exception as e:
                st.error(f"Fout bij het ophalen van de evaluatie: {e}")

    # ============================================================
    # Stap 2: de afsluiter ophalen
    # ============================================================
    if (st.session_state.get("evaluatie_rondes") is not None
            and not st.session_state.get("evaluatie_afsluiter")):

        with st.spinner("De afsluiting wordt voorbereid..."):
            try:
                # Bepaal wie de afsluiter doet
                if voorzitter and voorzitter in FILOSOFEN:
                    meest = FILOSOFEN[voorzitter]["naam"]
                else:
                    meest = bepaal_meest_gesproken(geschiedenis) or "Socrates"

                context_afsluiter = bouw_context(profiel, geschiedenis, pantheon)
                context_afsluiter += f"\n\n--- AFSLUITING DOOR ---\n{meest}\n\n"

                for ronde_naam, reacties in st.session_state.evaluatie_rondes.items():
                    context_afsluiter += f"\n--- {ronde_naam.upper()} ---\n"
                    for r in reacties:
                        context_afsluiter += f"{r['naam']}: {r['tekst']}\n\n"

                data_afsluiter = haal_reacties_op(
                    st.session_state.get("model_naam", "gemini-2.5-flash-lite"),
                    st.session_state.get("provider_key", "gemini"),
                    EVALUATIE_AFSLUITER,
                    context_afsluiter,
                )
                st.session_state.evaluatie_afsluiter = (
                    data_afsluiter or {}
                ).get("afsluiter")

            except Exception as e:
                st.error(f"Fout bij de afsluiter: {e}")

    # ============================================================
    # Stap 3: de reacties tonen
    # ============================================================
    if st.session_state.get("evaluatie_rondes") is not None:
        alle_reacties = verzamel_alle_reacties(
            st.session_state.evaluatie_rondes,
            st.session_state.get("evaluatie_afsluiter"),
        )

        stap = st.session_state.get("evaluatie_stap", 0)

        for i, (ronde_label, r) in enumerate(alle_reacties):
            if i > stap:
                break
            with st.chat_message(r.get("naam", "?"), avatar=r.get("emoji", "🏛️")):
                st.markdown(f"**{r.get('naam', '?')}** · _{ronde_label}_")
                st.markdown(r.get("tekst", ""))

        if stap < len(alle_reacties) - 1:
            volgende = alle_reacties[stap + 1][1]
            wachttijd = bereken_leestijd(volgende.get("tekst", ""))
            time.sleep(wachttijd)
            st.session_state.evaluatie_stap = stap + 1
            st.rerun()

        else:
            st.session_state.evaluatie_afgerond = True

    # ============================================================
    # Stap 4: naar het archief
    # ============================================================
    if st.session_state.get("evaluatie_afgerond"):
        st.markdown("---")
        if st.button("Naar het archief", type="primary"):
            naar_archief()
            st.rerun()


def toon_archief():
    st.title("🏛️ De sessie is afgerond")
    st.markdown("Wil je deze sessie bewaren in je archief?")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📁 Ja, archiveer", type="primary", use_container_width=True):
            eindig_sessie()
            st.rerun()

    with col2:
        if st.button("Nee, bewaar niet", use_container_width=True):
            eindig_sessie()
            st.rerun()


def toon_betalen():
    st.title("💳 Betaling")
    st.caption("_(nog niet beschikbaar in deze versie)_")

    st.markdown("---")

    if st.button("← Terug"):
        naar_geen_sessie()
        st.rerun()

# ============================================================
# De router
# ============================================================
def toon_juiste_scherm():
    staat = st.session_state.staat

    if staat == "inloggen":
        toon_inloggen()
    elif staat == "welkom":
        toon_welkom()
    elif staat == "geen_sessie":
        toon_geen_sessie()
    elif staat == "parameters":
        toon_parameters()
    elif staat == "incheck":
        toon_incheck()
    elif staat == "gesprek":
        toon_gesprek()
    elif staat == "afsluiting":
        toon_afsluiting()
    elif staat == "eindevaluatie":
        toon_eindevaluatie()
    elif staat == "archief":
        toon_archief()
    elif staat == "betalen":
        toon_betalen()
    else:
        st.error(f"Onbekende staat: {staat}")
        naar_inloggen()
        st.rerun()

# ============================================================
# De sidebar
# ============================================================
def toon_sidebar():
    st.sidebar.title("🏛️ Aurelius")
    st.sidebar.caption("Jouw filosofische metgezel")

    st.sidebar.markdown("---")

    if st.sidebar.button("📊 Dashboard"):
        st.session_state.toon_dashboard = True
        st.rerun()

    if st.sidebar.button("📜 Privacyverklaring"):
        st.session_state.toon_privacy = True
        st.rerun()

    if st.sidebar.button("📋 Algemene voorwaarden"):
        st.session_state.toon_voorwaarden = True
        st.rerun()

    st.sidebar.markdown("---")

    if st.sidebar.button("🗑️ Wis alle gesprekken"):
        try:
            wis_gesprek(st.session_state.gebruiker_id)
            st.session_state.geschiedenis = []
            st.sidebar.success("Gewist.")
            st.rerun()
        except Exception as e:
            st.sidebar.error(f"Fout: {e}")


# ============================================================
# De hoofdroute
# ============================================================
def main():
    initialiseer_state()

    # Sidebar (alleen als er een gebruiker is)
    if st.session_state.profiel:
        toon_sidebar()

    # Dashboard (als dat getoond moet worden)
    if st.session_state.get("toon_dashboard", False):
        if st.button("← Terug naar de app"):
            st.session_state.toon_dashboard = False
            st.rerun()

        from dashboard import toon_dashboard
        toon_dashboard(st.session_state.gebruiker_id, st.session_state.profiel)
        return

    # Privacy
    if st.session_state.get("toon_privacy", False):
        if st.button("← Terug naar de app"):
            st.session_state.toon_privacy = False
            st.rerun()

        from privacy import toon_privacy
        toon_privacy()
        return

    # Voorwaarden
    if st.session_state.get("toon_voorwaarden", False):
        if st.button("← Terug naar de app"):
            st.session_state.toon_voorwaarden = False
            st.rerun()

        from voorwaarden import toon_voorwaarden
        toon_voorwaarden()
        return

    # Het juiste scherm
    toon_juiste_scherm()


if __name__ == "__main__":
    main()
