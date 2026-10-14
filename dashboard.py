"""
Dashboard voor Aurelius.
Toont het archief, de voortgang, de favorieten en de filosofen.
"""

import streamlit as st

from filosofen import FILOSOFEN, PANTHEON_PER_LEVEL
from opslag import laad_sessies, bewaar_profiel


def toon_dashboard(gebruiker_id, profiel):
    """Toont het hele dashboard."""
    st.title("🏛️ Jouw dashboard")
    st.caption(f"Welkom terug, {gebruiker_id}.")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Archief", "Voortgang", "Favorieten", "Filosofen"]
    )

    with tab1:
        _toon_archief(gebruiker_id, profiel)

    with tab2:
        _toon_voortgang(profiel)

    with tab3:
        _toon_favorieten(profiel)

    with tab4:
        _toon_filosofen(profiel)


# ============================================================
# Archief
# ============================================================
def _toon_archief(gebruiker_id, profiel):
    """Toont de gearchiveerde sessies."""
    st.markdown("### Jouw archief")

    sessies = laad_sessies(gebruiker_id)

    if not sessies:
        st.markdown(
            "Je hebt nog geen sessies gearchiveerd. "
            "Na elk gesprek kun je de sessie bewaren, en dan verschijnt "
            "hij hier."
        )
        return

    st.caption(f"{len(sessies)} sessies gevonden.")

    for sessie in sessies:
        datum = str(sessie.get("datum", "?"))[:16]
        thema = sessie.get("thema", "onbekend")

        with st.expander(f"📁 {datum} — {thema}"):
            # Pantheon
            pantheon = sessie.get("pantheon", [])
            if pantheon:
                namen = [
                    FILOSOFEN[f]["naam"]
                    for f in pantheon
                    if f in FILOSOFEN
                ]
                st.markdown(f"**Pantheon:** {', '.join(namen)}")

            # Duur
            duur = sessie.get("duur_minuten", "?")
            st.markdown(f"**Duur:** {duur} minuten")

            # Incheck
            incheck = sessie.get("incheck", {})
            if incheck:
                st.markdown("**Incheck:**")
                st.markdown(f"- Wat speelt er: {incheck.get('openheid', '—')}")
                st.markdown(f"- Emotie: {incheck.get('emotie', '—')}")
                st.markdown(f"- Overzicht: {incheck.get('overzicht', '—')}/10")
                st.markdown(f"- Intentie: {incheck.get('intentie', '—')}")
                volgorde = incheck.get("volgorde", [])
                if volgorde:
                    st.markdown(f"- Volgorde: {' → '.join(volgorde)}")

            # Gesprek
            gesprek = sessie.get("gesprek", [])
            if gesprek:
                st.markdown("### Gesprek")
                for bericht in gesprek:
                    naam = bericht.get("naam", "?")
                    tekst = bericht.get("tekst", "")
                    st.markdown(f"**{naam}:** {tekst}")

            # Rondes
            rondes = sessie.get("rondes", {})
            if rondes:
                st.markdown("### Eindgesprek")
                for ronde_naam, reacties in rondes.items():
                    st.markdown(f"**{ronde_naam.replace('_', ' ').title()}**")
                    for r in reacties:
                        st.markdown(
                            f"**{r.get('naam', '?')}:** {r.get('tekst', '')}"
                        )

            # Afsluiter
            afsluiter = sessie.get("afsluiter", {})
            if afsluiter:
                st.markdown("### Afsluiting")
                st.markdown(
                    f"**{afsluiter.get('naam', '?')}:** "
                    f"{afsluiter.get('tekst', '')}"
                )

            # PDF-download (alleen voor basic en gold)
            from tiers import heeft_toegang
            _tier = profiel.get("tier", "sessie")
            _level = profiel.get("level", 1)

            if heeft_toegang(_tier, _level, "pdf"):
                st.markdown("---")
                from pdf import maak_pdf
                try:
                    pdf_pad = maak_pdf(sessie=sessie)
                    with open(pdf_pad, "rb") as f:
                        pdf_bytes = f.read()
                    st.download_button(
                        "📄 Download als PDF",
                        pdf_bytes,
                        file_name=f"aurelius_{str(sessie.get('datum', ''))[:10]}.pdf",
                        mime="application/pdf",
                        key=f"pdf_{sessie.get('id', 'x')}",
                    )
                except Exception as e:
                    st.caption(f"PDF kon niet worden gemaakt: {e}")


# ============================================================
# Voortgang
# ============================================================
def _toon_voortgang(profiel):
    """Toont de voortgang van de gebruiker."""
    st.markdown("### Jouw voortgang")
    st.markdown(f"**Level:** {profiel.get('level', 1)}")
    st.markdown(f"**Tier:** {profiel.get('tier', 'sessie')}")

    # Vrijgespeelde filosofen
    from tiers import beschikbare_filosofen
    tier = profiel.get("tier", "sessie")
    level = profiel.get("level", 1)
    filosofen = beschikbare_filosofen(tier, level)
    st.markdown(f"**Vrijgespeelde filosofen:** {len(filosofen)}")

    # Vrijgespeelde gespreksvormen
    from gespreksvormen import beschikbare_vormen
    vormen = beschikbare_vormen(profiel)
    st.markdown(f"**Vrijgespeelde gespreksvormen:** {len(vormen)}")

    st.caption("Meer statistieken volgen later.")


# ============================================================
# Favorieten
# ============================================================
def _toon_favorieten(profiel):
    """Toont de favorieten van de gebruiker."""
    st.markdown("### Jouw favorieten")

    level = profiel.get("level", 1)
    tier = profiel.get("tier", "sessie")

    _toon_favoriet_filosoof(profiel, level, tier)


def _toon_favoriet_filosoof(profiel, level, tier):
    """Toont de keuze voor de favoriete filosoof."""
    from tiers import heeft_toegang, beschikbare_filosofen, drempel_van

    st.markdown("#### Favoriete filosoof")
    st.caption(
        "Kies de filosoof die je het meeste aanspreekt. "
        "Hij zit altijd in je eigen pantheon."
    )

    if not heeft_toegang(tier, level, "favoriete_filosoof"):
        drempel = drempel_van("favoriete_filosoof")
        st.text_input(
            "Favoriete filosoof",
            value="",
            disabled=True,
            placeholder=f"Beschikbaar vanaf level {drempel}"
            if drempel else "Niet beschikbaar",
            key="favoriete_filosoof_disabled"
        )
        return

    opties = ["Geen"] + beschikbare_filosofen(tier, level)
    huidige = profiel.get("favoriete_filosoof") or "Geen"
    if huidige not in opties:
        huidige = "Geen"

    keuze = st.selectbox(
        "Favoriete filosoof",
        opties,
        index=opties.index(huidige),
        format_func=lambda x: (
            f"{FILOSOFEN[x]['emoji']} {FILOSOFEN[x]['naam']}"
            if x in FILOSOFEN else "Geen"
        ),
        key="favoriete_filosoof_keuze"
    )

    if keuze != huidige:
        nieuwe_favoriet = None if keuze == "Geen" else keuze
        oude_favoriet = profiel.get("favoriete_filosoof")

        # Werk het eigen pantheon bij
        eigen_pantheon = list(profiel.get("eigen_pantheon", []))

        # Verwijder de oude favoriet
        if oude_favoriet and oude_favoriet in eigen_pantheon:
            eigen_pantheon.remove(oude_favoriet)

        # Voeg de nieuwe favoriet toe
        if nieuwe_favoriet:
            if nieuwe_favoriet not in eigen_pantheon:
                if len(eigen_pantheon) >= 5:
                    eigen_pantheon = eigen_pantheon[:-1] + [nieuwe_favoriet]
                else:
                    eigen_pantheon.append(nieuwe_favoriet)

        profiel["favoriete_filosoof"] = nieuwe_favoriet
        profiel["eigen_pantheon"] = eigen_pantheon
        bewaar_profiel(profiel)
        st.success("Favoriete filosoof opgeslagen.")
        st.rerun()


# ============================================================
# Filosofen
# ============================================================
def _toon_filosofen(profiel):
    """Toont alle filosofen met een index en interne links."""
    from filosofen import FILOSOFEN
    from filosofen_biografieen import BIOGRAFIEEN
    from tiers import beschikbare_filosofen

    st.markdown("### Filosofen")
    st.caption("Klik op een naam om naar de biografie te springen.")

    tier = profiel.get("tier", "sessie")
    level = profiel.get("level", 1)

    # Welke filosofen zijn beschikbaar?
    opties = beschikbare_filosofen(tier, level)

    # Sorteer op naam
    opties_gesorteerd = sorted(
        opties,
        key=lambda x: FILOSOFEN.get(x, {}).get("naam", x),
    )

    # ============================================================
    # Index
    # ============================================================
    index_html = '<div id="index"><h2>Index</h2><ul>'
    for f in opties_gesorteerd:
        if f in FILOSOFEN and f in BIOGRAFIEEN:
            naam = FILOSOFEN[f]["naam"]
            index_html += f'<li><a href="#{f}">{naam}</a></li>'
    index_html += "</ul></div>"

    st.markdown(index_html, unsafe_allow_html=True)

    st.markdown("---")

    # ============================================================
    # Biografieën
    # ============================================================
    for f in opties_gesorteerd:
        if f not in FILOSOFEN or f not in BIOGRAFIEEN:
            continue

        bio = BIOGRAFIEEN[f]
        emoji = FILOSOFEN[f]["emoji"]

        # Anker voor deze filosoof
        st.markdown(
            f'<h2 id="{f}">{emoji} {bio["naam"]}</h2>',
            unsafe_allow_html=True,
        )
        st.caption(f"_{bio['leefde']}_")
        st.markdown(f"**Stroming:** {bio['stroming']}")

        st.markdown("**Bekende boeken:**")
        for boek in bio["boeken"]:
            st.markdown(f"- {boek}")

        st.markdown("**Bekende uitspraken:**")
        for uitspraak in bio["uitspraken"]:
            st.markdown(f"> *{uitspraak}*")

        st.markdown("**Visie:**")
        st.markdown(bio["visie"])

        # Terug naar index
        st.markdown(
            '<a href="#index">↑ Terug naar index</a>',
            unsafe_allow_html=True,
        )

        st.markdown("---")

        st.markdown("### Visie")
        st.markdown(bio["visie"])
