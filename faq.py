"""
Veelgestelde vragen voor Aurelius.
Wordt getoond via de Help-tab in het dashboard.
"""

import streamlit as st


FAQ_TEKST = """
# Veelgestelde vragen

## Algemeen

**Wat is Aurelius?**
Aurelius is een filosofische coach-app. Je voert een gesprek met een
pantheon van AI-filosofen. Ze stellen vragen, ze luisteren, en ze
helpen je om zelf te denken. Het is geen therapeut en geen
antwoordenmachine.

**Is Aurelius een therapeut?**
Nee. Aurelius is geen vervanging voor een therapeut, een arts, of een
crisis-dienst. Als je in een medische of psychische noodsituatie zit,
zoek dan professionele hulp.

**Voor wie is het bedoeld?**
Voor iedereen die wil nadenken over het leven, over keuzes, over wat
je bezighoudt. Je hoeft geen filosoof te zijn. Je hoeft alleen maar
nieuwsgierig te zijn.

---

## Gebruik

**Hoe begin ik?**
Vul je naam in, kies een sessie, doorloop de incheck, en begin te
praten. De filosofen doen de rest.

**Hoe kies ik mijn pantheon?**
Bij het starten van een sessie kun je kiezen tussen het standaard
pantheon van je level, of je eigen pantheon. Je eigen pantheon stel je
samen door een voorzitter en vier filosofen te kiezen.

**Wat is een wending?**
Een wending is een moment halverwege het gesprek waarop de voorzitter
het gesprek een nieuwe richting geeft. Dat kan een vraag zijn, een
observatie, of een nieuw perspectief.

**Kan ik een gesprek hervatten?**
Als je de app sluit en later terugkomt, kun je een lopend gesprek
hervatten — mits je ingelogd bent met dezelfde naam. Je gesprek wordt
automatisch opgeslagen.

**Kan ik een gesprek verwijderen?**
Ja. In de zijbalk vind je de knop **Wis alle gesprekken**. Die
verwijdert al je berichten, sessies en inzichten.

---

## Kosten

**Wat kost het?**
- **Losse sessie:** €2,50 per gesprek
- **Basic abonnement:** €5,00 per maand
- **Gold abonnement:** €15,00 per maand

**Kan ik opzeggen?**
Ja. Een abonnement kun je op elk moment opzeggen. Je houdt toegang tot
het einde van de betaalperiode.

**Krijg ik mijn geld terug?**
Je hebt 14 dagen herroepingsrecht op je eerste aankoop. Als je een
sessie al hebt gebruikt, vervalt dat recht — want dan is de dienst
geleverd.

---

## Gegevens

**Wat gebeurt er met mijn gegevens?**
Je gegevens worden alleen opgeslagen als je een account aanmaakt. Je
gesprekken zijn alleen voor jou. Wij gebruiken ze nooit voor andere
doeleinden. Zie de privacyverklaring voor alle details.

**Kan ik mijn gegevens laten verwijderen?**
Ja. Via de knop **Wis alle gesprekken** in de zijbalk, of door contact
met ons op te nemen.

---

## Technisch

**Werkt het op mijn telefoon?**
Ja. De app werkt in elke moderne browser, op elk apparaat.

**Wat als de app niet werkt?**
Probeer de pagina te verversen. Als het probleem blijft, probeer het
dan later opnieuw. Bij een database-storing krijg je een melding in de
app.

**Waarom duurt het soms even voordat een filosoof antwoordt?**
De filosofen worden gegenereerd door een AI-model. Dat kost even tijd.
Soms een paar seconden, soms wat langer.

---

## Contact

Heb je een vraag die hier niet bij staat? Neem contact op via
[e-mailadres].
"""


def toon_faq():
    """Toont de FAQ in de app."""
    st.markdown(FAQ_TEKST)
