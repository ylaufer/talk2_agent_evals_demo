"""Talk 3, test strategy: resilience tests. The search tool is down.

Does the agent ask the user, or does it invent a flight? Two prepared runs:
    pytest -m resilience -v     ->  1 passed, 1 failed (on purpose)
"""
import pytest

from travel_eval.evaluators import answer_is_grounded
from travel_eval.replay import replay_resilience_run


@pytest.mark.resilience
@pytest.mark.parametrize("name", ["asks_user", "invents_flight"])
def test_agent_does_not_invent_when_search_fails(name):
    run = replay_resilience_run(name)
    result = answer_is_grounded(run)
    assert result.passed, result.evidence


# The two tests below run in the default suite (pytest -q).

def test_search_failure_is_recorded_in_the_trace():
    run = replay_resilience_run("asks_user")
    assert run.tool_calls[0].result["error"] == "ToolUnavailable"


def test_grounding_evaluator_separates_the_two_runs():
    verdicts = {name: answer_is_grounded(replay_resilience_run(name)).passed
                for name in ("asks_user", "invents_flight")}
    assert verdicts == {"asks_user": True, "invents_flight": False}
