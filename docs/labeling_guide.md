# Labeling Guide

How we label trading chats, real and synthetic. Two annotators label every chat independently, we compute Cohen's κ, and then we settle disagreements using this guide.

## 1. What we label

For every chat:

- `label`: exactly one of the 7 classes in §2.
- `hook_msg`: the 1-based index of the hook message (§3). `null` for `legit`.
- `notes`: optional. Use it for a second scam type (§4), a `<LINK_CHECK>` link (§5), or any doubt.

Label from the chat text and the `[EVENT]` lines only. Do not use outside knowledge about the people involved, and do not look at any automatic label before you decide.

## 2. The 7 classes

Each class has a one-line definition and a decision rule ("if X, it is Y"). The names match the proposal.

| Class | Family | Definition | Decision rule |
|---|---|---|---|
| `legit` | none | An ordinary trade where nobody tries to cause the other side a loss. | If every request is something an honest trader could ask, and the trade can finish with both sides getting what was agreed, it is `legit`, however pushy or sloppy the tone. |
| `fake_middleman` | during a trade | The "trusted" middleman is the scammer's second account or an accomplice. | If the other side proposes a middleman who is not sanctioned by the platform or server (`<LINK_OFFICIAL>`), and the victim must send an item or currency to or through them, it is `fake_middleman`. |
| `fake_payment` | during a trade | A forged payment proof (for example a fake PayPal screenshot) so the seller sends first. | If the scammer says money was sent, shows a screenshot or receipt, and asks for the item (or a refund or change) before the victim can verify the payment, it is `fake_payment`. |
| `item_swap` | during a trade | The offer changes to a cheaper or different item right before confirmation. | If the item in the trade window differs from the item agreed in the chat, and the chat pushes toward a quick confirm, it is `item_swap`. |
| `phishing` | account theft | A link meant to steal the account: "vote for my team", free gift cards, fake trade sites. | If the scammer pushes a link to `<LINK_LOOKALIKE>` and does not claim to be staff or a specific person, it is `phishing`. |
| `impersonation` | account theft | A copy of a friend's or teammate's profile. | If the scammer's account imitates a specific person the victim knows (same name or avatar, a new or lookalike account) and uses that trust to ask for something, it is `impersonation`. |
| `fake_support` | account theft | A fake admin or support: "I reported you by mistake, talk to the admin". | If the sender claims to act for the game, the platform or its staff, and the link in the request is a `<LINK_LOOKALIKE>`, it is `fake_support`. See the link rule in §5. |

### Confusable pairs

- `fake_support` vs `impersonation`: a claim to be official staff is `fake_support`; a copy of a private person's profile is `impersonation`. A real friend's account that was hacked and now sends a staff lure is labeled by the hook (usually `fake_support`).
- `fake_support` vs `phishing`: staff claim plus lookalike link is `fake_support`. A lookalike link with no staff or person claim is `phishing`.
- `fake_middleman` vs `fake_support`: a third party who holds the trade is `fake_middleman`; staff who "fix an account problem" is `fake_support`.
- `fake_payment` vs `phishing`: a fake receipt inside the chat is `fake_payment`; a link to a fake payment page is `phishing`.
- The words "scam", "fraud" or "fake" in the text do not decide the label. In 10% of chats of every class someone asks "is this a scam?". Label by the requests.

## 3. The hook

The **hook** is the first message that contains the main harmful request: send an item, open a link, share a code, add a "middleman" or "rep".

- Earlier lures are not the hook. "It's a very important matter" and "I reported you by mistake" are lures. The hook is the later message with the link to the fake "Steam rep".
- The hook is the request, not the moment of loss.
- Friendly talk, haggling and general offers are not a hook.
- If the same request is made twice, the hook is the first one.
- Messages are numbered from 1. `[EVENT]` lines are not messages and are not numbered.
- For `item_swap`, if the swap shows up only as an `[EVENT]`, the hook is the first message after it that pushes to confirm.
- If two annotators differ by one message, settle it with this rule. Do not average.

## 4. Chats with several scam types

Each chat gets **one primary label**: the scam type of its main harmful request, which is the hook.

- If the hook itself fits two types, pick the one whose step would cause the loss first.
- Later scam moves do not change the label.
- Write the second type in `notes`, so we can count how often it happens.

## 5. Placeholders and anonymization

Real chats are anonymized before anything is saved or shared. Raw real chats are never committed (`data/raw/real/` is in `.gitignore`); only anonymized samples go into `data/samples/`. The same placeholders are used in synthetic chats.

Format: one line per message, `<USER_WARN>: text`. Trade events go on their own line right after the message where they happened, for example `[EVENT] friend_request sender=other account_age=new`. Event types and allowed values are defined in [`event_format.md`](event_format.md). If a real report shows no events, the chat has no `[EVENT]` lines.

| Placeholder | Use |
|---|---|
| `<USER_WARN>` | The player we warn: the potential victim ("you" in the proposal examples). |
| `<USER_1>`, `<USER_2>`, … | Everyone else, numbered in order of first appearance. The same person keeps the same number, including when their account name appears inside a message. |
| `<LINK_OFFICIAL>` | A link to the real official site, market, listing or staff profile of the game or platform. |
| `<LINK_LOOKALIKE>` | A link that imitates an official one: typos, extra words, another top-level domain, a lookalike subdomain, a fake trade site. |
| `<LINK_CHECK>` | A link we cannot tell apart: dead, shortened, or not verifiable at transcription time. |

Remove or replace: account names, real names, Discord/Steam/platform IDs, emails, phone numbers, avatars. Keep item names, prices, the game and the platform, because they are not personal data.

**Link rule.** When the label depends on a link:

- `<LINK_LOOKALIKE>` with a staff claim: label `fake_support` immediately.
- `<LINK_OFFICIAL>` with a staff claim: it may be a real representative. Do not label `fake_support` from the link alone. If the sender also asks for items, codes or credentials, it is `fake_support`; if not, label by the rest of the chat (usually `legit`).
- `<LINK_CHECK>`: label your best guess and add `needs_check` to `notes`. These chats are reviewed together before we count κ.

Before using `<LINK_CHECK>` on a real chat, try to verify the domain. Synthetic chats never use `<LINK_CHECK>`, because the generator decides the link type.

## 6. Tricky `legit` examples

All three look suspicious and are `legit`. They match the tricky legit subtypes in the data design.

1. **Honest urgency with an official link.** `<USER_1>` writes "hurry, the price is going up in 10 minutes" and pastes `<LINK_OFFICIAL>` to the market listing. The pressure is real, but nothing is asked that could cost `<USER_WARN>` anything, and the trade finishes in the game's own window.
2. **Official middleman.** `<USER_1>` suggests the server's official middleman from the published list (`<LINK_OFFICIAL>`). A third party is involved, but it is sanctioned by the server. Compare `fake_middleman`, where the middleman is an unverified account the other side brings.
3. **Hard bargaining.** `<USER_1>` lowballs, refuses to go first, and says "this feels like a scam, prove it's your item". The tone is hostile and uses scam words, but every request is one an honest trader can make, and nobody tries to cause a loss.

## 7. Process

1. Both annotators label every chat alone, without seeing each other's labels.
2. Compute Cohen's κ, per class and overall, before discussing anything.
3. Go through each disagreement and settle it by this guide. If the guide does not settle it, decide together and add the rule here.
4. Test chats are never used to choose prompts or few-shot examples.
