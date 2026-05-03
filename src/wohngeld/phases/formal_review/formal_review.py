import logging

from wohngeld.state import WohngeldState
from wohngeld.phases.formal_review.llm.agent import FormalReviewAgent


class FormalReview:
    def __init__(self) -> None:
        self.reviewer = FormalReviewAgent()

    def __call__(self, state: WohngeldState) -> dict:
        input_data = state.get("input_data", {})

        answer = self.reviewer.pruefe_formal(input_data)
        answer_data = answer.model_dump() if hasattr(answer, "model_dump") else answer  # type: ignore
        logging.info("LLM FormalReview output: %s", answer_data)

        needs_human = answer_data["benoetigt_manuelle_pruefung"]  # type: ignore
        is_valid = answer_data["ist_gueltig"] or needs_human  # type: ignore
        inconsistencies = list(answer_data["befunde"])  # type: ignore

        if needs_human:
            inconsistencies.append("Manuelle Pruefung noetig.")

        human_status = state.get("human_feedback_status", "")
        if needs_human:
            human_status = "pending"

        return {
            "current_phase": "phase_2_formal_review",
            "is_formally_valid": is_valid,
            "formal_inconsistencies": inconsistencies,
            "formal_review_needs_human": needs_human,
            "human_feedback_status": human_status,
            "human_feedback_phase": "phase_2_formal_review" if needs_human else "",
            "final_decision": (
                "Rejected"
                if (not is_valid and not needs_human)
                else state.get("final_decision", "")
            ),
            "disqualification_reason": (
                " ; ".join(inconsistencies)
                if (not is_valid and not needs_human)
                else state.get("disqualification_reason", "")
            ),
        }
