"""Talk 3, slide "Trusting the gate": test the evaluation pipeline, not only the agent.

These run in the default suite (pytest -q).
"""
from unittest.mock import Mock

import pytest

from travel_eval.judge_packet import (EvaluationInputError, evaluate_with_judge,
                                      legacy_render_for_judge, render_for_judge)


def test_renderer_preserves_structured_tool_call(faulty_run):
    packet = render_for_judge(faulty_run)
    assert "search_flights" in packet
    assert '"date": "2026-11-19"' in packet


def test_every_tool_call_has_a_result(faulty_run):
    assert all(call.result for call in faulty_run.tool_calls)


def test_invalid_packet_never_reaches_judge(faulty_run):
    judge = Mock()
    with pytest.raises(EvaluationInputError):
        evaluate_with_judge(faulty_run, judge, renderer=legacy_render_for_judge)
    judge.assert_not_called()


def test_valid_packet_reaches_judge_unchanged(faulty_run):
    judge = Mock(return_value="RISKY")
    assert evaluate_with_judge(faulty_run, judge) == "RISKY"
    judge.assert_called_once_with(render_for_judge(faulty_run))
