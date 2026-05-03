from __future__ import annotations

import os

from langchain_mistralai import ChatMistralAI

API_KEY = "MISTRALAI_API_KEY"


class Agent:
    def __init__(self) -> None:
        api_key = os.getenv(API_KEY, "").strip()
        if not api_key:
            raise RuntimeError(
                f"{API_KEY} ist nicht gesetzt. Bitte als Umgebungsvariable setzen."
            )

        self.model = ChatMistralAI(
            api_key="lTQuAFf0Vd6K9Dw2IPsqUoIGfbDHTC1U",
            model_name="mistral-large-latest",
            temperature=0,
            max_retries=2,
        )
