from pathlib import Path
import json
import pandas as pd


# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "data" / "BanglaDial.csv"

XLSX_DIR = BASE_DIR / "data" / "finalized" / "xlsx"
JSON_DIR = BASE_DIR / "data" / "finalized" / "json"

SENTENCE_COL = "Sentence"
LABEL_COL = "Language"


# --------------------------------------------------
# Load dataset
# --------------------------------------------------

def load_data(path: Path = INPUT_FILE) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    return pd.read_csv(path, encoding="utf-8")


# --------------------------------------------------
# Split dataset
# --------------------------------------------------

def split_dataset(df: pd.DataFrame) -> None:

    XLSX_DIR.mkdir(parents=True, exist_ok=True)
    JSON_DIR.mkdir(parents=True, exist_ok=True)

    languages = sorted(df[LABEL_COL].dropna().unique())

    print("=" * 72)
    print("SPLITTING DATASET")
    print("=" * 72)

    print(f"Total rows : {len(df):,}")
    print(f"Languages  : {len(languages)}")
    print()

    for language in languages:

        # Get rows belonging to this language
        language_df = df[df[LABEL_COL] == language].copy()

        # Safe filename
        filename = str(language).strip()

        # ------------------------------------------
        # Excel
        # ------------------------------------------

        xlsx_path = XLSX_DIR / f"{filename}.xlsx"

        language_df.to_excel(
            xlsx_path,
            index=False
        )

        # ------------------------------------------
        # JSON
        # ------------------------------------------

        json_path = JSON_DIR / f"{filename}.json"

        records = language_df.to_dict(orient="records")

        with open(
            json_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                records,
                file,
                ensure_ascii=False,
                indent=2
            )

        print(
            f"{language:<20}"
            f"{len(language_df):>8,} rows"
        )

    print()
    print("=" * 72)
    print("DONE")
    print("=" * 72)

    print(f"Excel files : {XLSX_DIR}")
    print(f"JSON files  : {JSON_DIR}")


# --------------------------------------------------
# Main
# --------------------------------------------------

def main() -> None:

    df = load_data()

    split_dataset(df)


if __name__ == "__main__":
    main()