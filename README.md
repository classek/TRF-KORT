TRF-kort Generator

# TRF-kort Generator

Detta projekt är ett Python-baserat verktyg som genererar PDF-dokument för utlåning av fordon mellan två parter. 
Dokumenten innehåller automatiskt datum, ort, namn och underskriftsfält samt en juridisk klausul för att förtydliga 
att avtalet är bindande när båda parter signerat.

## Funktioner
- Skapar ett PDF-dokument i A4-format
- Automatiskt ifyllt datum och ort
- Underskriftsfält för både ägare och förare
- Namnförtydligande under underskriftslinjerna
- Juridisk text i foten:
  - "Detta dokument reglerar utlåning av fordon mellan ovanstående parter."
  - "Avtalet är giltigt endast när båda parter har undertecknat."
- Anpassat avstånd i botten för tydliga signaturer

## Krav
- Python 3.8 eller senare
- [ReportLab](https://pypi.org/project/reportlab/)

Installera beroenden:
```bash
pip install reportlab
