"""
Privacyverklaring voor Aurelius.
Wordt getoond via een knop in de zijbalk.
"""

import streamlit as st


PRIVACY_TEKST = """
# Privacyverklaring Aurelius

**Laatst bijgewerkt:** 28 oktober 2026

## Samenvatting

Wij bewaren alleen wat je zelf invult. Je gesprekken zijn alleen voor jou. Je kunt alles wissen via de knop "Wis alle gesprekken" in de zijbalk. Wij gebruiken je gegevens nooit voor onderzoek, marketing of andere doeleinden.

## 1. Wie wij zijn

Aurelius is een filosofische coach-app, een onderdeel van **Thomas Dijkman Medicinale Voeding** (geestelijke voeding / breinvoedsel). De app wordt beheerd door Thomas Dijkman, hierna te noemen "wij" of "de beheerder".

Voor vragen over deze privacyverklaring kun je contact opnemen via **camerathomas@gmail.com**.

## 2. Welke gegevens wij verwerken

Wij verwerken alleen gegevens die je zelf aan ons geeft:

- **Een gebruikersnaam** — zodat je gesprekken en voortgang bewaard blijven.
- **De antwoorden die je invult tijdens de incheck** — zoals wat je bezighoudt, hoe je je voelt, en welke intentie je hebt.
- **De gesprekken die je met de filosofen voert** — de tekstberichten die je uitwisselt met de coach.
- **Gearchiveerde sessies** — maar alleen als je daar zelf voor kiest.

Wij vragen **geen e-mailadres** en **geen wachtwoord**. De app werkt met een gebruikersnaam die je zelf kiest.

## 3. Wanneer wij gegevens opslaan

Wij slaan gegevens **alleen op als jij een account aanmaakt**. Zonder account worden er geen persoonlijke gegevens bewaard.

Wanneer je een account aanmaakt, bewaren wij je gebruikersnaam, zodat je later verder kunt waar je gebleven was.

## 4. Gearchiveerde sessies

Aan het einde van een gesprek kun je ervoor kiezen om de sessie te **archiveren**. Dat is een keuze, geen verplichting.

- **Als je archiveert**, wordt het gesprek opgeslagen in jouw persoonlijke archief.
- **Als je niet archiveert**, wordt het gesprek niet bewaard.

Gearchiveerde sessies zijn **uitsluitend voor jou**. Ze zijn alleen voor jou zichtbaar in je eigen archief.

## 5. Wat wij nooit doen

Wij gebruiken gearchiveerde sessies **nooit en te nimmer** voor andere doeleinden dan het voor jou beschikbaar stellen van je eigen gesprekken.

Concreet betekent dit:

- **Niemand** krijgt jouw sessies te lezen.
- Er wordt **geen informatie** uit jouw sessies gehaald.
- Jouw gesprekken worden **niet gebruikt** voor onderzoek, analyse, marketing, of welke andere doeleinden dan ook.
- Jouw gesprekken worden **niet gedeeld** met derden.

## 6. Verwerkers

Wij maken gebruik van de volgende diensten om de app te laten werken. Deze partijen verwerken gegevens in onze opdracht:

- **Google Gemini** (AI-reacties) — privacybeleid: https://policies.google.com/privacy
- **Turso** (database) — privacybeleid: https://turso.tech/privacy
- **Streamlit Cloud** (hosting) — privacybeleid: https://streamlit.io/privacy-policy

Deze partijen krijgen alleen de gegevens die nodig zijn om hun taak uit te voeren. Zij gebruiken jouw gegevens niet voor eigen doeleinden.

## 7. Rechtsgrond

Wij verwerken je gegevens op basis van:

- **Uitvoering van de overeenkomst** (je account en de gesprekken)
- **Jouw toestemming** (voor het archiveren van sessies)

## 8. Jouw rechten

Je hebt het recht om:

- Je account te laten verwijderen.
- Je gearchiveerde sessies te laten verwijderen.
- Inzage te vragen in de gegevens die wij van je hebben.
- Je gegevens te laten corrigeren.

Je kunt je gegevens **zelf verwijderen** via de knop "Wis alle gesprekken" in de zijbalk. Voor andere verzoeken kun je contact opnemen via **camerathomas@gmail.com**.

## 9. Beveiliging

Wij nemen passende maatregelen om jouw gegevens te beschermen tegen verlies, misbruik en ongeoorloofde toegang. Jouw gegevens worden opgeslagen op beveiligde servers.

**Let op:** de app gebruikt alleen een gebruikersnaam, geen wachtwoord. Kies daarom een naam die niet makkelijk te raden is. Als iemand anders jouw gebruikersnaam kent, kan hij of zij bij jouw gesprekken. Wij raden je aan om een unieke naam te kiezen die alleen jij kent.

## 10. Leeftijd

Deze app is bedoeld voor gebruikers van **16 jaar en ouder**.

## 11. Bewaartermijn

Wij bewaren je gegevens zolang je een account hebt.

- Als je je account verwijdert, worden je gegevens verwijderd.
- Lopende gesprekken worden bewaard zolang je ze kunt hervatten.
- Je kunt je gegevens altijd zelf verwijderen via de knop "Wis alle gesprekken".

## 12. Wijzigingen

Wij kunnen deze privacyverklaring aanpassen. De meest recente versie staat altijd in de app.

## 13. Contact

Voor vragen over deze privacyverklaring of over je gegevens kun je contact opnemen via **camerathomas@gmail.com**.
"""


def toon_privacy():
    """Toont de privacyverklaring in de app."""
    st.markdown(PRIVACY_TEKST)
