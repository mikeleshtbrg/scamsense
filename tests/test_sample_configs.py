"""Config sampler: exact quotas, fixed seed, valid events. Run: python -m pytest"""

import json
from collections import Counter

import pytest

from src.data.events import format_event, parse_event
from src.data.sample_configs import (
    GEN_CFG, exact_counts, hook_ranges, load_yaml, paths, sample_configs,
)

SPACE_CFG, OUT_DIR = paths()
GEN, SPACE = load_yaml(GEN_CFG), load_yaml(SPACE_CFG)
SEED, N = GEN["seed"], GEN["n_configs"]
SCAMS = [lab for lab in GEN["label_mix"] if lab != "legit"]


@pytest.fixture(scope="module")
def configs():
    return sample_configs(SEED, N, GEN["label_mix"], SPACE)


def test_label_quotas_exact(configs):
    counts = Counter(c["label"] for c in configs)
    assert len(configs) == N
    assert counts["legit"] == round(0.40 * N)
    for lab in SCAMS:
        assert counts[lab] == round(0.10 * N)


def test_legit_half_tricky(configs):
    subs = Counter(c["legit_subtype"] for c in configs if c["label"] == "legit")
    n_legit = sum(subs.values())
    assert subs["normal_trade"] == n_legit // 2
    assert sum(v for k, v in subs.items() if k != "normal_trade") == n_legit - n_legit // 2
    assert all(c["legit_subtype"] is None for c in configs if c["label"] != "legit")


def test_scam_word_exactly_ten_percent_per_class(configs):
    for lab in GEN["label_mix"]:
        group = [c for c in configs if c["label"] == lab]
        assert sum(c["scam_word"] for c in group) == round(0.10 * len(group))


def test_attributes_in_space(configs):
    for c in configs:
        assert c["game"] in SPACE["game"]
        assert c["item_value"] in SPACE["item_value"]
        assert c["style"] in SPACE["style"]
        assert SPACE["length"]["min"] <= c["length"] <= SPACE["length"]["max"]
        if c["label"] == "legit":
            assert c["tactic"] is None and c["hook_position"] is None and c["hook_msg"] is None
            assert c["victim_reaction"] in SPACE["victim_reaction"]["legit"]
        else:
            assert c["tactic"] in SPACE["tactic"]["all"]
            assert c["victim_reaction"] in SPACE["victim_reaction"]["scam"]
            assert c["hook_msg"] in hook_ranges(c["length"], SPACE["hook_min_msg"])[c["hook_position"]]
    assert not any(c["tactic"] == "authority" for c in configs if c["label"] == "phishing")


def test_attributes_spread_evenly_per_class(configs):
    for lab in GEN["label_mix"]:
        games = Counter(c["game"] for c in configs if c["label"] == lab)
        assert max(games.values()) - min(games.values()) <= 1


def test_same_seed_same_output_other_seed_differs(configs):
    again = sample_configs(SEED, N, GEN["label_mix"], SPACE)
    assert again == configs
    other = sample_configs(SEED + 1, N, GEN["label_mix"], SPACE)
    assert other != configs


def test_ids_unique(configs):
    assert len({c["config_id"] for c in configs}) == len(configs)


def test_events_valid_and_placed(configs):
    for c in configs:
        prev = 0
        for e in c["events"]:
            assert 0 <= e["after_msg"] <= c["length"]
            assert e["after_msg"] >= prev
            prev = e["after_msg"]
            line = format_event(e["type"], e["attrs"])
            assert parse_event(line) == (e["type"], e["attrs"])
            assert not any(ch.isdigit() for ch in line)


def test_events_match_label(configs):
    for c in configs:
        types = [e["type"] for e in c["events"]]
        if c["label"] == "item_swap":
            ch = [e for e in c["events"] if e["type"] == "trade_offer_changed"]
            assert len(ch) == 1 and ch[0]["after_msg"] == c["hook_msg"] - 1
            assert types.index("trade_offer") < types.index("trade_offer_changed")
        if c["label"] in ("fake_middleman", "fake_support"):
            assert any(e["type"] == "friend_request" and e["attrs"]["sender"] == "other"
                       and e["after_msg"] == c["hook_msg"] for e in c["events"])
        if c["label"] == "impersonation":
            assert c["events"][0]["after_msg"] == 0 and c["events"][0]["type"] == "friend_request"
        if c["label"] == "legit":
            if c["legit_subtype"] == "official_middleman":
                assert any(e["attrs"].get("sender") == "other" for e in c["events"])


def test_no_event_only_shortcuts(configs):
    """Event cues that point to a scam must also appear in some legit chats."""
    legit = [c for c in configs if c["label"] == "legit"]
    assert any(e["type"] == "trade_offer_changed" for c in legit for e in c["events"])
    assert any(e["attrs"].get("account_age") == "new" for c in legit for e in c["events"])
    assert any("trade_offer" not in [e["type"] for e in c["events"]] for c in legit)
    for lab in ("fake_middleman", "fake_payment"):
        assert any(e["type"] == "trade_offer" for c in configs if c["label"] == lab for e in c["events"])


def test_exact_counts_sums():
    assert sum(exact_counts(7, {"a": 0.4, "b": 0.3, "c": 0.3}).values()) == 7


def test_saved_file_matches_sampler(configs):
    """The committed configs file is exactly what the sampler produces."""
    path = OUT_DIR / f"configs_seed{SEED}_n{N}.jsonl"
    if not path.exists():
        pytest.skip(f"{path.name} not generated yet")
    with open(path, encoding="utf-8") as f:
        saved = [json.loads(line) for line in f]
    assert saved == configs
