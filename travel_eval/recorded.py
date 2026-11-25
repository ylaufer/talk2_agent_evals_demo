import json
from pathlib import Path

from .models import AgentRun, ToolCall


def load_recorded_run(path: Path) -> AgentRun:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return AgentRun(
        request=payload["request"],
        final_answer=payload["final_answer"],
        tool_calls=[ToolCall(**call) for call in payload["tool_calls"]],
        final_state=payload["final_state"],
    )

