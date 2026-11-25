"""Talk 3, "Trusting the gate": the evaluation pipeline is also a system under test.

render_for_judge turns a run into the text an LLM judge reads. validate_packet
checks that the evidence survived. evaluate_with_judge refuses to call the judge
when it did not. legacy_render_for_judge reproduces the bug from Xia et al.
(Nov 2026): a renderer that silently drops structured tool calls.
"""
import json
from typing import Any, Callable

from .models import AgentRun


class EvaluationInputError(Exception):
    """The packet for the judge is missing evidence. The judge must not run."""


def _dump(value: Any) -> str:
    return json.dumps(value, sort_keys=True)


def render_for_judge(run: AgentRun) -> str:
    lines = [f"REQUEST: {_dump(run.request)}"]
    for i, call in enumerate(run.tool_calls, start=1):
        lines.append(f"TOOL CALL {i}: {call.name} {_dump(call.arguments)}")
        lines.append(f"TOOL RESULT {i}: {_dump(call.result)}")
    lines.append(f"FINAL ANSWER: {run.final_answer}")
    return "\n".join(lines)


def legacy_render_for_judge(run: AgentRun) -> str:
    """The buggy version: only the conversation text survives."""
    return f"REQUEST: {_dump(run.request)}\nFINAL ANSWER: {run.final_answer}"


def validate_packet(run: AgentRun, packet: str) -> None:
    for i, call in enumerate(run.tool_calls, start=1):
        expected = (f"TOOL CALL {i}: {call.name} {_dump(call.arguments)}",
                    f"TOOL RESULT {i}: {_dump(call.result)}")
        for line in expected:
            if line not in packet:
                raise EvaluationInputError(f"Missing from judge packet: {line}")


def evaluate_with_judge(run: AgentRun, judge: Callable[[str], Any],
                        renderer: Callable[[AgentRun], str] = render_for_judge) -> Any:
    packet = renderer(run)
    validate_packet(run, packet)   # a failed check stops the pipeline
    return judge(packet)           # the judge reads exactly the validated bytes
