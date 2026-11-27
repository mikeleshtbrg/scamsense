# Trade Event Format (`[EVENT]`)

Trade events are things that happen in the platform's trade system, not in the chat text: a friend request, a trade offer, an offer that changes. The model reads them together with the messages. This file defines how they are written. The same format is used in synthetic chats and in real chats; the labeling guide ([`labeling_guide.md`](labeling_guide.md)) refers to these lines without defining them.

## 1. The line

```
[EVENT] <type> key=value key=value
```

- One event per line, on its own line.
- The line goes **right after the message where the event happened**. An event that happened before the first message goes above message 1.
- `[EVENT]` lines are not messages: they are not numbered and never count toward the hook index.
- Keys are written in the order of the table in §2. Every key of the type is required.
- Values are **categorical only**: lower-case words from the table. No numbers, prices, dates, names or free text (write `account_age=new`, never `account_age=2_days`).
- Parsing and validation: `src/data/events.py` (`parse_event`, `format_event`, `render_chat`, `split_chat`).

## 2. Types and allowed values

| Type | Key | Allowed values | Meaning |
|---|---|---|---|
| `friend_request` | `sender` | `partner`, `other` | `partner` = the person `<USER_WARN>` is chatting with; `other` = a third account (for example a "middleman" or a "support rep"). |
| | `account_age` | `new`, `old` | Whether the sending account looks newly created. |
| `trade_offer` | `sender` | `partner`, `warn` | Who opened the offer in the trade window: the partner, or `<USER_WARN>`. |
| | `value` | `low`, `mid`, `high` | Value category of the items in the offer. |
| `trade_offer_changed` | `old_value` | `low`, `mid`, `high` | Value category before the change. |
| | `new_value` | `low`, `mid`, `high` | Value category after the change. |

`trade_offer_changed` is needed to recognize `item_swap`: the swap often shows up only in the trade window. By the labeling guide, if the swap appears only as an event, the hook is the first message after it that pushes to confirm. A change with `new_value` equal to `old_value` means a different item of the same value category.

## 3. Example

```
[EVENT] friend_request sender=partner account_age=old
<USER_1>: u still selling the AK Redline? 25$ ok?
<USER_WARN>: ya deal
<USER_1>: lets use a middleman so its safe. add <USER_2>
[EVENT] friend_request sender=other account_age=new
<USER_WARN>: ok added
```

Message 3 is the hook (`fake_middleman`); the event after it does not change the numbering.

## 4. Synthetic vs real chats

- **Synthetic chats.** Events are built in code from the sampled config (`src/data/sample_configs.py`), never written by the LLM. The generator receives the planned events with their message positions and writes messages that fit them; the `[EVENT]` lines are then inserted by `render_chat`. Event cues that point to a scam also appear in some legit chats (a new account, an honest offer change, chats with no offer), so the events alone do not give away the label. The rates are in `configs/attribute_space.yaml`.
- **Real chats.** When a report or screenshot shows an event (a friend request, the trade window, an offer change), the transcriber writes the matching `[EVENT]` line after the message where it appears. **If a real report does not show any events, the chat has no `[EVENT]` lines.** Do not infer events that are not shown.
- If something is visible but its value cannot be told (for example the account age is not shown), leave the event out rather than guess a value.

## 5. Changing the format

Adding a type, key or value means changing `EVENT_SCHEMA` in `src/data/events.py`, this file, and the tests in `tests/test_events.py` together. Configs sampled before the change must be regenerated.
