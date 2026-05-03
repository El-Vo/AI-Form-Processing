from pydantic import BaseModel, Field


class Result(BaseModel):
    """Strukturierter Output fuer die materielle Pruefung."""

    ist_gueltig: bool = Field(
        description="True, wenn der Antrag materiell gueltig ist.",
    )
    ablehnungsgrund: str = Field(
        default="",
        description="Ablehnungsgrund, falls ungueltig.",
    )
    benoetigt_manuelle_pruefung: bool = Field(
        description="True, wenn eine manuelle Pruefung erforderlich ist.",
    )
    bemerkungen: list[str] = Field(
        default_factory=list,
        description="Zusatzhinweise oder Auffaelligkeiten.",
    )
