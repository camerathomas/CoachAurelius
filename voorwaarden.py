"""
Algemene voorwaarden voor Aurelius.
Wordt getoond via een knop in de zijbalk.
"""

import streamlit as st


VOORWAARDEN_TEKST = """
# Algemene voorwaarden Aurelius

**Laatst bijgewerkt:** 28 oktober 2026

## 1. Wie wij zijn

Aurelius is een filosofische coach-app, een onderdeel van **Thomas Dijkman Medicinale Voeding** (geestelijke voeding / breinvoedsel). De app wordt beheerd door Thomas Dijkman, hierna te noemen "wij" of "de aanbieder".

**Contactgegevens:**
- E-mail: camerathomas@gmail.com
- Adres: [vestigingsadres]

## 2. Toepasselijkheid

Deze algemene voorwaarden zijn van toepassing op alle overeenkomsten tussen jou (de consument) en ons (de aanbieder) met betrekking tot het gebruik van de Aurelius-app.

Door een account aan te maken of de app te gebruiken, ga je akkoord met deze voorwaarden.

## 3. De dienst

Aurelius is een filosofische coach-app. De app biedt:

- Gesprekken met AI-gestuurde filosofen
- Gepersonaliseerde coaching-sessies
- Een archief van eerdere sessies (optioneel)

Wij doen ons uiterste best om de dienst beschikbaar en functioneel te houden, maar wij garanderen geen ononderbroken beschikbaarheid.

## 4. Accounts en registratie

Je maakt een account aan met een gebruikersnaam. Je bent zelf verantwoordelijk voor:

- De juistheid van je gegevens
- Alle activiteiten die via jouw account plaatsvinden

**Let op:** de app gebruikt alleen een gebruikersnaam, geen wachtwoord. Kies daarom een naam die niet makkelijk te raden is. Wij raden je aan om een unieke naam te kiezen die alleen jij kent.

## 5. AI en de filosofen

De filosofen in de app zijn AI-personages. Zij zijn geen echte mensen en hun reacties worden gegenereerd door een AI-model (Google Gemini). De reacties kunnen onjuist, onvolledig of onverwacht zijn. Gebruik de app niet als vervanging voor professionele medische, psychologische of juridische hulp.

## 6. Prijzen en betaling

Wij bieden de volgende opties:

**Losse sessies:**
- **Premium sessie:** €2,50 per sessie
- **Gold sessie:** €3,50 per sessie

**Bundels (10 sessies):**
- **Premium bundel:** €19,00 voor 10 sessies
- **Gold bundel:** €29,00 voor 10 sessies

**Introductiekorting (eerste maand):**
- **Premium en Gold sessie:** €1,00 per sessie
- **Premium en Gold bundel (10 sessies):** €8,00 per bundel

Alle prijzen zijn inclusief btw, tenzij anders vermeld.

Betaling vindt plaats via de betaalmethoden die in de app worden aangeboden. Er zijn geen abonnementen; je betaalt per sessie of per bundel.

Wij kunnen onze prijzen wijzigen. Bij een prijswijziging informeren wij je minimaal 30 dagen van tevoren.

## 7. Herroepingsrecht

**Je hebt het recht om binnen 14 dagen na aankoop de overeenkomst zonder opgave van redenen te herroepen.**

Dit recht geldt voor de aankoop van losse sessies en bundels, zolang de sessies nog niet zijn gebruikt.

Om je herroepingsrecht uit te oefenen, stuur je een e-mail naar **camerathomas@gmail.com** met een duidelijke verklaring dat je de overeenkomst herroept. Wij bevestigen de ontvangst en betalen binnen 14 dagen het volledige bedrag terug.

**Uitzondering:** het herroepingsrecht vervalt zodra je een sessie daadwerkelijk hebt gebruikt, omdat de dienst dan volledig is geleverd. Bij de aankoop vragen wij je uitdrukkelijk om toestemming voor directe levering. Door deze toestemming vervalt je herroepingsrecht zodra de sessie is gestart.

## 8. Gebruik van de dienst

Je mag de app alleen gebruiken voor persoonlijke, niet-commerciële doeleinden. Het is niet toegestaan om:

- De app te gebruiken voor illegale doeleinden
- De app te reverse-engineeren of te kopiëren
- Inhoud te uploaden die in strijd is met de wet
- De app te gebruiken om anderen te schaden
- De AI bewust te manipuleren of schadelijke reacties uit te lokken

Wij behouden ons het recht voor om je account te schorsen of te beëindigen als je deze voorwaarden schendt.

## 9. Intellectueel eigendom

Alle inhoud in de app — waaronder de filosofen-personages, de gesprekslogica, en de vormgeving — is eigendom van de aanbieder.

Jouw gesprekken en inzichten zijn van jou. Wij claimen geen eigendom over de inhoud die jij inbrengt.

## 10. Aansprakelijkheid

Aurelius is een coach-app, geen therapeut, geen arts, en geen crisis-dienst. De app is niet bedoeld voor medische of psychische noodgevallen.

Wij zijn niet aansprakelijk voor:

- Schade die voortkomt uit het gebruik van de app
- Beslissingen die je neemt op basis van gesprekken in de app
- Technische storingen of gegevensverlies

Onze aansprakelijkheid is beperkt tot het bedrag dat je voor de dienst hebt betaald, **behalve in gevallen van opzet, grove nalatigheid, of schade door dood of letsel.**

## 11. Beschikbaarheid en wijzigingen

Wij kunnen de dienst op elk moment wijzigen, tijdelijk opschorten, of beëindigen. Bij belangrijke wijzigingen informeren wij je vooraf.

Als wij de dienst definitief beëindigen, heb je recht op een proportionele terugbetaling van je bundel of losse sessies.

## 12. Gegevens en bewaring

Voor informatie over hoe wij omgaan met je gegevens en hoe lang wij ze bewaren, verwijzen wij naar onze privacyverklaring.

## 13. Klachten en geschillen

Heb je een klacht? Neem contact op via **camerathomas@gmail.com**. Wij proberen binnen 14 dagen te reageren.

Als wij er niet samen uitkomen, kun je je klacht voorleggen aan de bevoegde rechter in Nederland.

## 14. Toepasselijk recht

Op deze voorwaarden is Nederlands recht van toepassing.

## 15. Wijzigingen van deze voorwaarden

Wij kunnen deze voorwaarden aanpassen. De meest recente versie staat altijd in de app. Bij belangrijke wijzigingen informeren wij je vooraf via een melding in de app.

## 16. Contact

Voor vragen over deze voorwaarden kun je contact opnemen via **camerathomas@gmail.com**.
"""


def toon_voorwaarden():
    """Toont de algemene voorwaarden in de app."""
    st.markdown(VOORWAARDEN_TEKST)
