"""Generation log and seeding. Run: python -m pytest tests/test_log.py"""

import random

import pytest
from pydantic import ValidationError

from src.utils.log import log_sample, read_log
from src.utils.seed import set_seed

CHATS = [
    {"config_id": "s42_00001", "label": "fake_middleman", "prompt": "Write a trade chat...",
     "raw_output": "<USER_1>: selling AWP\n<USER_2>: my friend can middleman"},
    {"config_id": "s42_00002", "label": "impersonation", "prompt": "Write a trade chat...",
     "raw_output": "<USER_1>: I'm from Valve support"},
    {"config_id": "s42_00003", "label": "legit", "prompt": "Write a trade chat...",
     "raw_output": "<USER_1>: 20 keys for the knife?\n<USER_2>: deal ✓"},
]


def test_three_chats_three_full_lines(tmp_path):
    path = tmp_path / "logs" / "generation_log.jsonl"
    for chat in CHATS:
        log_sample(path, model="gpt-5-mini", seed=42, params={"max_output_tokens": 800}, **chat)

    rows = read_log(path)
    assert len(rows) == 3
    for row, chat in zip(rows, CHATS):
        for key in ("config_id", "prompt", "model", "raw_output", "seed", "params", "ts"):
            assert key in row
        assert row["raw_output"] == chat["raw_output"]  # unicode survives the round trip
        assert row["label"] == chat["label"]           # extra fields are kept


def test_appends_without_overwriting(tmp_path):
    path = tmp_path / "log.jsonl"
    log_sample(path, model="m", seed=1, **CHATS[0])
    log_sample(path, model="m", seed=1, **CHATS[1])
    assert [r["config_id"] for r in read_log(path)] == ["s42_00001", "s42_00002"]


def test_missing_field_is_rejected(tmp_path):
    path = tmp_path / "log.jsonl"
    with pytest.raises(ValidationError):
        log_sample(path, config_id="s42_00001", prompt="p", raw_output="x", seed=42)  # no model
    assert not path.exists()  # nothing half-written


def test_set_seed_repeats_random():
    set_seed(42)
    first = [random.random() for _ in range(3)]
    set_seed(42)
    assert [random.random() for _ in range(3)] == first


def test_set_seed_repeats_numpy_and_torch():
    np = pytest.importorskip("numpy")
    set_seed(7)
    a = np.random.rand(3)
    set_seed(7)
    assert (np.random.rand(3) == a).all()

    torch = pytest.importorskip("torch")
    set_seed(7)
    t = torch.rand(3)
    set_seed(7)
    assert torch.equal(torch.rand(3), t)