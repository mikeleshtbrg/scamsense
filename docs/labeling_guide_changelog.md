# Labeling guide: change log

Every change to `labeling_guide.md` is recorded here, newest first. Each entry says what changed and why. Update this file in the same commit as the guide.

## v0.2 — 2026-11-25

**Placeholders**

- The player we warn is now `<USER_WARN>`. All other participants are `<USER_1>`, `<USER_2>`, … in order of first appearance; the same person keeps the same number, including when the account name appears inside a message.
- Added `<LINK_CHECK>` for a link that cannot be classified as official or lookalike (dead, shortened, not verifiable at transcription time). Synthetic chats never use it.
- Why: `<USER_1>` for the potential victim was ambiguous once a chat has more than two participants.

**Link rule (new, §5)**

- Staff claim + `<LINK_LOOKALIKE>` → `fake_support` immediately.
- Staff claim + `<LINK_OFFICIAL>` → may be a real representative, so the link alone does not make it `fake_support`. A request for items, codes or credentials does.
- `<LINK_CHECK>` → label the best guess, add `needs_check` to `notes`, review together before computing κ.
- Why: the right label depends on the link, and an official link can belong to a real representative.

**Hook (§3)**

- The hook is the first message with the main harmful request (send an item, open a link, share a code, add a "middleman" or "rep"), not the first suspicious claim. Earlier lures are not the hook.
- `item_swap`: if the swap appears only as an `[EVENT]`, the hook is the first message after it that pushes to confirm.
- Why: the real scam example in the proposal puts the hook at message 9, after lures in messages 1 and 3.

**Classes (§2)**

- Class names and definitions aligned with the proposal, and each class now has its family ("during a trade" or "account theft").
- `fake_support` vs `phishing` vs `impersonation` clarified: a hacked real account that sends a staff lure is labeled by the hook; `impersonation` means a copy of a private person's profile.
- Added: the words "scam", "fraud" or "fake" in the text never decide the label.

**Tricky `legit` examples (§6)**

- Replaced with three cases that match the tricky legit subtypes in the data design: honest urgency with an official link, official middleman, hard bargaining.

**Privacy (§5)**

- Stated where raw real chats live (`data/raw/real/`, ignored by git) and where anonymized samples go (`data/samples/`).

**Multi-scam chats (§4)**

- One primary label: the scam type of the hook. If the hook fits two types, the one that would cause the loss first. The second type goes into `notes`.

## v0.1 — 2026-11-25

First draft: one definition and decision rule per class, hook definition, multi-scam rule, placeholders, tricky legit examples, labeling process.
