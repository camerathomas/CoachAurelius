"""
Gespreksvormen voor Aurelius.

Elke gespreksvorm bepaalt de rol van de gebruiker en de rol van de
filosofen. Verder blijft alles hetzelfde: pantheon-principe, wendingen,
eindgesprek.

Vrijspelen:
- Coach-sessie is altijd beschikbaar (level 1)
- De andere vormen worden per level vrijgespeeld
- Gold heeft alles vanaf het begin
"""


# ============================================================
# De gespreksvormen
# ============================================================

GESPREKSVORMEN = {
    "coach_sessie": {
        "naam": "Coach-sessie",
        "beschrijving": "Een gewoon gesprek met het pantheon.",
        "icoon": "🏛️",
        "level": 1,
        "filosofen": "pantheon",
        "gebruiker_rol": "deelnemer",
        "eerste_vraag": None,  # gebruikt de generieke opening
        "prompt_toevoeging": (
            "Dit is een coach-sessie. De gebruiker is het middelpunt. "
            "Reageer op wat de gebruiker zegt, ga dieper, onderzoek. "
            "Stel vragen die voortkomen uit wat de gebruiker inbrengt."
        ),
    },
    "tweegesprek": {
        "naam": "Tweegesprek",
        "beschrijving": "Jij en één filosoof. Diepgaand.",
        "icoon": "🤝",
        "level": 16,
        "filosofen": "één",
        "gebruiker_rol": "deelnemer",
        "eerste_vraag": (
            "Je hebt gekozen voor een tweegesprek. Jij en ik, één op één. "
            "Waar wil je het over hebben?"
        ),
        "prompt_toevoeging": (
            "Dit is een tweegesprek. Jij en de gebruiker, één op één. "
            "Er zijn geen andere filosofen. Ga diep, neem de tijd, "
            "onderzoek wat de gebruiker inbrengt grondig. "
            "Stel vragen die voortkomen uit wat de gebruiker zegt."
        ),
    },
    "grote_dialoog": {
        "naam": "Grote dialoog",
        "beschrijving": "De filosofen praten met elkaar. Jij kunt bijsturen.",
        "icoon": "🎭",
        "level": 17,
        "filosofen": "pantheon",
        "gebruiker_rol": "gastheer",
        "eerste_vraag": (
            "Welkom bij de grote dialoog. De filosofen zijn klaar om met "
            "elkaar in gesprek te gaan. Wat is het thema dat je vandaag "
            "wilt inbrengen?"
        ),
        "prompt_toevoeging": (
            "Dit is een grote dialoog. De filosofen praten met elkaar, "
            "reageren op elkaars standpunten, en dagen elkaar uit. "
            "De gebruiker is een gastheer die af en toe iets inbrengt. "
            "Reageer in eerste instantie op de vorige filosoof, niet op de "
            "gebruiker. Als de gebruiker iets zegt, reageer daar dan op, "
            "en ga daarna weer met de andere filosofen in gesprek."
        ),
    },
    "doorgaan_archief": {
        "naam": "Doorgaan met een gearchiveerd gesprek",
        "beschrijving": "Bouwt voort op een eerdere sessie.",
        "icoon": "🔄",
        "level": 19,
        "filosofen": "pantheon",
        "gebruiker_rol": "deelnemer",
        "eerste_vraag": None,  # de vervolgcontext bepaalt de opening
        "prompt_toevoeging": (
            "Dit is een vervolggesprek. De gebruiker bouwt voort op een "
            "eerdere sessie. Je hebt de context van die sessie gekregen. "
            "Verwijs waar zinvol naar wat er eerder gezegd is, en "
            "onderzoek wat er sindsdien veranderd is."
        ),
    },
    "strenge_coach": {
        "naam": "Strenge coach",
        "beschrijving": "Directe, confronterende vragen. Bereid je voor.",
        "icoon": "⚔️",
        "level": 20,
        "filosofen": "pantheon",
        "gebruiker_rol": "deelnemer",
        "eerste_vraag": "Wat ontwijk je?",
        "prompt_toevoeging": (
            "Dit is een strenge coach-sessie. De gebruiker wil tot het bot "
            "gaan. Jouw taak is om niet te troosten, niet te verzachten, en "
            "niet weg te kijken. Stel de vraag die de gebruiker het liefst "
            "niet hoort. Vraag door als het antwoord vaag is. Wijs op "
            "tegenstrijdigheden. Blijf respectvol, maar wees onverbiddelijk. "
            "Geen 'wat fijn dat je dit deelt'. Geen superlatieven. Geen "
            "troost. Alleen de vraag die ertoe doet."
        ),
    },
    "vragenvuur": {
        "naam": "Vragenvuur",
        "beschrijving": "Snel achter elkaar vragen. Je moet snel antwoorden.",
        "icoon": "🔥",
        "level": 21,
        "filosofen": "één",
        "gebruiker_rol": "deelnemer",
        "eerste_vraag": (
            "Ik ga je snel een paar vragen stellen. Denk niet te lang na. "
            "Eerste vraag: wat houdt je op dit moment het meest bezig?"
        ),
        "prompt_toevoeging": (
            "Dit is een vragenvuur. Je stelt de gebruiker meerdere vragen "
            "achter elkaar, snel, zonder ruimte om te lang na te denken. "
            "Elke beurt stel je twee tot drie korte vragen. De gebruiker "
            "antwoordt, en jij gaat direct door met nieuwe vragen. "
            "Je bent niet confronterend, maar wel vasthoudend. "
            "Aan het einde van het gesprek stel je één vraag die alles "
            "samenvat: 'Wat is het echte antwoord?'"
        ),
    },
    "socratisch_gesprek": {
        "naam": "Socratisch gesprek",
        "beschrijving": "Alleen vragen. Geen antwoorden. Jij moet zelf denken.",
        "icoon": "❓",
        "level": 22,
        "filosofen": "pantheon",
        "gebruiker_rol": "deelnemer",
        "eerste_vraag": (
            "Ik ga je alleen vragen stellen, geen antwoorden geven. "
            "Mijn eerste vraag: wat weet je zeker?"
        ),
        "prompt_toevoeging": (
            "Dit is een socratisch gesprek. Je stelt ALLEEN vragen. "
            "Je geeft geen antwoorden, geen advies, geen mening. "
            "Je stelt één vraag per beurt. Als de gebruiker iets beweert, "
            "vraag je door: 'Wat bedoel je precies?' of 'Hoe weet je dat?' "
            "of 'Is dat altijd zo?' Je doel is om de gebruiker zelf te "
            "laten nadenken, niet om hem iets te leren."
        ),
    },
    "de_biecht": {
        "naam": "De biecht",
        "beschrijving": "Je vertelt iets persoonlijks. De filosoof luistert zonder oordeel.",
        "icoon": "🕯️",
        "level": 23,
        "filosofen": "pantheon",
        "gebruiker_rol": "biechteling",
        "eerste_vraag": "Wat wil je opbiechten?",
        "prompt_toevoeging": (
            "Dit is een biecht. De gebruiker vertelt iets persoonlijks, "
            "iets waar hij zich misschien voor schaamt of dat hij moeilijk "
            "vindt om te delen. Jouw taak: luister zonder oordeel. "
            "Vraag door, maar wees zacht. Geef geen absoluties en geen "
            "advies. Help de gebruiker om het zelf onder ogen te zien. "
            "Aan het einde geef je een korte, milde overweging mee."
        ),
    },
    "het_dilemma": {
        "naam": "Het dilemma",
        "beschrijving": "Een moreel dilemma. Jij moet kiezen.",
        "icoon": "🔀",
        "level": 24,
        "filosofen": "pantheon",
        "gebruiker_rol": "deelnemer",
        "eerste_vraag": (
            "Ik leg je een dilemma voor. Je moet kiezen tussen twee kwaden. "
            "Ben je er klaar voor?"
        ),
        "prompt_toevoeging": (
            "Dit is een dilemma. Je presenteert de gebruiker een moreel "
            "dilemma: een keuze tussen twee kwaden, waarbij geen van beide "
            "opties goed is. De gebruiker moet kiezen. Jouw taak: vraag "
            "door naar de redenen, confronteer met de consequenties, en "
            "laat zien welke waarden in het spel zijn. Je geeft geen "
            "antwoord; je helpt de gebruiker zijn eigen keuze te begrijpen."
        ),
    },
    "de_droom": {
        "naam": "De droom",
        "beschrijving": "Je vertelt een droom. De filosoof interpreteert hem.",
        "icoon": "🌙",
        "level": 25,
        "filosofen": "pantheon",
        "gebruiker_rol": "dromer",
        "eerste_vraag": "Vertel me over je droom. Wat heb je gedroomd?",
        "prompt_toevoeging": (
            "Dit is een droomgesprek. De gebruiker vertelt een droom. "
            "Jouw taak: vraag naar de details, de beelden, de gevoelens. "
            "Interpreteer de droom voorzichtig, als een verhaal met "
            "symbolen. Verwijs naar mythen, filosofie of literatuur waar "
            "dat past. Je geeft geen psychologische diagnose; je opent "
            "mogelijke betekenissen. Aan het einde vraag je wat de droom "
            "voor de gebruiker zelf zou kunnen betekenen."
        ),
    },
}


# ============================================================
# Vrijspelen
# ============================================================

def beschikbare_vormen(profiel):
    """
    Geeft de gespreksvormen die de gebruiker mag kiezen.

    - Gold: alles
    - Sessie en basic: alleen coach-sessie tot level 15,
      daarna per level een nieuwe vorm
    """
    level = profiel.get("level", 1)
    tier = profiel.get("tier", "sessie")

    if tier == "gold":
        return list(GESPREKSVORMEN.keys())

    return [
        naam for naam, vorm in GESPREKSVORMEN.items()
        if vorm.get("level", 1) <= level
    ]


def is_beschikbaar(vorm_naam, profiel, heeft_eerdere_sessie=False):
    """
    Bepaalt of deze gespreksvorm beschikbaar is voor deze gebruiker.
    - Vervolggesprek: alleen als er een eerdere sessie is.
    - De andere: op basis van level.
    """
    if vorm_naam == "doorgaan_archief":
        return heeft_eerdere_sessie and vorm_naam in beschikbare_vormen(profiel)

    return vorm_naam in beschikbare_vormen(profiel)


# ============================================================
# Filosofen kiezen
# ============================================================

def kies_filosofen(vorm_naam, pantheon, voorzitter=None):
    """
    Bepaalt welke filosofen meedoen aan deze gespreksvorm.
    - 'pantheon': het hele pantheon
    - 'één': alleen de voorzitter (of de eerste filosoof)
    """
    vorm = GESPREKSVORMEN.get(vorm_naam)
    if not vorm:
        return pantheon

    if vorm["filosofen"] == "één":
        if voorzitter and voorzitter in pantheon:
            return [voorzitter]
        return pantheon[:1]

    return pantheon


# ============================================================
# Prompts
# ============================================================

def bouw_vorm_prompt(vorm_naam, context=None):
    """
    Bouwt de prompt-toevoeging voor deze gespreksvorm.
    Wordt aan de system prompt toegevoegd.
    """
    vorm = GESPREKSVORMEN.get(vorm_naam)
    if not vorm:
        return ""

    prompt = vorm["prompt_toevoeging"]

    if context:
        prompt += f"\n\n[CONTEXT VAN EERDERE SESSIE]\n{context}"

    return prompt


def bouw_vervolg_context(sessie):
    """
    Bouwt de context van een eerdere sessie voor een vervolggesprek.
    Geeft een string terug die aan de prompt wordt toegevoegd.
    """
    if not sessie:
        return ""

    onderdelen = []

    # Het thema
    if sessie.get("thema"):
        onderdelen.append(f"Onderwerp: {sessie['thema']}")

    # De incheck
    incheck = sessie.get("incheck", {})
    if incheck:
        onderdelen.append(f"Wat speelde er: {incheck.get('openheid', '—')}")
        onderdelen.append(f"Emotie: {incheck.get('emotie', '—')}")
        onderdelen.append(f"Intentie: {incheck.get('intentie', '—')}")

    # De afsluiter (samenvatting van de vorige sessie)
    afsluiter = sessie.get("afsluiter", {})
    if afsluiter:
        onderdelen.append(
            f"Afsluiting door {afsluiter.get('naam', '?')}: "
            f"{afsluiter.get('tekst', '')}"
        )

    return "\n".join(onderdelen)
