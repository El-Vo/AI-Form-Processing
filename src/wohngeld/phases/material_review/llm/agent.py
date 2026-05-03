from wohngeld.llm.generic_agent import Agent
from wohngeld.phases.material_review.llm.output import Result
from wohngeld.phases.material_review.llm.prompt import build_prompt


class MaterialReviewAgent:
    def __init__(self) -> None:
        self.generic_agent = Agent().model
        self.agent = self.generic_agent.with_structured_output(
            Result, method="json_mode"
        )

    def pruefe_materiell(self, input_data: str, interpretation_context: str):
        prompt = build_prompt(
            input_data,
            interpretation_context,
        )
        return self.agent.invoke(prompt)
