# Projekt Black Statter - Del 1
En statistik app, hvis eneste formål er at forsøge at indsamle dagsaktuelle priser fra danske webshops på vare navne som brugeren har indtastet og ønsker at holde øje med over tid.

* Alt kode skal skrives i Python
* Data skal gemmes i en Duckdb database
* Man skal kunne oprette, rette og slette produkter manuelt via brugergrænsefladen
* Man skal kunne oprette, rette og slette pris transaktioner for en vare manuelt
* Der skal gemmes information om Dato og tid, url til hvor man har fundet prisen, og prisen for hver transaktion
* Der skal være en graf så man på en vare kan følge prisudviklingen for varen over tid.
* Brugergrænsefladen skal være tekst baseret ved brug af Textual modulet, også grafen som måske kan løses med textual-plotext modulet, men kom gerne med forslag til anden løsning.
* Brugergrænsefladen skal kunne navigeres uden brug af mus. Alt skal være styret med tastaturet.

## Krav til teknik der skal anvendes
- Alt kode skal skrives i python
- Projektet er initieret med UV og UV skal anvendes til håndtering af dependencies mm.
- Data skal gemmes i en duckdb database så man efterfølgende vil kunne lave statistik på disse data.
- Pydantic anvendes til datamodeller
- Settings der skal gemmes skal placeres i en env fil der ikke committes.
- Alt lokalisering af appen skal anvende brugerens system locale. Dog skal det kunne konfigureres i env filen hvilken locale der evt anvendes.
