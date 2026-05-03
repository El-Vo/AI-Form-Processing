from pydantic import BaseModel, Field


class Result(BaseModel):
    """Strukturierter Output fuer die formale Pruefung."""

    ist_gueltig: bool = Field(
        description="True, wenn der Antrag formal gueltig ist.",
    )
    befunde: list[str] = Field(
        default_factory=list,
        description="Liste formaler Befunde oder Fehler.",
    )
    benoetigt_manuelle_pruefung: bool = Field(
        description="True, wenn eine manuelle Pruefung erforderlich ist.",
    )
