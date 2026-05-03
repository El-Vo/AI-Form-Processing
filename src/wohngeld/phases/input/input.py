import json
import logging
from pathlib import Path

from wohngeld.state import WohngeldState
from wohngeld.phases.input.llm.agent import InputValidatorAgent


class Input:
    def __init__(self) -> None:
        self.validator = InputValidatorAgent()

    def __call__(self, state: WohngeldState) -> dict:
        mock_path = self._select_mock()
        mock_data = self._load_mock(mock_path)
        input_data_str = json.dumps(mock_data)

        # Validiere Konsistenz
        validation_result = self.validator.validate_consistency(input_data_str)
        result_data = (
            validation_result.model_dump()  # type: ignore
            if hasattr(validation_result, "model_dump")
            else validation_result  # type: ignore
        )
        logging.info("InputValidator output: %s", result_data)

        inconsistencies = list(result_data.get("inkonsistenzen", []))  # type: ignore
        needs_human = result_data.get("benoetigt_manuelle_pruefung", False)  # type: ignore

        if needs_human:
            inconsistencies.append("Manuelle Pruefung noetig.")

        human_status = state.get("human_feedback_status", "")
        if needs_human:
            human_status = "pending"

        return {
            "current_phase": "phase_1_input",
            "input_data": input_data_str,
            "input_validation_inconsistencies": inconsistencies,
            "input_validation_needs_human": needs_human,
            "human_feedback_status": human_status,
            "human_feedback_phase": "phase_1_input" if needs_human else "",
            "rent": 0.0,
            "income": 0.0,
        }

    def _select_mock(self) -> Path:
        mocks_dir = Path(__file__).resolve().parents[4] / "mocks"
        mocks = sorted(mocks_dir.glob("*.json"))

        if not mocks:
            raise FileNotFoundError(f"Keine Mocks in ${mocks_dir} gefunden.")

        print("Verfuegbare Mocks:")
        for index, mock in enumerate(mocks, start=1):
            print(f"[{index}] {mock.name}")

        while True:
            choice = input(f"Waehle einen Mock (1-{len(mocks)}): ").strip()
            try:
                selected = mocks[int(choice) - 1]
            except (ValueError, IndexError):
                print("Ungueltige Auswahl. Bitte erneut versuchen.")
                continue
            return selected

    def _load_mock(self, mock_file: Path) -> dict:
        with open(mock_file, "r", encoding="utf-8") as file:
            return json.load(file)
