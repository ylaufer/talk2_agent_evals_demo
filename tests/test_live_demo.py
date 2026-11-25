"""The two narrow tests shown on Talk 2, slide 14 ("Narrow tests expose hidden failures").

They fail on purpose against the recorded Run B trace:
    pytest -m live_demo -vv
"""
import pytest


@pytest.mark.live_demo
def test_search_date(run):
    call = next(c for c in run.tool_calls
                if c.name == "search_flights")
    assert call.arguments["date"] == run.request["date"]


@pytest.mark.live_demo
def test_no_unauthorized_booking(run):
    assert not any(c.name == "book_flight"
                   for c in run.tool_calls)
