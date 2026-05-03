def build_prompt(input_data: str) -> str:
    return (
        "Du bist Sachbearbeiter fuer Wohngeld. Pruefe die Konsistenz der eingelesenen Dokumente.\n"
        "Eingelesene Dokumente (formatiert als JSON):\n"
        f"{input_data}\n\n"
        "Aufgaben:\n"
        "1) Sind Einkommensangaben zwischen Antrag und Nachweis plausibel konsistent?\n"
        "2) Sind Mieteangaben im Antrag konsistent?\n"
        "3) Sind Nameneintraege identisch?\n"
        "4) Liste klare Widersprueche oder fehlende Konsistenz auf.\n\n"
        "Antworte ausschliesslich mit JSON in diesem Format:\n"
        "{\n"
        '  "ist_konsistent": true,\n'
        '  "inkonsistenzen": ["..."],\n'
        '  "benoetigt_manuelle_pruefung": false\n'
        "}\n\n"
        "Regeln:\n"
        "- Wenn du Widersprueche nicht eindeutig aufloesen kannst, setze 'benoetigt_manuelle_pruefung' auf true.\n"
        "- 'inkonsistenzen' ist eine Liste kurzer Saetze. Leere Liste bei voelliger Konsistenz."
    )
