"""Trade-event format shared by synthetic and real chats.

One event = one line, placed right after the message where it happened:

    [EVENT] <type> key=value key=value

Values are categorical only (no numbers, no free text). See docs/event_format.md.
"""

from __future__ import annotations

import re

EVENT_PREFIX = "[EVENT]"

# type -> {key: allowed values}. Every key is required.
EVENT_SCHEMA: dict[str, dict[str, tuple[str, ...]]] = {
    "friend_request": {
        "sender": ("partner", "other"),
        "account_age": ("new", "old"),
    },
    "trade_offer": {
        "sender": ("partner", "warn"),
        "value": ("low", "mid", "high"),
    },
    "trade_offer_changed": {
        "old_value": ("low", "mid", "high"),
        "new_value": ("low", "mid", "high"),
    },
}

_TOKEN = re.compile(r"^([a-z_]+)=([a-z_]+)$")


class EventFormatError(ValueError):
    """An event does not follow the [EVENT] format."""


def validate_event(event_type: str, attrs: dict[str, str]) -> None:
    if event_type not in EVENT_SCHEMA:
        raise EventFormatError(f"unknown event type: {event_type!r}")
    schema = EVENT_SCHEMA[event_type]
    missing = set(schema) - set(attrs)
    extra = set(attrs) - set(schema)
    if missing or extra:
        raise EventFormatError(
            f"{event_type}: missing keys {sorted(missing)}, unknown keys {sorted(extra)}"
        )
    for key, value in attrs.items():
        if value not in schema[key]:
            raise EventFormatError(
                f"{event_type}: {key}={value!r} not in {list(schema[key])}"
            )


def format_event(event_type: str, attrs: dict[str, str]) -> str:
    """Return the [EVENT] line. Keys are written in schema order."""
    validate_event(event_type, attrs)
    pairs = " ".join(f"{k}={attrs[k]}" for k in EVENT_SCHEMA[event_type])
    return f"{EVENT_PREFIX} {event_type} {pairs}"


def is_event_line(line: str) -> bool:
    return line.strip().startswith(EVENT_PREFIX)


def parse_event(line: str) -> tuple[str, dict[str, str]]:
    """Parse one [EVENT] line into (type, attrs). Raises EventFormatError."""
    parts = line.strip().split()
    if len(parts) < 2 or parts[0] != EVENT_PREFIX:
        raise EventFormatError(f"not an event line: {line!r}")
    event_type, attrs = parts[1], {}
    for token in parts[2:]:
        m = _TOKEN.match(token)
        if not m:
            raise EventFormatError(f"bad token {token!r} in {line!r}")
        if m.group(1) in attrs:
            raise EventFormatError(f"duplicate key {m.group(1)!r} in {line!r}")
        attrs[m.group(1)] = m.group(2)
    validate_event(event_type, attrs)
    return event_type, attrs


def render_chat(messages: list[str], events: list[dict]) -> str:
    """Interleave messages and events into chat text.

    messages: lines like "<USER_WARN>: text", in order (message 1 is messages[0]).
    events: dicts with "after_msg" (0 = before message 1), "type", "attrs".
    Events with the same after_msg keep their list order.
    """
    by_msg: dict[int, list[str]] = {}
    for ev in events:
        n = ev["after_msg"]
        if not 0 <= n <= len(messages):
            raise EventFormatError(f"after_msg={n} outside 0..{len(messages)}")
        by_msg.setdefault(n, []).append(format_event(ev["type"], ev["attrs"]))
    lines = list(by_msg.get(0, []))
    for i, msg in enumerate(messages, start=1):
        lines.append(msg)
        lines.extend(by_msg.get(i, []))
    return "\n".join(lines)


def split_chat(text: str) -> tuple[list[str], list[dict]]:
    """Inverse of render_chat: chat text -> (messages, events)."""
    messages: list[str] = []
    events: list[dict] = []
    for line in text.splitlines():
        if not line.strip():
            continue
        if is_event_line(line):
            event_type, attrs = parse_event(line)
            events.append({"after_msg": len(messages), "type": event_type, "attrs": attrs})
        else:
            messages.append(line)
    return messages, events
