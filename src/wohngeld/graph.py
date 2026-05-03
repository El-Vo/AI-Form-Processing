from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from wohngeld.state import WohngeldState
from wohngeld.phases.input.input import Input
from wohngeld.phases.formal_review.formal_review import FormalReview
from wohngeld.phases.material_review.material_review import MaterialReview
from wohngeld.phases.decision.decision import Decision
from wohngeld.phases.notification.notification import Notification
from wohngeld.phases.archive.archive import Archive

PHASE_ONE = "Phase 1 - Input"
PHASE_TWO = "Phase 2 - Formal Review"
PHASE_THREE = "Phase 3 - Material Review"
PHASE_FOUR = "Phase 4 - Decision"
PHASE_FIVE = "Phase 5 - Notification"
PHASE_SIX = "Phase 6 - Archive"


def check_input_validation(state: WohngeldState) -> str:
    if state.get("human_feedback_status") == "negative":
        return PHASE_FIVE
    if state.get("input_validation_needs_human", False):
        return PHASE_TWO
    return PHASE_TWO


def check_formal_review(state: WohngeldState) -> str:
    if state.get("human_feedback_status") == "negative":
        return PHASE_FIVE
    if not state.get("is_formally_valid", False):
        return PHASE_FIVE
    return PHASE_THREE


def check_material_review(state: WohngeldState) -> str:
    if state.get("human_feedback_status") == "negative":
        return PHASE_FIVE
    if not state.get("is_materially_valid", False):
        return PHASE_FIVE
    return PHASE_FOUR


class WohngeldGraphBuilder:
    def build(self):
        builder = StateGraph(WohngeldState)

        builder.add_node(PHASE_ONE, Input())
        builder.add_node(PHASE_TWO, FormalReview())
        builder.add_node(PHASE_THREE, MaterialReview())
        builder.add_node(PHASE_FOUR, Decision())
        builder.add_node(PHASE_FIVE, Notification())
        builder.add_node(PHASE_SIX, Archive())

        builder.add_edge(START, PHASE_ONE)
        builder.add_conditional_edges(
            PHASE_ONE,
            check_input_validation,
            {
                PHASE_TWO: PHASE_TWO,
                PHASE_FIVE: PHASE_FIVE,
            },
        )

        builder.add_conditional_edges(
            PHASE_TWO,
            check_formal_review,
            {
                PHASE_THREE: PHASE_THREE,
                PHASE_FIVE: PHASE_FIVE,
            },
        )

        builder.add_conditional_edges(
            PHASE_THREE,
            check_material_review,
            {
                PHASE_FOUR: PHASE_FOUR,
                PHASE_FIVE: PHASE_FIVE,
            },
        )

        builder.add_edge(PHASE_FOUR, PHASE_FIVE)
        builder.add_edge(PHASE_FIVE, PHASE_SIX)
        builder.add_edge(PHASE_SIX, END)

        memory = MemorySaver()
        return builder.compile(
            checkpointer=memory,
            interrupt_before=[PHASE_TWO, PHASE_THREE],
            interrupt_after=[PHASE_FOUR],
        )
