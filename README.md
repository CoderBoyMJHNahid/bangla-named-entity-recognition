# bangla-dialect-classification

Regional dialect classification for Bengali text, built on the **BanglaDial**
dataset. The script splits the merged dataset into one file per dialect in both
Excel and JSON form, ready for downstream modelling.

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

Class distribution is imbalanced, with a gap of roughly 10x between the
largest and smallest class:

| Dialect | Rows | Share |
|---|---|---|
| Chittagong | 8,819 | 13.93% |
| Kishoreganj | 8,751 | 13.82% |
| Narail | 7,829 | 12.37% |
| Tangail | 6,793 | 10.73% |
| Rangpur | 5,909 | 9.33% |
| Narsingdi | 5,862 | 9.26% |
| Standard_Bangla | 4,545 | 7.18% |
| Barisal | 4,270 | 6.75% |
| Sylhet | 3,922 | 6.20% |
| Mymensingh | 3,212 | 5.07% |
| Noakhali | 2,500 | 3.95% |
| Rajshahi | 891 | 1.41% |

> The file `data/BanglaDial_ A Merged and Imbalanced text Dataset for Bengali
> > Regional dialect analysis. - Sheet1.csv` is a byte-identical duplicate of
> > `BanglaDial.csv`; `main.py` reads the latter.

## Project structure

```
.
├── main.py
├── requirements.txt
└── data/
    ├── BanglaDial.csv          # input, 63,303 rows
    └── finalized/
        ├── xlsx/               # 12 files, one per dialect
        │   ├── Barisal.xlsx
        │   ├── Chittagong.xlsx
        │   └── ...
        └── json/               # 12 files, one per dialect
            ├── Barisal.json
            ├── Chittagong.json
            └── ...
```

## Setup

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Windows (PowerShell)

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If PowerShell refuses to run the activation script, allow it for the current
session only:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

On Windows Command Prompt, activate with `.venv\Scripts\activate.bat` instead.

## Running

### macOS / Linux

```bash
source .venv/bin/activate
python main.py
```

### Windows (PowerShell)

```powershell
.\.venv\Scripts\Activate.ps1
python main.py
```

Output directories are created if they do not exist. The run prints a summary
followed by the two output locations:

```
========================================================================
SPLITTING DATASET
========================================================================
Total rows : 63,303
Languages  : 12

Barisal                4,270 rows
Chittagong             8,819 rows
Kishoreganj            8,751 rows
...
Rajshahi                 891 rows
Standard_Bangla        4,545 rows

========================================================================
DONE
========================================================================
Excel files : .../data/finalized/xlsx
JSON files  : .../data/finalized/json
```

> `data/finalized/` is committed to the repository rather than ignored, so a
> re-run rewrites 24 tracked files and will show up as changes in
> `git status`. The Excel files are byte-stable in content but not in size —
> `openpyxl` writes a timestamp into the archive, so re-running always
> produces a small diff even when the data is unchanged.

## Outputs

For each of the 12 dialects, two files are written.

**Excel** — written with `to_excel(..., index=False)`, so each file has the two
columns as headers with no extra index column.

**JSON** — a list of records, written with `ensure_ascii=False` and
`indent=2` so Bengali text stays readable instead of being escaped to
`\uXXXX`:

```json
[
  {
    "Sentence": "আমি বেটাতোকে ঘিন্না করি",
    "Language": "Rajshahi"
  }
]
```

## Code conventions

The code follows a small set of consistent rules.

- **Type hints everywhere.** Every function signature is annotated, including
  the `-> None` return on functions that only print or write files.
- **Constants in UPPER_CASE.** Module-level configuration such as
  `BASE_DIR`, `INPUT_FILE`, `XLSX_DIR`, `JSON_DIR`, `SENTENCE_COL`, and
  `LABEL_COL` sits in a single block at the top of the file.
- **Banner comments divide the file.** Sections are separated by
  `# ---` rules with a title, e.g. `Paths`, `Load dataset`, `Split dataset`,
  and `Main`, so the file reads top to bottom without scrolling.
- **One function per task.** `load_data` reads, `split_dataset` writes,
  `main` wires them together. No step does two jobs.
- **Paths are absolute.** `BASE_DIR` is derived from
  `Path(__file__).resolve().parent` rather than relative paths, so the script
  works from any working directory.
- **Guarded entry point.** Work runs under `if __name__ == "__main__":` so the
  modules stay importable.
- **Minimal dependencies.** `pandas` does the reading and writing; Excel
  output relies on `openpyxl`, which `requirements.txt` pins explicitly rather
  than leaving it implicit.
- **Pinned versions.** `requirements.txt` pins exact versions for
  reproducibility.

## Dependencies

| Package | Role |
|---|---|
| `pandas` | Reads `BanglaDial.csv`, filters by label, writes xlsx and JSON |
| `openpyxl` | Excel engine used by `pandas.to_excel` |

All versions are pinned in `requirements.txt`.
