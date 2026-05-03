def build_prompt(input_data: str) -> str:
    return (
        "Du bist Sachbearbeiter fuer Wohngeld. Pruefe, ob die Pflichtfelder vorhanden sind.\n"
        "Eingelesene Dokumente (formatiert als JSON):\n"
        f"{input_data}\n\n"
        "Aufgaben:\n"
        "1) Sind Name des Antragstellers, monatliche Miete und Nettoeinkommen vorhanden?\n"
        "2) Extrahiere die monatliche Miete (rent) und das Nettoeinkommen (income).\n"
        "3) Liste fehlende Pflichtfelder auf.\n\n"
        "Antworte ausschliesslich mit JSON in diesem Format:\n"
        "{\n"
        '  "ist_gueltig": true,\n'
        '  "befunde": ["..."],\n'
        '  "benoetigt_manuelle_pruefung": false,\n'
        '  "rent": 0.0,\n'
        '  "income": 0.0\n'
        "}\n\n"
        "Regeln:\n"
        "- ist_gueltig ist true, wenn alle drei Felder vorhanden sind.\n"
        "- 'befunde' ist eine Liste kurzer Saetze mit fehlenden Feldern. Leere Liste bei vollstaendigen Angaben.\n"
        "- 'rent' und 'income' sollen numerische Werte in EUR sein. Bei fehlenden Werten 0.0 setzen."
    )
