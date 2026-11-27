"""Sample one config per synthetic chat, with exact quotas and a fixed seed.

A config holds the label, the 8 attributes and the trade events. The events are
built here in code, so the LLM only writes the messages around them.

Quotas are exact, not just expected: the label mix, the legit subtypes and the
scam-word share are allocated by count and then shuffled. The other attributes
are spread evenly inside each class (cycled, then shuffled).

Usage (from the repo root):
    python -m src.data.sample_configs            # seed and n_configs from generation.yaml
    python -m src.data.sample_configs --seed 7 --n 600
"""

from __future__ import annotations

import argparse
import json
import math
import random
from collections import Counter
from pathlib import Path

import yaml

from src.data.events import validate_event

ROOT = Path(__file__).resolve().parents[2]
GEN_CFG = ROOT / "configs" / "generation.yaml"

VALUE_ORDER = ["low", "mid", "high"]


def load_yaml(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def paths() -> tuple[Path, Path]:
    """(attribute space file, output folder) from generation.yaml."""
    p = load_yaml(GEN_CFG)["paths"]
    return ROOT / p["attribute_space"], ROOT / p["configs_sampled"]


def exact_counts(n: int, shares: dict[str, float]) -> dict[str, int]:
    """Split n into integer counts by shares (largest remainder, ties by key order)."""
    total = sum(shares.values())
    raw = {k: n * v / total for k, v in shares.items()}
    counts = {k: math.floor(x) for k, x in raw.items()}
    left = n - sum(counts.values())
    order = sorted(shares, key=lambda k: (-(raw[k] - counts[k]), list(shares).index(k)))
    for k in order[:left]:
        counts[k] += 1
    return counts


def even_column(rng: random.Random, n: int, values: list) -> list:
    """n values spread as evenly as possible, in random order."""
    col = [values[i % len(values)] for i in range(n)]
    rng.shuffle(col)
    return col


def exact_flags(rng: random.Random, n: int, rate: float) -> list[bool]:
    k = round(n * rate)
    col = [True] * k + [False] * (n - k)
    rng.shuffle(col)
    return col


def hook_ranges(length: int, min_msg: int) -> dict[str, list[int]]:
    """Split messages min_msg..length into early / middle / late thirds."""
    msgs = list(range(min_msg, length + 1))
    q, r = divmod(len(msgs), 3)
    sizes = [q + (1 if i < r else 0) for i in range(3)]
    out, start = {}, 0
    for name, size in zip(["early", "middle", "late"], sizes):
        out[name] = msgs[start:start + size]
        start += size
    return out


# ---------- trade events ----------

def _fr(rng, cfg, sender, ev_cfg) -> dict:
    p_new = ev_cfg["account_age_new"][cfg["label"]]
    age = "new" if rng.random() < p_new else "old"
    return {"type": "friend_request", "attrs": {"sender": sender, "account_age": age}}


def _at(after_msg: int, event: dict) -> dict:
    return {"after_msg": after_msg, **event}


def build_events(rng: random.Random, cfg: dict, ev_cfg: dict) -> list[dict]:
    """Trade events for one config. after_msg=0 means before message 1."""
    label, length, hook = cfg["label"], cfg["length"], cfg["hook_msg"]
    value = cfg["item_value"]
    opening = ev_cfg["opening_friend_request"]
    events: list[dict] = []

    if label in opening and rng.random() < opening[label]:
        events.append(_at(0, _fr(rng, cfg, "partner", ev_cfg)))

    if label == "legit":
        sub = cfg["legit_subtype"]
        offer_at = rng.randint(math.ceil(0.6 * length), length)
        if sub == "official_middleman":
            mm_at = rng.randint(2, offer_at - 1)
            events.append(_at(mm_at, _fr(rng, cfg, "other", ev_cfg)))
        if rng.random() < ev_cfg["legit_offer"]:
            sender = rng.choice(["partner", "warn"])
            events.append(_at(offer_at, {"type": "trade_offer",
                                         "attrs": {"sender": sender, "value": value}}))
        if (any(e["type"] == "trade_offer" for e in events) and offer_at < length
                and rng.random() < ev_cfg["legit_offer_changed"]):
            # honest renegotiation: the chat agrees on the change before it shows up
            new_value = rng.choice(VALUE_ORDER)
            events.append(_at(rng.randint(offer_at + 1, length),
                              {"type": "trade_offer_changed",
                               "attrs": {"old_value": value, "new_value": new_value}}))

    elif label == "fake_middleman":
        # the hook names the "middleman", whose friend request follows it
        events.append(_at(hook, _fr(rng, cfg, "other", ev_cfg)))

    elif label == "item_swap":
        # offer first, then it changes, then the hook pushes to confirm
        new_value = VALUE_ORDER[max(0, VALUE_ORDER.index(value) - 1)]
        events.append(_at(rng.randint(1, hook - 2),
                          {"type": "trade_offer", "attrs": {"sender": "partner", "value": value}}))
        events.append(_at(hook - 1,
                          {"type": "trade_offer_changed",
                           "attrs": {"old_value": value, "new_value": new_value}}))

    elif label == "impersonation":
        # the copied profile adds the victim before the chat starts
        events.append(_at(0, _fr(rng, cfg, "partner", ev_cfg)))

    elif label == "fake_support":
        # the hook says "add the rep"; the rep's request follows it
        events.append(_at(hook, _fr(rng, cfg, "other", ev_cfg)))

    # fake_payment and phishing: only the optional opening friend request

    post = ev_cfg["post_hook_offer"]
    if label in post and hook < length and rng.random() < post[label]:
        # the victim sends the item after the hook (to the "middleman" / before payment clears)
        events.append(_at(rng.randint(hook + 1, length),
                          {"type": "trade_offer", "attrs": {"sender": "warn", "value": value}}))

    for ev in events:
        validate_event(ev["type"], ev["attrs"])
        assert 0 <= ev["after_msg"] <= length
    events.sort(key=lambda e: e["after_msg"])  # stable: same-message order kept
    return events


# ---------- configs ----------

def sample_configs(seed: int, n: int, label_mix: dict[str, float], space: dict) -> list[dict]:
    rng = random.Random(seed)
    label_counts = exact_counts(n, label_mix)
    configs: list[dict] = []

    for label, count in label_counts.items():
        is_legit = label == "legit"
        if is_legit:
            sub_counts = exact_counts(count, space["legit_subtype"])
            subtypes = [s for s, c in sub_counts.items() for _ in range(c)]
            rng.shuffle(subtypes)
            tactics = [None] * count
            reactions = even_column(rng, count, space["victim_reaction"]["legit"])
            positions = [None] * count
        else:
            subtypes = [None] * count
            excl = space["tactic"].get("exclude", {}).get(label, [])
            tactics = even_column(rng, count, [t for t in space["tactic"]["all"] if t not in excl])
            reactions = even_column(rng, count, space["victim_reaction"]["scam"])
            positions = even_column(rng, count, space["hook_position"])

        games = even_column(rng, count, space["game"])
        values = even_column(rng, count, space["item_value"])
        styles = even_column(rng, count, space["style"])
        lengths = even_column(rng, count, list(range(space["length"]["min"],
                                                     space["length"]["max"] + 1)))
        scam_words = exact_flags(rng, count, space["scam_word_rate"])

        for i in range(count):
            hook_msg = None
            if positions[i] is not None:
                hook_msg = rng.choice(hook_ranges(lengths[i], space["hook_min_msg"])[positions[i]])
            configs.append({
                "label": label,
                "legit_subtype": subtypes[i],
                "game": games[i],
                "tactic": tactics[i],
                "victim_reaction": reactions[i],
                "item_value": values[i],
                "style": styles[i],
                "length": lengths[i],
                "hook_position": positions[i],
                "hook_msg": hook_msg,
                "scam_word": scam_words[i],
            })

    rng.shuffle(configs)
    for idx, cfg in enumerate(configs, start=1):
        cfg["config_id"] = f"s{seed}_{idx:05d}"
        cfg["seed"] = seed
        cfg["events"] = build_events(rng, cfg, space["events"])
    # config_id first, for readability
    return [{"config_id": c.pop("config_id"), **c} for c in configs]


def summarize(configs: list[dict]) -> dict:
    by_label = Counter(c["label"] for c in configs)
    return {
        "n_configs": len(configs),
        "label": dict(sorted(by_label.items())),
        "legit_subtype": dict(sorted(Counter(c["legit_subtype"] for c in configs
                                             if c["label"] == "legit").items())),
        "scam_word_by_label": {lab: sum(c["scam_word"] for c in configs if c["label"] == lab)
                               for lab in sorted(by_label)},
        "events_by_label": {lab: dict(sorted(Counter(e["type"] for c in configs
                                                     if c["label"] == lab
                                                     for e in c["events"]).items()))
                            for lab in sorted(by_label)},
        "account_age_new_by_label": {
            lab: sum(e["attrs"].get("account_age") == "new" for c in configs
                     if c["label"] == lab for e in c["events"])
            for lab in sorted(by_label)},
    }


def run(seed: int | None = None, n: int | None = None) -> Path:
    space_path, out_dir = paths()
    gen, space = load_yaml(GEN_CFG), load_yaml(space_path)
    seed = gen["seed"] if seed is None else seed
    n = gen["n_configs"] if n is None else n
    configs = sample_configs(seed, n, gen["label_mix"], space)
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"configs_seed{seed}_n{n}.jsonl"
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        for c in configs:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    with open(out_dir / f"summary_seed{seed}_n{n}.json", "w", encoding="utf-8", newline="\n") as f:
        json.dump(summarize(configs), f, indent=2)
        f.write("\n")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--n", type=int, default=None)
    args = ap.parse_args()
    out = run(args.seed, args.n)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
