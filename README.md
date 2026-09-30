# bangla-dialect-classification

Regional dialect classification for Bengali text, built on the **BanglaDial**
dataset.

## Dataset

`data/BanglaDial.csv` — merged and imbalanced text dataset for Bengali
regional dialect analysis.

| | |
|---|---|
| Rows | 63,303 |
| Columns | `Sentence` (Bengali text), `Language` (dialect label) |
| Classes | 12 — 11 regional dialects + `Standard_Bangla` |
| Missing values | 0 |
| Duplicate rows | 1,763 |

Class distribution is imbalanced: `Chittagong` 13.93% (8,819) down to
`Rajshahi` 1.41% (891) — roughly a 10x gap.

> The file `data/BanglaDial_ A Merged and Imbalanced text Dataset for Bengali
> Regional dialect analysis. - Sheet1.csv` is a byte-identical duplicate of
> `BanglaDial.csv`; `main.py` reads the latter.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

Prints a dataset overview, the first 10 rows, the class distribution with a
bar chart, and sample sentences from each dialect.
