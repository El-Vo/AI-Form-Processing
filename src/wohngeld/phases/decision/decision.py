import json

from wohngeld.state import WohngeldState


class Decision:
    def __call__(self, state: WohngeldState) -> dict:
        rent = state.get("rent", "{}")
        income = state.get("income", "{}")
        benefit = round(((income / 2.0) - rent) * (-1), 2)
        decision = "Approved" if benefit > 10.0 else "Rejected"
        reason = ""
        if decision == "Rejected":
            reason = "Wohnformel <= 10 EUR."

        return {
            "current_phase": "phase_4_decision",
            "calculated_benefit": benefit,
            "final_decision": decision,
            "disqualification_reason": reason
            or state.get("disqualification_reason", ""),
        }
