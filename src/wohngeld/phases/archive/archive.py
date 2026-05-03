import json
import os
from datetime import datetime, timezone
from wohngeld.state import WohngeldState


class Archive:
    def __call__(self, state: WohngeldState) -> dict:
        now = datetime.now(timezone.utc)
        archive_data = {
            "timestamp": now.isoformat(),
            "application_result": state.get("final_decision", "Rejected"),
            "rejection_reason": state.get("disqualification_reason", ""),
            "calculated_amount_eur": state.get("calculated_benefit", 0.0),
            "human_reviewed": state.get("human_approved", False),
            "input_data": state.get("input_data", {}),
        }

        os.makedirs("archives", exist_ok=True)
        filename = f"archives/result_{now.strftime('%Y%m%d%H%M%S')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(archive_data, f, indent=2, ensure_ascii=False)

        return {"current_phase": "phase_6_archive"}
