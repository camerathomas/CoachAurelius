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
        st.session_state.gespreksvorm = "themagesprek"
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
    st.session_state.gespreksvorm = "themagesprek"
    st.session_state.sessie_duur = 10
    st.session_state.sessie_start = 0
    st.session_state.sessie_tijd = 0
    st.session_state.is_proefsessie = False
    st.session_state.evaluatie = {}
    st.session_state.evaluatie_stap = 0
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

    st.title("🏛️ Aurelius")
    st.caption(f"Welkom terug, {st.session_state.gebruiker_id}.")
    st.markdown(f"### 🎯 Level {level}")

    st.markdown("---")

    if st.button("🚀 Nieuwe sessie", type="primary", use_container_width=True):
        naar_parameters()
        st.rerun()

    if st.button("📊 Dashboard", use_container_width=True):
        st.session_state.toon_dashboard = True
        st.rerun()


def toon_parameters():
    st.title("🕐 Parameters voor een nieuw gesprek")
    st.caption("Kies hoe lang het gesprek mag duren, en met wie je wilt spreken.")

    st.markdown("---")

    st.markdown("### Duur")
    duur = st.radio(
        "Duur",
        ["Flitsgesprek (5 min)", "Kort gesprek (10 min)",
         "Standaard (20 min)", "Diep (30 min)"],
        label_visibility="collapsed",
    )

    st.markdown("---")

    st.markdown("### Gespreksvorm")
    st.markdown("_(nog niet beschikbaar in deze versie)_")

    st.markdown("---")

    st.markdown("### Pantheon")
    st.markdown("_(nog niet beschikbaar in deze versie)_")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("← Terug", use_container_width=True):
            naar_geen_sessie()
            st.rerun()

    with col2:
        if st.button("Start gesprek", type="primary", use_container_width=True):
            duur_map = {
                "Flitsgesprek (5 min)": 5,
                "Kort gesprek (10 min)": 10,
                "Standaard (20 min)": 20,
                "Diep (30 min)": 30,
            }
            st.session_state.sessie_duur = duur_map.get(duur, 10)
            naar_incheck()
            st.rerun()


def toon_incheck():
    st.title("👋 Welkom")
    st.caption("Even een paar vragen voordat we beginnen.")

    st.markdown("---")

    st.markdown("_(nog niet beschikbaar in deze versie)_")

    if st.button("← Terug"):
        naar_parameters()
        st.rerun()


def toon_gesprek():
    st.title("🕐 Gesprek")
    st.caption("_(nog niet beschikbaar in deze versie)_")

    st.markdown("---")

    if st.button("Naar afsluiting"):
        naar_afsluiting()
        st.rerun()


def toon_afsluiting():
    st.title("🕊️ Afsluiting")
    st.caption("_(nog niet beschikbaar in deze versie)_")

    st.markdown("---")

    if st.button("Naar eindevaluatie"):
        naar_eindevaluatie()
        st.rerun()


def toon_eindevaluatie():
    st.title("🕊️ Eindgesprek")
    st.caption("_(nog niet beschikbaar in deze versie)_")

    st.markdown("---")

    if st.button("Naar archief"):
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
