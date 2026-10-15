"""
Uitleg voor Aurelius.
Wordt getoond via de Help-tab in het dashboard.
"""

import streamlit as st


UITLEG_TEKST = """
# Uitleg

Welkom bij Aurelius. Deze app is een filosofische coach. Geen
therapeut, geen adviseur, geen antwoordenmachine — maar een plek om
te denken, met filosofen die je uitnodigen om zelf te kijken, zelf te
vragen, zelf te kiezen.

Hieronder leggen we stap voor stap uit hoe je de app gebruikt.

---

## Stap 1 — Inloggen

Vul je naam in. Als je nieuw bent, kies dan een naam die je wilt
gebruiken. Als je al eerder bent geweest, vul dan dezelfde naam in —
dan vind je je oude gesprekken en voortgang terug.

Je gegevens worden alleen opgeslagen als je een account aanmaakt.
Zonder account wordt er niets bewaard.

---

## Stap 2 — Een sessie starten

Op het hoofdscherm kies je **Nieuwe sessie**. Daarna kies je:

### Duur
Hoe lang mag het gesprek duren? Kies uit:

- **Flitsgesprek** (5 min) — even snel
- **Kort gesprek** (10 min) — de standaard
- **Standaard** (20 min) — voor een echt gesprek
- **Diep** (30 min) — als je de tijd hebt

### Gespreksvorm
Welke vorm wil je? De simpelste is de **coach-sessie**: een gewoon
gesprek met het pantheon. Andere vormen komen vrij naarmate je level
stijgt.

### Pantheon
Met wie wil je spreken? Je kunt kiezen uit:

- **Standaard pantheon** van je level
- **Mijn eigen pantheon** — als je die hebt samengesteld

Het pantheon bestaat altijd uit **vijf filosofen**: één voorzitter en
vier deelnemers.

---

## Stap 3 — De incheck

Voordat het gesprek begint, krijg je een paar korte vragen. Die helpen
de filosofen om te weten waar je staat. Er zijn geen goede of foute
antwoorden — het is een moment om even stil te staan.

De vragen gaan over:

- Wat er speelt in je leven
- Hoe je je voelt
- Hoeveel overzicht je hebt
- Wat je intentie is voor dit gesprek

---

## Stap 4 — Het gesprek

Nu begint het echte werk. De **voorzitter** opent het gesprek met een
vraag. Daarna reageer je, en een van de andere filosofen antwoordt.

### Wie spreekt wanneer?

- **De voorzitter** opent het gesprek, doet de wendingen halverwege,
  en sluit af aan het einde.
- **De andere filosofen** reageren op wat jij zegt. Ze worden gekozen
  op basis van wat het beste past bij jouw onderwerp.

### Wat zijn wendingen?

Halverwege het gesprek kan er een **wending** komen. Dat is een
moment waarop de voorzitter het gesprek een nieuwe richting geeft.
Bijvoorbeeld: een vraag die je nog niet had gesteld, of een
perspectief dat je nog niet had gezien.

### Hoe lang duurt het?

De timer loopt. Als je bijna aan het einde bent, kun je kiezen:

- **Nog 3 minuten** — als je nog niet klaar bent
- **Afronden** — als je wilt afsluiten

---

## Stap 5 — De afsluiting

De voorzitter rondt het gesprek af met een korte, concluderende
gedachte. Daarna krijg je een paar **inzichtvragen**. Die helpen je om
stil te staan bij wat je hebt geleerd.

Wat neem je mee? Wat valt je op? Wat ga je anders doen?

---

## Stap 6 — Het eindgesprek

Na de afsluiting volgt het **eindgesprek**. De filosofen kijken terug
op wat er is gezegd. Ze reageren op elkaar, en op wat jij hebt
ingebracht.

Dit is geen herhaling van het gesprek — het is een moment van
reflectie. De filosofen laten zien wat ze hebben gehoord, en wat ze
belangrijk vinden.

---

## Stap 7 — Archiveren

Aan het einde kun je kiezen: **wil je deze sessie bewaren?**

- **Ja, archiveer** — het gesprek wordt opgeslagen in je persoonlijke
  archief. Je kunt het later teruglezen.
- **Nee, bewaar niet** — het gesprek wordt niet bewaard.

Gearchiveerde sessies zijn **alleen voor jou**. Niemand anders krijgt
ze te lezen.

---

## Tips voor een goed gesprek

1. **Neem de tijd.** De filosofen zijn geen antwoordenmachine. Ze
   stellen vragen, en wachten op jouw antwoord.

2. **Wees eerlijk.** Hoe opener je bent, hoe meer het gesprek je kan
   brengen.

3. **Laat het los.** Je hoeft geen perfect antwoord te hebben. Soms is
   "ik weet het niet" het beste begin.

4. **Lees terug.** In je archief kun je oude gesprekken teruglezen.
   Soms zie je dingen die je toen niet zag.

5. **Probeer verschillende filosofen.** Elk kijkt op een andere manier
   naar wat je meebrengt. Soms raakt een filosoof je die je niet had
   verwacht.

---

## Het dashboard

Via de zijbalk kun je naar het **dashboard**. Daar vind je:

- **Voortgang** — je level, tier, en hoeveel filosofen en
  gespreksvormen je hebt vrijgespeeld.
- **Archief** — al je bewaarde sessies.
- **Favorieten** — je favoriete filosoof en je eigen pantheon.
- **Filosofen** — biografieën van alle filosofen.
- **Help** — deze uitleg, de FAQ, de privacyverklaring, en de
  algemene voorwaarden.

---

## Tot slot

Aurelius is geen app die je "even" gebruikt. Het is een plek om te
vertragen. Om te denken. Om te kijken naar wat je meebrengt, en wat je
ermee doet.

Begin rustig. Er is geen goed of fout gesprek.
"""


def toon_uitleg():
    """Toont de uitleg in de app."""
    st.markdown(UITLEG_TEKST)
