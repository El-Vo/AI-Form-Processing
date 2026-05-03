from pydantic import BaseModel, Field


class Result(BaseModel):
    """Strukturierter Output fuer die Eingabevalidierung."""

    ist_konsistent: bool = Field(
        description="True, wenn die Eintraege zwischen Dokumenten konsistent sind.",
    )
    inkonsistenzen: list[str] = Field(
        default_factory=list,
        description="Liste erkannter Inkonsistenzen zwischen Dokumenten.",
    )
    benoetigt_manuelle_pruefung: bool = Field(
        description="True, wenn eine manuelle Pruefung erforderlich ist.",
    )
