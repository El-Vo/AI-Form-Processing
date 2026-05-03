def human_interpretation_help(interpretation_context: str | None) -> str:
    if not interpretation_context:
        return ""
    return (
        "\nInterpretationshilfe vom Menschen:\n"
        f"{interpretation_context}\n"
        "Bitte diese Hinweise priorisiert beruecksichtigen.\n"
    )
