from pydantic import BaseModel, Field


class Result(BaseModel):
    """Strukturierter Output fuer die formale Pruefung."""

    ist_gueltig: bool = Field(
        description="True, wenn Name, Miete und Nettoeinkommen vorhanden sind.",
    )
    befunde: list[str] = Field(
        default_factory=list,
        description="Liste fehlender Pflichtfelder oder Fehler.",
    )
    benoetigt_manuelle_pruefung: bool = Field(
        description="True, wenn eine manuelle Pruefung erforderlich ist.",
    )
    rent: float = Field(
        default=0.0,
        description="Monatliche Miete in EUR.",
    )
    income: float = Field(
        default=0.0,
        description="Nettoeinkommen in EUR.",
    )
