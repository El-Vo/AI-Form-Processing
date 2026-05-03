from wohngeld.llm.prompts import human_interpretation_help


def build_prompt(
    input_data: str,
    interpretation_context: str | None = None,
) -> str:
    interpretation_block = human_interpretation_help(interpretation_context)
    return (
        "Du bist Sachbearbeiter fuer Wohngeld. Pruefe die materielle Eignung.\n"
        "Dokumente: (formatiert als JSON):\n"
        f"{input_data}\n\n"
        f"{interpretation_block}\n"
        "Aufgabe:\n"
        "- Pruefe, ob disqualifizierende Leistungen genannt sind (z.B. Buergergeld, Grundsicherung, BAfoeg oder aehnliche).\n"
        "- Wenn klar vorhanden, ist_gueltig = false und ablehnungsgrund setzen.\n"
        "- Wenn nicht erkennbar, ist_gueltig = true.\n"
        "- Wenn unklar, benoetigt_manuelle_pruefung = true und bemerkungen setzen.\n\n"
        "Antworte ausschliesslich mit JSON in diesem Format:\n"
        "{\n"
        '  "ist_gueltig": true,\n'
        '  "ablehnungsgrund": "",\n'
        '  "benoetigt_manuelle_pruefung": false,\n'
        '  "bemerkungen": []\n'
        "}"
    )
