from travel_eval.evaluators import evaluate


def test_evaluator_names_are_narrow_and_stable(faulty_run):
    names = [result.name for result in evaluate(faulty_run)]
    assert names == [
        "final_answer_quality",
        "task_outcome",
        "tool_argument_accuracy",
        "trajectory_safety",
    ]


def test_faulty_trace_produces_two_passes_and_two_failures(faulty_run):
    results = {result.name: result.passed for result in evaluate(faulty_run)}
    assert results == {
        "final_answer_quality": True,
        "task_outcome": True,
        "tool_argument_accuracy": False,
        "trajectory_safety": False,
    }
