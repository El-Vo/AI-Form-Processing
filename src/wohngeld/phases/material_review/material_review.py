import logging

from wohngeld.state import WohngeldState
from wohngeld.phases.material_review.llm.agent import MaterialReviewAgent


class MaterialReview:
    def __init__(self) -> None:
        self.reviewer = MaterialReviewAgent()

    def __call__(self, state: WohngeldState) -> dict:
        input_data = state.get("input_data", {})
        interpretation = state.get("interpretation_context", "")

        answer = self.reviewer.pruefe_materiell(input_data, interpretation)
        answer_data = answer.model_dump() if hasattr(answer, "model_dump") else answer  # type: ignore
        logging.info("LLM MaterialReview output: %s", answer_data)

        needs_human = answer_data["benoetigt_manuelle_pruefung"]  # type: ignore
        is_valid = answer_data["ist_gueltig"] or needs_human  # type: ignore
        notes = list(answer_data["bemerkungen"])  # type: ignore
        reason = answer_data["ablehnungsgrund"]  # type: ignore

        if needs_human:
            notes.append("Manuelle Pruefung noetig.")

        human_status = state.get("human_feedback_status", "")
        if needs_human:
            human_status = "pending"

        return {
            "current_phase": "phase_3_material_review",
            "is_materially_valid": is_valid,
            "material_review_needs_human": needs_human,
            "material_review_notes": notes,
            "human_feedback_status": human_status,
            "human_feedback_phase": "phase_3_material_review" if needs_human else "",
            "disqualification_reason": (
                reason if not is_valid else state.get("disqualification_reason", "")
            ),
            "final_decision": (
                "Rejected"
                if (not is_valid and not needs_human)
                else state.get("final_decision", "")
            ),
        }
