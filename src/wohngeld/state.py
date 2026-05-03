from typing import TypedDict


class WohngeldState(TypedDict):
    # Phase 1: Eingaben
    input_data: str

    # Phase 2 & 3: Pruefungen
    is_formally_valid: bool
    formal_inconsistencies: list[str]
    formal_review_needs_human: bool
    human_feedback_status: str
    human_feedback_phase: str
    interpretation_context: str
    is_materially_valid: bool
    material_review_needs_human: bool
    material_review_notes: list[str]
    disqualification_reason: str

    # Phase 4: Extraktion & Berechnung
    calculated_benefit: float
    human_approved: bool

    # Pipeline Meta
    current_phase: str
    final_decision: str  # "Approved" | "Rejected"
