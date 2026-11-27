"""Smoke test for the generation log: 3 real chats from the first 3 sampled configs.

The prompt here is a placeholder, not the project prompt. Output goes to a separate
file so it does not mix with the real generation log.

Run from the repo root:  python -m src.utils.smoke_log
"""

import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from src.data.sample_configs import GEN_CFG, ROOT, load_yaml
from src.utils.log import log_sample, read_log
from src.utils.seed import set_seed

gen = load_yaml(GEN_CFG)
seed = set_seed(gen["seed"])
configs_file = ROOT / gen["paths"]["configs_sampled"] / f"configs_seed{seed}_n{gen['n_configs']}.jsonl"
out = ROOT / "results" / "experiment_logs" / "smoke_log.jsonl"

load_dotenv()
client = OpenAI(
    base_url=os.environ["AZURE_OPENAI_ENDPOINT"].rstrip("/") + "/openai/v1/",
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
)
model = os.environ["AZURE_OPENAI_DEPLOYMENT"]
params = {"reasoning": {"effort": "minimal"}, "max_output_tokens": 400}

with open(configs_file, encoding="utf-8") as f:
    configs = [json.loads(next(f)) for _ in range(3)]

for cfg in configs:
    prompt = (f"Write a short {cfg['game']} item-trade chat between <USER_1> and <USER_2>, "
              f"{cfg['length']} messages, one per line. Scenario label: {cfg['label']}.")
    r = client.responses.create(model=model, input=prompt, **params)
    log_sample(out, config_id=cfg["config_id"], label=cfg["label"], prompt=prompt,
               model=model, params=params, raw_output=r.output_text, seed=seed)

rows = read_log(out)
print(f"{len(rows)} records in {out.relative_to(ROOT)}")
for row in rows[-3:]:
    print(row["config_id"], row["label"], "|", row["raw_output"][:60].replace("\n", " / "))