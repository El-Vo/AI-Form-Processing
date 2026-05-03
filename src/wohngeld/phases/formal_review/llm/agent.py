from wohngeld.llm.generic_agent import Agent
from wohngeld.phases.formal_review.llm.output import Result
from wohngeld.phases.formal_review.llm.prompt import build_prompt


class FormalReviewAgent:
    def __init__(self) -> None:
        self.generic_agent = Agent().model
        self.agent = self.generic_agent.with_structured_output(
            Result, method="json_schema"
        )

    def pruefe_formal(self, input_data: str):
        prompt = build_prompt(input_data)
        return self.agent.invoke(prompt)
