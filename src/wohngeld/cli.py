import json
import uuid
from typing import cast, Any
from pathlib import Path
from langchain_core.runnables import RunnableConfig
from wohngeld.state import WohngeldState
import logging
from wohngeld.graph import WohngeldGraphBuilder, PHASE_TWO, PHASE_THREE, PHASE_FIVE
from wohngeld.llm.generic_agent import Agent


def load_mock(mock_file: Path) -> dict[str, Any]:
    with open(mock_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def _handle_human_feedback(graph, config: RunnableConfig) -> None:
    state = graph.get_state(config)
    values = state.values
    if values.get("human_feedback_status") != "pending":
        return

    phase = values.get("human_feedback_phase", "")
    findings = []
    if phase == "phase_1_input":
        findings = values.get("input_validation_inconsistencies", [])
    elif phase == "phase_2_formal_review":
        findings = values.get("formal_inconsistencies", [])
    elif phase == "phase_3_material_review":
        findings = values.get("material_review_notes", [])

    if findings:
        print("\nRueckfragen/Findings:")
        for item in findings:
            print(f"- {item}")

    decision = input("Menschliches Feedback (P=positiv, N=negativ): ").strip().upper()
    if decision == "N":
        graph.update_state(
            config,
            {
                "human_feedback_status": "negative",
                "final_decision": "Rejected",
                "disqualification_reason": "Negatives menschliches Feedback",
            },
        )
        return

    interpretation = input("Interpretationshilfe (optional): ").strip()
    graph.update_state(
        config,
        {
            "human_feedback_status": "positive",
            "human_feedback_phase": "",
            "interpretation_context": interpretation,
        },
    )


def run_cli():
    print("=== Wohngeld LangGraph Workflow ===")

    graph = WohngeldGraphBuilder().build()
    initial_state = cast(WohngeldState, {})

    config = cast(
        RunnableConfig,
        {"configurable": {"thread_id": f"cli_thread_{uuid.uuid4().hex[:8]}"}},
    )

    logging.basicConfig(level=logging.INFO)
    print("\nStart Workflow...")
    while True:
        for event in graph.stream(initial_state, config):
            for key, value in event.items():
                print(f"Node execution: {key}")

        initial_state = None

        state = graph.get_state(config)

        if not state.next:
            print("Workflow beendet.")
            break

        next_node = state.next[0]

        if state.values.get("human_feedback_status") == "pending":
            _handle_human_feedback(graph, config)
            state = graph.get_state(config)
            if not state.next:
                continue
            next_node = state.next[0]

        if next_node == PHASE_TWO:  # Pause vor Phase 2
            print("\n[Halt] Formale Pruefung startet gleich.")
            input("Druecken Sie Enter, um fortzufahren...")

        if next_node == PHASE_THREE:  # Pause vor Phase 3
            print("\n[Halt] Materielle Pruefung startet gleich.")
            input("Druecken Sie Enter, um fortzufahren...")

        elif next_node == PHASE_FIVE:  # Pause nach Phase 4
            decision_state = state.values.get("final_decision", "")
            if decision_state == "Rejected":
                print("\n[Halt] Vorgang ist abgelehnt. Review wird dokumentiert.")
                graph.update_state(config, {"human_approved": True})
                continue

            benefit = state.values.get("calculated_benefit", 0)
            print(f"\n[Halt] Berechnetes Wohngeld: {benefit} EUR.")
            decision = input("Entscheidung freigeben? (Y/N): ")

            if decision.strip().upper() == "Y":
                print("Freigabe erteilt.")
                graph.update_state(
                    config, {"human_approved": True, "final_decision": "Approved"}
                )
            else:
                print("Abgelehnt durch Pruefer.")
                graph.update_state(
                    config,
                    {
                        "human_approved": True,
                        "final_decision": "Rejected",
                        "disqualification_reason": "Manuell abgelehnt",
                    },
                )


if __name__ == "__main__":
    run_cli()
