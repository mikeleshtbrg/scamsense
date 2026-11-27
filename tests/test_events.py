"""[EVENT] line format. Run: python -m pytest"""

import pytest

from src.data.events import EventFormatError, format_event, parse_event, render_chat, split_chat


def test_format_and_parse_round_trip():
    line = format_event("friend_request", {"account_age": "new", "sender": "other"})
    assert line == "[EVENT] friend_request sender=other account_age=new"
    assert parse_event(line) == ("friend_request", {"sender": "other", "account_age": "new"})


@pytest.mark.parametrize("line", [
    "[EVENT] friend_request sender=other",                      # missing key
    "[EVENT] friend_request sender=other account_age=2_days",   # value not allowed
    "[EVENT] friend_request sender=other account_age=new x=y",  # unknown key
    "[EVENT] gift_sent value=high",                             # unknown type
    "[EVENT] trade_offer sender=partner value=25",              # number
    "EVENT trade_offer sender=partner value=low",               # no prefix
])
def test_bad_lines_rejected(line):
    with pytest.raises(EventFormatError):
        parse_event(line)


def test_render_and_split_round_trip():
    messages = [
        "<USER_1>: u still selling the AK Redline?",
        "<USER_WARN>: ya, 25$",
        "<USER_1>: lets use a middleman, add <USER_2>",
    ]
    events = [
        {"after_msg": 0, "type": "friend_request", "attrs": {"sender": "partner", "account_age": "old"}},
        {"after_msg": 3, "type": "friend_request", "attrs": {"sender": "other", "account_age": "new"}},
    ]
    text = render_chat(messages, events)
    assert text.splitlines()[0].startswith("[EVENT]")
    assert text.splitlines()[-1] == "[EVENT] friend_request sender=other account_age=new"
    assert split_chat(text) == (messages, events)


def test_chat_without_events():
    messages = ["<USER_1>: hi", "<USER_WARN>: hey"]
    assert split_chat(render_chat(messages, [])) == (messages, [])
