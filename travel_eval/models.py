from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ToolCall:
    name: str
    arguments: dict[str, Any]
    result: dict[str, Any]


@dataclass(frozen=True)
class AgentRun:
    request: dict[str, Any]
    final_answer: str
    tool_calls: list[ToolCall]
    final_state: dict[str, Any] = field(default_factory=dict)

