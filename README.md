# ScamSense: Catching Scams in In-Game Trading Chats

LLM4NLP course project · Vered Shaulov, Mikele Shteinberg

## 1. Overview

Players trade skins and items on Steam, Roblox and Discord, and scams look like normal trades that build up over several messages. ScamSense reads the first messages and trade events of a chat and predicts **legit** or one of **6 scam types** (fake middleman, fake payment, item swap, phishing link, impersonation, fake support) before the player acts. The main model is DeBERTa-v3-base, fine-tuned on synthetic chats and tested on real public chats (English).

## 2. Repository Structure

```
scamsense/
├── README.md, requirements.txt, environment.yml, LICENSE, .env.example
├── slides/                  # proposal, midterm, final (PPTX + PDF)
├── src/
│   ├── data/                # generation, filtering, splits, prefixes
│   ├── models/              # TF-IDF, zero-shot LLM, DeBERTa, MiniLM
│   ├── training/            # fine-tuning
│   ├── evaluation/          # macro-F1, alert time, data quality
│   └── utils/               # seeding, logging, config loading
├── notebooks/               # 01_data_exploration, 02_baseline, 03_experiments
├── data/
│   ├── raw/                 # synthetic/ (generated); real/ is never committed
│   ├── processed/
│   └── samples/             # small anonymized samples
├── configs/                 # generation and training configs
├── results/                 # metrics/, predictions/, experiment_logs/
├── visuals/                 # visual abstract, pipeline diagram, result_figures/
└── tests/
```

## 3. Project Motivation

_To be written._

## 4. Problem Statement

_To be written._

## 5. Visual Abstract

_To be added: `visuals/visual_abstract.png`._

## 6. Datasets

_To be written: name, source, license, sample count, fields, preprocessing, splits, access, limitations for each dataset._

Real chats are not committed. Only anonymized samples are kept in `data/samples/`.

## 7. Models and Pipeline

_To be written._

## 8. Data Augmentation and Generation

_To be written._

## 9. Training Process

_To be written._

## 10. Evaluation and Metrics

_To be written._

## 11. Results

_To be written._

## Reproducibility

Python 3.12. On Google Colab:

```bash
git clone https://github.com/mikeleshtbrg/scamsense.git
cd scamsense
pip install -r requirements.txt
cp .env.example .env   # then fill in the keys
```

Locally with conda: `conda env create -f environment.yml && conda activate scamsense`.

Environment variables are listed in `.env.example`. Data preparation, training, evaluation and inference commands will be added as the pipeline is built.

## Team Members and Contributions

| Member | Contributions |
|---|---|
| Vered Shaulov | _To be written._ |
| Mikele Shteinberg | _To be written._ |
