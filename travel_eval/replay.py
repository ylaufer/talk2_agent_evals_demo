"""Replay recorded agent decisions against the current tools.

A recorded run stores what the agent decided (tool calls + final answer), not
what the tools returned. Replaying it executes those decisions again, so a new
control in tools.py shows up in the trace and in the final state.
"""
import json
from pathlib import Path

from . import tools
from .models import AgentRun, ToolCall

INJECTION_RUNS = Path(__file__).resolve().parent.parent / "data" / "injection_runs"
RESILIENCE_RUNS = Path(__file__).resolve().parent.parent / "data" / "resilience_runs"
METAMORPHIC_RUNS = Path(__file__).resolve().parent.parent / "data" / "metamorphic_runs"


def load_decisions(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def replay(decisions: dict, inject: bool = True, search_down: bool = False) -> AgentRun:
    tools.reset(inject=inject, search_down=search_down)
    calls = []
    for step in decisions["tool_calls"]:
        try:
            result = tools.TOOLS[step["name"]](**step["arguments"])
        except (tools.ToolRefused, tools.ToolUnavailable) as exc:
            result = {"error": type(exc).__name__, "message": str(exc)}
        calls.append(ToolCall(step["name"], step["arguments"], result))
    return AgentRun(
        request=decisions["request"],
        final_answer=decisions["final_answer"],
        tool_calls=calls,
        final_state=dict(tools.state),
    )


def replay_injection_run(index: int) -> AgentRun:
    path = INJECTION_RUNS / f"run_{index:02d}.json"
    if not path.exists():
        raise FileNotFoundError(f"No recorded injection run {index}. There are 10; use --count 10 or --live.")
    return replay(load_decisions(path))


def replay_resilience_run(name: str) -> AgentRun:
    """Prepared decisions for a run where the search tool is down."""
    return replay(load_decisions(RESILIENCE_RUNS / f"{name}.json"), inject=False, search_down=True)


def replay_metamorphic_run(name: str) -> AgentRun:
    """Prepared decisions for one wording of the same request (see the "prompt" field in the file)."""
    return replay(load_decisions(METAMORPHIC_RUNS / f"{name}.json"), inject=False)
