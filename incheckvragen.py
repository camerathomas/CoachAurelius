"""
Incheck-vragen voor Aurelius.

Per sessie worden 3 vragen gekozen:
- 1 tekstvraag
- 1 slider-vraag
- 1 keuzevraag

De vragen zijn verdeeld over 10 categorieën.
"""

import random


# ============================================================
# De vragen
# ============================================================

TEKST_VRAGEN = [
    {
        "sleutel": "openheid",
        "categorie": "openheid",
        "vraag": "Wat speelt er vandaag?",
        "placeholder": "Vertel vrijuit — er is geen goed of fout antwoord.",
    },
    {
        "sleutel": "emotie",
        "categorie": "emotie",
        "vraag": "Hoe gaat het met je?",
        "placeholder": "Bijvoorbeeld: druk, moe, rustig, onrustig...",
    },
    {
        "sleutel": "lichaam",
        "categorie": "lichaam",
        "vraag": "Hoe zit je in je lichaam op dit moment?",
        "placeholder": "Bijvoorbeeld: gespannen, rustig, moe...",
    },
    {
        "sleutel": "relaties",
        "categorie": "relaties",
        "vraag": "Met wie heb je op dit moment het meest te maken?",
        "placeholder": "Bijvoorbeeld: partner, collega, vriend, familie...",
    },
    {
        "sleutel": "werk",
        "categorie": "werk",
        "vraag": "Wat houdt je op dit moment het meest bezig?",
        "placeholder": "Bijvoorbeeld: werk, studie, een project...",
    },
    {
        "sleutel": "toekomst",
        "categorie": "toekomst",
        "vraag": "Waar hoop je naartoe te gaan?",
        "placeholder": "Bijvoorbeeld: een reis, een baan, een verandering...",
    },
    {
        "sleutel": "vragen",
        "categorie": "vragen",
        "vraag": "Wat wil je graag vragen of onderzoeken?",
        "placeholder": "Bijvoorbeeld: een dilemma, een keuze, een twijfel...",
    },
    {
        "sleutel": "verrassing",
        "categorie": "openheid",
        "vraag": "Wat verraste je de laatste tijd?",
        "placeholder": "Bijvoorbeeld: iets onverwachts, iets moois, iets moeilijks...",
    },
    {
        "sleutel": "dankbaarheid",
        "categorie": "emotie",
        "vraag": "Waar ben je op dit moment dankbaar voor?",
        "placeholder": "Bijvoorbeeld: een persoon, een moment, een klein ding...",
    },
    {
        "sleutel": "weerstand",
        "categorie": "intentie",
        "vraag": "Waar heb je weerstand tegen?",
        "placeholder": "Bijvoorbeeld: een gesprek, een taak, een beslissing...",
    },
]


SLIDER_VRAGEN = [
    {
        "sleutel": "overzicht",
        "categorie": "overzicht",
        "vraag": "Heb je op dit moment overzicht over je leven?",
        "min": 1,
        "max": 10,
        "default": 5,
        "toelichting": "1 = geen overzicht, 10 = volledig overzicht",
    },
    {
        "sleutel": "energie",
        "categorie": "lichaam",
        "vraag": "Hoeveel energie heb je op dit moment?",
        "min": 1,
        "max": 10,
        "default": 5,
        "toelichting": "1 = uitgeput, 10 = vol energie",
    },
    {
        "sleutel": "rust",
        "categorie": "emotie",
        "vraag": "Hoe rustig voel je je op dit moment?",
        "min": 1,
        "max": 10,
        "default": 5,
        "toelichting": "1 = onrustig, 10 = heel rustig",
    },
    {
        "sleutel": "verbinding",
        "categorie": "relaties",
        "vraag": "Hoe verbonden voel je je met de mensen om je heen?",
        "min": 1,
        "max": 10,
        "default": 5,
        "toelichting": "1 = geïsoleerd, 10 = heel verbonden",
    },
    {
        "sleutel": "richting",
        "categorie": "toekomst",
        "vraag": "Hoe duidelijk is je richting op dit moment?",
        "min": 1,
        "max": 10,
        "default": 5,
        "toelichting": "1 = geen richting, 10 = heel duidelijk",
    },
    {
        "sleutel": "druk",
        "categorie": "werk",
        "vraag": "Hoeveel druk ervaar je op dit moment?",
        "min": 1,
        "max": 10,
        "default": 5,
        "toelichting": "1 = geen druk, 10 = heel veel druk",
    },
    {
        "sleutel": "tevredenheid",
        "categorie": "emotie",
        "vraag": "Hoe tevreden ben je op dit moment met je leven?",
        "min": 1,
        "max": 10,
        "default": 5,
        "toelichting": "1 = ontevreden, 10 = heel tevreden",
    },
    {
        "sleutel": "moed",
        "categorie": "intentie",
        "vraag": "Hoeveel moed voel je om iets aan te pakken?",
        "min": 1,
        "max": 10,
        "default": 5,
        "toelichting": "1 = geen moed, 10 = veel moed",
    },
    {
        "sleutel": "helderheid",
        "categorie": "overzicht",
        "vraag": "Hoe helder is je denken op dit moment?",
        "min": 1,
        "max": 10,
        "default": 5,
        "toelichting": "1 = verward, 10 = heel helder",
    },
    {
        "sleutel": "veerkracht",
        "categorie": "lichaam",
        "vraag": "Hoe veerkrachtig voel je je op dit moment?",
        "min": 1,
        "max": 10,
        "default": 5,
        "toelichting": "1 = kwetsbaar, 10 = heel veerkrachtig",
    },
]


KEUZE_VRAGEN = [
    {
        "sleutel": "intentie",
        "categorie": "intentie",
        "vraag": "Wat wil je vandaag?",
        "opties": [
            "Even praten",
            "Iets bespreken",
            "Iets onderzoeken",
            "Iets vieren",
            "Tot rust komen",
        ],
    },
    {
        "sleutel": "modus",
        "categorie": "intentie",
        "vraag": "Hoe wil je dat het gesprek verloopt?",
        "opties": [
            "Rustig en onderzoekend",
            "Direct en confronterend",
            "Speels en verrassend",
            "Troostend en zacht",
            "Analytisch en scherp",
        ],
    },
    {
        "sleutel": "stemming",
        "categorie": "emotie",
        "vraag": "Wat past het beste bij je stemming?",
        "opties": [
            "Blij",
            "Rustig",
            "Onrustig",
            "Verdrietig",
            "Nieuwsgierig",
            "Boos",
        ],
    },
    {
        "sleutel": "thema",
        "categorie": "openheid",
        "vraag": "Welk thema wil je vandaag aanraken?",
        "opties": [
            "Werk en ambitie",
            "Relaties en verbinding",
            "Zingeving en richting",
            "Lichaam en gezondheid",
            "Geld en zekerheid",
            "Verlies en afscheid",
        ],
    },
    {
        "sleutel": "tijd",
        "categorie": "toekomst",
        "vraag": "Waar ligt je focus op dit moment?",
        "opties": [
            "Het verleden",
            "Het heden",
            "De nabije toekomst",
            "De verre toekomst",
            "Ik weet het niet",
        ],
    },
    {
        "sleutel": "houding",
        "categorie": "intentie",
        "vraag": "Hoe sta je tegenover het gesprek?",
        "opties": [
            "Open en nieuwsgierig",
            "Gesloten en voorzichtig",
            "Zoekend en twijfelend",
            "Vastberaden en helder",
            "Moe en afwachtend",
        ],
    },
    {
        "sleutel": "behoefte",
        "categorie": "emotie",
        "vraag": "Wat heb je op dit moment het meest nodig?",
        "opties": [
            "Rust",
            "Erkenning",
            "Inzicht",
            "Troost",
            "Uitdaging",
            "Verbinding",
        ],
    },
    {
        "sleutel": "relatie",
        "categorie": "relaties",
        "vraag": "Over wie wil je het hebben?",
        "opties": [
            "Mijzelf",
            "Mijn partner",
            "Mijn familie",
            "Mijn vrienden",
            "Mijn collega's",
            "Niemand in het bijzonder",
        ],
    },
    {
        "sleutel": "werk_rol",
        "categorie": "werk",
        "vraag": "Hoe sta je op dit moment in je werk of studie?",
        "opties": [
            "Ik zit er goed in",
            "Ik twijfel",
            "Ik voel me vastgelopen",
            "Ik wil iets anders",
            "Ik weet het nog niet",
        ],
    },
    {
        "sleutel": "lichaam_rol",
        "categorie": "lichaam",
        "vraag": "Hoe ga je om met je lichaam?",
        "opties": [
            "Ik luister ernaar",
            "Ik negeer het",
            "Ik forceer het",
            "Ik verzorg het",
            "Ik worstel ermee",
        ],
    },
]


# ============================================================
# De hulpfuncties
# ============================================================

def kies_random_vragen():
    """
    Kiest 3 random vragen: 1 tekst, 1 slider, 1 keuze.
    Geeft een lijst terug van 3 dicts.
    """
    return [
        random.choice(TEKST_VRAGEN),
        random.choice(SLIDER_VRAGEN),
        random.choice(KEUZE_VRAGEN),
    ]


def alle_vragen():
    """Geeft alle vragen terug, in één lijst."""
    return TEKST_VRAGEN + SLIDER_VRAGEN + KEUZE_VRAGEN


def aantal_vragen():
    """Geeft het totaal aantal vragen terug."""
    return len(TEKST_VRAGEN) + len(SLIDER_VRAGEN) + len(KEUZE_VRAGEN)
