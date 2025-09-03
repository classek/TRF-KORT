TRF-kort Generator

Ett enkelt Python-verktyg med GUI för att skapa **TRF-kort (Tillstånd och Reglering av Fordon)** som PDF.  
Appen gör det smidigt att fylla i fordonsägare, förare och fordonsinformation, och genererar en färdig PDF-mall.  
Vissa fält lämnas tomma för manuell ifyllande och signering.

---

## Funktioner
- Grafiskt gränssnitt (Tkinter) för enkel inmatning
- Genererar en **juridiskt användbar PDF-mall**
- Fyll i:
  - Fordonsägare (namn, personnummer/org.nr, kontakt information)
  - Förare (namn, personnummer, kontakt)
  - Fordonsinformation (registreringsnummer, märke & modell)
- Lämnar tomma fält för:

    Ansvars- och kostnadsfördelning
  - Start- och slutdatum för tillstånd
  - Underskrifter från både fordonsägare och förare
 
  -   Är beroende av reportlab och Tkinter
