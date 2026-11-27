"""One JSONL line per generated chat: what we sent, to which model, and what came back.

The API output itself is not reproducible (even with the same prompt and seed),
so this log is the record: every chat can be traced back to its config, prompt,
model, parameters and raw output.

Usage:
    from src.utils.log import log_sample
    log_sample(LOG_PATH, config_id="s42_00001", prompt=p, model="gpt-5-mini",
               raw_output=text, seed=42, params={"max_output_tokens": 800})
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class GenerationRecord(BaseModel):
    """Fields every log line must have. Extra fields (label, hook_msg, ...) are kept as is."""

    model_config = ConfigDict(extra="allow", protected_namespaces=())

    config_id: str = Field(min_length=1)
    prompt: str = Field(min_length=1)
    model: str = Field(min_length=1)
    raw_output: str
    seed: int
    params: dict[str, Any] = Field(default_factory=dict)
    ts: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat(timespec="seconds"))


def log_sample(path: str | Path, **rec: Any) -> dict:
    """Validate one record and append it to the JSONL file as a single line."""
    record = GenerationRecord(**rec)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8", newline="\n") as f:
        f.write(record.model_dump_json() + "\n")
    return record.model_dump()


def read_log(path: str | Path) -> list[dict]:
    """All records in the file, in the order they were written."""
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]
