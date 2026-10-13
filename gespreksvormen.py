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
        "level": 2,
        "filosofen": "één",
        "gebruiker_rol": "deelnemer",
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
        "level": 3,
        "filosofen": "pantheon",
        "gebruiker_rol": "gastheer",
        "prompt_toevoeging": (
            "Dit is een grote dialoog. De filosofen praten met elkaar, "
            "reageren op elkaars standpunten, en dagen elkaar uit. "
            "De gebruiker is een gastheer die af en toe iets inbrengt. "
            "Reageer in eerste instantie op de vorige filosoof, niet op de "
            "gebruiker. Als de gebruiker iets zegt, reageer daar dan op, "
            "en ga daarna weer met de andere filosofen in gesprek."
        ),
    },
    "groot_pantheon": {
        "naam": "Groot Pantheon",
        "beschrijving": "Alle filosofen. Wie het beste past, krijgt de beurt.",
        "icoon": "🌌",
        "level": 4,
        "filosofen": "alles",
        "gebruiker_rol": "deelnemer",
        "prompt_toevoeging": (
            "Dit is het Groot Pantheon. Alle filosofen doen mee. "
            "Reageer alleen als je iets hebt toe te voegen dat werkelijk "
            "nieuw is. Als een andere filosoof beter past bij wat de "
            "gebruiker zegt, laat hem dan het woord nemen. "
            "Je hoeft niet te reageren als je niets toe te voegen hebt."
        ),
    },
    "doorgaan_archief": {
        "naam": "Doorgaan met een gearchiveerd gesprek",
        "beschrijving": "Bouwt voort op een eerdere sessie.",
        "icoon": "🔄",
        "level": 5,
        "filosofen": "pantheon",
        "gebruiker_rol": "deelnemer",
        "prompt_toevoeging": (
            "Dit is een vervolggesprek. De gebruiker bouwt voort op een "
            "eerdere sessie. Je hebt de context van die sessie gekregen. "
            "Verwijs waar zinvol naar wat er eerder gezegd is, en "
            "onderzoek wat er sindsdien veranderd is."
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
    - Sessie en basic: alleen de vormen van de levels die zijn behaald
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
    - 'alles': alle filosofen uit alle pantheons
    """
    vorm = GESPREKSVORMEN.get(vorm_naam)
    if not vorm:
        return pantheon

    if vorm["filosofen"] == "alles":
        from filosofen import FILOSOFEN
        return list(FILOSOFEN.keys())

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
