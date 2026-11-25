"""Talk 3: metamorphic testing (ISTQB CT-AI v2.0, section 6.1.5).

Metamorphic relation: the same request, reworded, must produce the same search.
No expected value is needed: each follow-up run is compared with the source run.
    pytest -m metamorphic -v     ->  1 passed, 1 failed (on purpose)
The three runs are prepared decisions, not measurements of a live model.
"""
import pytest

from travel_eval.evaluators import search_arguments
from travel_eval.replay import replay_metamorphic_run


@pytest.mark.metamorphic
@pytest.mark.parametrize("follow_up", ["reworded", "long_paragraph"])
def test_same_request_reworded_gives_same_search(follow_up):
    source = search_arguments(replay_metamorphic_run("direct"))
    result = search_arguments(replay_metamorphic_run(follow_up))
    assert result == source


# The two tests below run in the default suite (pytest -q).

def test_source_run_passes_the_date_check():
    run = replay_metamorphic_run("direct")
    assert search_arguments(run)["date"] == run.request["date"]


def test_metamorphic_relation_separates_the_follow_up_runs():
    source = search_arguments(replay_metamorphic_run("direct"))
    same = {name: search_arguments(replay_metamorphic_run(name)) == source
            for name in ("reworded", "long_paragraph")}
    assert same == {"reworded": True, "long_paragraph": False}
