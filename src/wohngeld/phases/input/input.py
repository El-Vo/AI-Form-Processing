import json
from pathlib import Path

from wohngeld.state import WohngeldState


class Input:
    def __call__(self, state: WohngeldState) -> dict:
        mock_path = self._select_mock()
        mock_data = self._load_mock(mock_path)

        return {
            "current_phase": "phase_1_input",
            "input_data": json.dumps(mock_data),
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
