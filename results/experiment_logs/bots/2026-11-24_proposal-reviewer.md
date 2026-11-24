# Proposal Reviewer log

Log of the course bot's review of our proposal deck, and of what we changed or decided in response. This file records errors and changes only; it is not a copy of the bot's output.

| Field | Value |
|---|---|
| Date | 2026-11-24 |
| Bot | Course Proposal Reviewer (ChatGPT custom GPT) |
| Reviewed | ScamSense - Project Proposal 10 (PDF, 14 slides) |
| Compared against | ScamSense - Project Proposal 11 (PPTX, 14 slides), text and speaker notes |
| Bot verdict | Significant revision required |
| Next bot run | None planned before upload |

## Status legend

| Status | Meaning |
|---|---|
| FIXED | Change is visible in Proposal 11 |
| PARTIAL | Some of the comment is addressed; the gap is stated |
| OPEN | Not addressed in Proposal 11; candidate for the next edit |
| DEFERRED | Intentionally postponed (midterm or generation run) |
| REJECTED | Not acted on, with the reason |

## Summary

| Status | Count |
|---|---|
| FIXED | 14 |
| PARTIAL | 15 |
| OPEN | 11 |
| DEFERRED | 9 |
| REJECTED | 5 |
| Total | 54 |

The bot's three headline concerns and where they stand:

1. Real test set independence: FIXED (S10-2). Written-by-us chats are a separate subset and main results use public chats only. Test-set size (S10-1) is deferred.
2. Synthetic data may not generalize to real chats: PARTIAL. The real test set is the answer by design; judge-bias and seed-leakage checks (S9-2, S9-5) are still OPEN.
3. Early-warning evaluation precision: FIXED (S12-2, S12-4, S12-5), with one residual wording issue (S12-1).

## Comment-by-comment log

Severity is the bot's own label, kept for traceability. It is not our priority.

| ID | Slide | Bot severity | Comment | Status | Change in v11 / decision |
|---|---|---|---|---|---|
| S1-1 | 1 | Minor | Opening example implies a prediction after message 3 without saying it is illustrative | REJECTED | Cosmetic; speaker notes already present it as the intended behavior |
| S2-1 | 2 | Major | The four statistics measure different things | FIXED | v11 adds a line stating what each number measures (malware attacks, phishing-brand ranking, one account-theft case, Danish trade-scam victims) |
| S2-2 | 2 | Major | "Current protections do not read the whole conversation" is unsupported | FIXED | v11 names the protections (trade holds, link warnings, keyword bots, user reports) and softens to "we found none" |
| S2-3 | 2 | Moderate | $5B skin market is indirect evidence for the task | PARTIAL | Kept as context for why items are worth stealing; the clarification line states the stats are not prevalence evidence |
| S3-1 | 3 | Major | Scam categories overlap; no primary-label rule | FIXED | v11 adds the label rule: one primary label = scam type of the main harmful request (the hook) |
| S3-2 | 3 | Moderate | Unclear if all classes have enough authentic examples | FIXED | Covered on slide 10: fewer than 10 public examples for a type are filled with our own written chats and reported separately |
| S3-3 | 3 | Minor | Transaction vs account-theft families not defined | PARTIAL | Each card carries a family tag (DURING A TRADE / ACCOUNT THEFT); no separate one-line definition |
| S4-1 | 4 | Moderate | "Enough time to warn" is an assumption, not a result | OPEN | Slide text unchanged in v11; candidate wording: "potential early-warning window" |
| S4-2 | 4 | Moderate | Source is a 2020 community guide, not a representative dataset | PARTIAL | Source line names the guide and year; the word "illustrative" is not added |
| S4-3 | 4 | Minor | Screenshot hard to read | DEFERRED | Visual polish, not verifiable from text; do if time remains |
| S5-1 | 5 | Major | Relationship between messages, events and prediction moment unspecified | FIXED | v11 adds "KNOWN AT MESSAGE t: only messages and trade events up to t, never later ones" |
| S5-2 | 5 | Major | No confidence or alert threshold defined | FIXED | Slide 12: alert threshold is picked on synthetic validation only |
| S5-3 | 5 | Moderate | Intended users too broad (players vs moderators) | OPEN | Slide still lists both as users |
| S6-1 | 6 | Critical | "First labeled dataset" is not demonstrated | FIXED | v11 reads "we found no public one" instead of a priority claim |
| S6-2 | 6 | Major | "Small trained models beat large LLMs" is too broad | OPEN | Unchanged; qualify or tie to the specific cited papers |
| S6-3 | 6 | Major | Original vs reused contributions not separated | PARTIAL | Slide has an ALREADY DONE / WHAT WE ADD split; reused methods (generation, models) are not listed as reused |
| S6-4 | 6 | Major | Add a related-work comparison table | DEFERRED | Only after the papers themselves are read; the bot marked several cells "Verify" |
| S7-1 | 7 | Major | Selection and diversity of the 25 seed chats unspecified | PARTIAL | Slide 10 lists the sources; no per-class counts or selection criteria yet |
| S7-2 | 7 | Major | No planned breakdown for ~6,000 raw to ~5,000 kept | DEFERRED | Per-filter rejection counts will be reported from the actual run; v11 makes 6,000 configs / ~6,000 raw / ~5,000 kept consistent |
| S7-3 | 7 | Moderate | Few-shot selection criteria unclear | PARTIAL | v11 states 3 rounds x 10 chats per class, keep best 2 per class; who selects and on what criteria is not stated |
| S7-4 | 7 | Moderate | No fallback if Azure credit fails | REJECTED | Azure budget was computed and is enough for the whole project (decision 2026-11-24) |
| S8-1 | 8 | Critical | No constraint matrix for valid attribute combinations | DEFERRED | To do before the full generation run (step 3), not necessarily before proposal upload |
| S8-2 | 8 | Major | Legit vs fraudulent official middleman / official link not operationalized | DEFERRED | Same work item as S8-1 |
| S8-3 | 8 | Major | 40% legit / 10% per class may not match deployment | REJECTED | Distribution is for training; false-alarm rate is measured separately on real legit chats |
| S8-4 | 8 | Moderate | Item value (low/mid/high) not operationalized | PARTIAL | v11 states it is a category, never a price |
| S9-1 | 9 | Critical | Cohen's kappa: adjudication order unspecified | FIXED | v11: kappa computed before disagreements are settled; kappa < 0.7 means fix that prompt |
| S9-2 | 9 | Major | LLM judge may share the generator's assumptions; needs blind audit of accepted and rejected chats | OPEN | 210-chat human sample exists; auditing rejected chats is not planned on the slide |
| S9-3 | 9 | Major | TF-IDF macro-F1 > 0.95 treated as automatic proof of leakage | OPEN | Unchanged; should be a diagnostic trigger followed by inspecting feature weights and errors |
| S9-4 | 9 | Major | Config group undefined | FIXED | v11: config group = label + game + scammer tactic |
| S9-5 | 9 | Major | Indirect leakage via shared few-shot seeds or prompt templates | OPEN | Not addressed in v11 |
| S9-6 | 9 | Moderate | Selection strategy of the 210-chat human sample | OPEN | 30 per class stated; stratified-random selection and split coverage not stated |
| S10-1 | 10 | Critical | ~140 real chats, 15 per scam class, too few for per-class conclusions | DEFERRED | Scope decision with Vered; v11 adds a fallback rule and CIs, and per-class results should be called exploratory |
| S10-2 | 10 | Critical | Team-written chats are not independent real data | FIXED | v11: written-by-us chats are a separate subset; main results use public chats only |
| S10-3 | 10 | Major | Source bias between scam reports and legit threads | OPEN | No per-source analysis planned on the slide |
| S10-4 | 10 | Major | Exact authentic vs authored count per class | PARTIAL | Target sizes given; actual counts must be reported per class at evaluation time |
| S10-5 | 10 | Major | Freeze prompts, models and thresholds before opening the test set | OPEN | Slide says never used for training or picking prompts; no explicit freeze statement |
| S10-6 | 10 | Moderate | Anonymization beyond names, Steam IDs and links | PARTIAL | Placeholders cover names, IDs and links; screenshot metadata and other identifiers not mentioned |
| S11-1 | 11 | Major | Zero-shot Llama may not be a fair baseline | PARTIAL | Slide 12: all models see the same test chats, one prefix at a time; the Llama prompt and output format are not described |
| S11-2 | 11 | Major | Why DeBERTa-v3-base over other encoders | DEFERRED | Prepare as an oral answer (compute, classification fit, direct comparison with Llama); not needed on the slide |
| S11-3 | 11 | Major | Event representation not shown on the models slide | PARTIAL | The chat-plus-event input is shown in the slide 5 example, not on slide 11 |
| S11-4 | 11 | Moderate | Prefix training creates correlated examples | FIXED | Covered on slide 9: split by config group before making prefixes |
| S12-1 | 12 | Critical | Primary criterion (scam-vs-legit F1) differs from headline macro-F1 | PARTIAL | Targets text now makes scam-vs-legit F1 primary and macro-F1 secondary; the top Macro-F1 card still reads as the headline metric (see Residual issues) |
| S12-2 | 12 | Critical | Alert time and harmful action not formally defined | FIXED | v11: first message from which the model stays right, vs. the hook (send an item, open a link, share a code); no alert = missed |
| S12-3 | 12 | Major | False-alarm rate on 50 legit chats is coarse | PARTIAL | v11: at most 5 of 50, a chat counts if any prefix is flagged, all numbers with 95% CIs; CI for the false-alarm rate itself is implied, not stated |
| S12-4 | 12 | Major | Missing or unstable predictions in alert time | FIXED | "No alert = missed" and "stays right" define both cases |
| S12-5 | 12 | Major | Bootstrap unit unspecified | FIXED | v11: resampling the test chats (conversation level) |
| S12-6 | 12 | Moderate | Data-quality metric mixes judge and human scores | OPEN | Unchanged; report judge and human scores separately |
| S13-1 | 13 | Minor | Add a contribution subtitle | REJECTED | Cosmetic |
| S14-1 | 14 | Major | References lack full bibliographic data | PARTIAL | Academic papers now have authors, year, title, venue or arXiv id; tools and web sources remain abbreviated |
| S14-2 | 14 | Major | No slide-level citations | PARTIAL | Reference groups are labeled by slide number; numbered markers on slides 2, 4, 6 not added |
| S14-3 | 14 | Major | No description of the literature search behind the novelty claim | OPEN | Record the search terms, indexes and date in this repo (see Follow-ups) |
| S14-4 | 14 | Moderate | Split dense reference slide in two | REJECTED | Optional; appendix-level polish |
| G-1 | - | Missing | Project timeline and owner per stage | DEFERRED | Midterm deliverable |
| G-2 | - | Risk | Event availability on real platforms (chat-only fallback) | DEFERRED | The chat-only vs chat+events ablation already gives the fallback; mention in midterm |

## Residual issues found while checking v11

1. **Slide 12 headline metric.** The Macro-F1 card (7 classes) is still the first metric shown, but the success target is scam-vs-legit F1 with macro-F1 secondary. Reorder the cards or label macro-F1 as secondary.
2. **README is out of date.** It says mDeBERTa and "EN + HE-EN"; the proposal says DeBERTa-v3-base and English only. The repo still holds the earlier proposal PPTX.
3. **Slide 9 TF-IDF rule.** Written as an automatic "too easy, rewrite prompts" at 0.95 with no justification for the threshold (S9-3).

## Bot reliability notes

- The bot reported it could not open the course HTML guides. The "Guide reference" column in its output is topic-level guesswork with no verified section numbers; do not cite it.
- It reviewed the v10 PDF, so some comments were already resolved by the time of this log.
- Its severity labels (Critical, Major) are not calibrated to our scope. For example S10-1 asks for a larger test set, which conflicts with the agreed scope cuts.

## Follow-ups

- [ ] Before the full generation run: attribute constraint matrix and legit-vs-scam conditions (S8-1, S8-2).
- [ ] Record the literature search (terms, indexes, date) that supports "we found no public dataset" (S14-3).
- [ ] Midterm (2026-12-09): timeline and owners (G-1), per-filter rejection counts (S7-2), authentic vs authored counts per class (S10-4).
- [ ] Next proposal edit, if any: S4-1, S5-3, S6-2, S9-2, S9-3, S9-5, S10-5, S12-1, S12-6.
