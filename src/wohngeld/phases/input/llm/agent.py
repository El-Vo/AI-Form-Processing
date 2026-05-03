from wohngeld.llm.generic_agent import Agent
from wohngeld.phases.input.llm.output import Result
from wohngeld.phases.input.llm.prompt import build_prompt


class InputValidatorAgent:
    def __init__(self) -> None:
        self.generic_agent = Agent().model
        self.agent = self.generic_agent.with_structured_output(
            Result, method="json_schema"
        )

    def validate_consistency(self, input_data: str):
        prompt = build_prompt(input_data)
        return self.agent.invoke(prompt)
