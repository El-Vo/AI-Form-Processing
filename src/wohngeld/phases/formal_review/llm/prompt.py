def build_prompt(input_data: str) -> str:
    return (
        "Du bist Sachbearbeiter fuer Wohngeld. Pruefe die formale Plausibilitaet.\n"
        "Eingelesene Dokumente (formatiert als JSON):\n"
        f"{input_data}\n\n"
        "Aufgaben:\n"
        "1) Sind alle Dokumente ausreichend lesbar/auswertbar?\n"
        "2) Sind Einkommensangaben zwischen Antrag und Nachweis plausibel konsistent?\n"
        "3) Liste klare Widersprueche oder fehlende Pflichtangaben.\n\n"
        "Antworte ausschliesslich mit JSON in diesem Format:\n"
        "{\n"
        '  "ist_gueltig": true,\n'
        '  "befunde": ["..."],\n'
        '  "benoetigt_manuelle_pruefung": false\n'
        "}\n\n"
        "Regeln:\n"
        "- Wenn du wichtige Angaben nicht sicher findest, setze 'benoetigt_manuelle_pruefung' auf true.\n"
        "- 'befunde' ist eine Liste kurzer Saetze. Leere Liste bei keinen Auffaelligkeiten."
    )
