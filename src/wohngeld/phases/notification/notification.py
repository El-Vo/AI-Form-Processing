from wohngeld.state import WohngeldState


class Notification:
    def __call__(self, state: WohngeldState) -> dict:
        decision = state.get("final_decision", "Unknown")
        benefit = state.get("calculated_benefit", 0.0)
        reason = state.get("disqualification_reason", "")

        if decision == "Approved":
            msg = f"Bewilligt. Betrag: {benefit} EUR."
        else:
            msg = (
                f"Abgelehnt. Grund: {reason if reason else 'Berechneter Betrag 0 EUR.'}"
            )

        print(f"---------------------------\n{msg}\n---------------------------")
        return {"current_phase": "phase_5_notification"}
