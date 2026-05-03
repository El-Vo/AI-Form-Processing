import json

from wohngeld.state import WohngeldState


class Decision:
    def __call__(self, state: WohngeldState) -> dict:
        raw_input = state.get("input_data", "{}")
        input_data = json.loads(raw_input) if isinstance(raw_input, str) else raw_input
        rent = input_data.get("basic_rent", 0.0)
        income = input_data.get("net_income", 0.0)

        benefit = round((income / 2.0) - rent, 2)
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
