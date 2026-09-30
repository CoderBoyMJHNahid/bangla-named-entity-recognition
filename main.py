from pathlib import Path

import pandas as pd

DATA_PATH = Path(__file__).resolve().parent / "data" / "BanglaDial.csv"
SENTENCE_COL = "Sentence"
LABEL_COL = "Language"
EXAMPLES_PER_CLASS = 2
MAX_EXAMPLE_CHARS = 70


def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")
    return pd.read_csv(path, encoding="utf-8")


def summarize(df: pd.DataFrame) -> None:
    print("=" * 72)
    print("DATASET OVERVIEW")
    print("=" * 72)
    print(f"Rows            : {len(df):,}")
    print(f"Columns         : {len(df.columns)} -> {list(df.columns)}")
    print(f"Classes         : {df[LABEL_COL].nunique()}")
    print(f"Missing values  : {int(df.isna().sum().sum())}")
    print(f"Duplicate rows  : {int(df.duplicated().sum())}")
    print(f"Duplicate texts : {int(df[SENTENCE_COL].duplicated().sum()):,}")

    lengths = df[SENTENCE_COL].str.split().str.len()
    print(f"Words / sentence: min {lengths.min()}, "
          f"mean {lengths.mean():.2f}, median {lengths.median():.0f}, max {lengths.max()}")


def show_head(df: pd.DataFrame, n: int = 10) -> None:
    print()
    print("=" * 72)
    print(f"FIRST {n} ROWS")
    print("=" * 72)
    print(df.head(n).to_string(index=False))


def show_class_distribution(df: pd.DataFrame) -> pd.Series:
    counts = df[LABEL_COL].value_counts()
    total = counts.sum()
    balance = counts.max() / counts.min()

    print()
    print("=" * 72)
    print("CLASS DISTRIBUTION")
    print("=" * 72)
    print(f"{'Language':<20}{'Count':>9}{'Percent':>10}  {'Bar'}")
    print("-" * 72)
    for label, count in counts.items():
        pct = count / total * 100
        bar = "#" * max(1, round(pct / counts.max() * 20))
        print(f"{label:<20}{count:>9,}{pct:>9.2f}%{bar:<24}")
    print("-" * 72)
    print(f"{'TOTAL':<20}{total:>9,}{100.0:>9.2f}%")
    print(f"\nImbalance: largest class is {balance:.1f}x the smallest.")
    return counts


def show_examples(df: pd.DataFrame, n: int = EXAMPLES_PER_CLASS) -> None:
    print()
    print("=" * 72)
    print("SAMPLE SENTENCES PER DIALECT")
    print("=" * 72)
    for label, group in df.groupby(LABEL_COL, sort=True):
        print(f"\n[{label}]  ({len(group):,} rows)")
        for sentence in group[SENTENCE_COL].head(n):
            text = str(sentence)
            if len(text) > MAX_EXAMPLE_CHARS:
                text = text[: MAX_EXAMPLE_CHARS - 1].rstrip() + "…"
            print(f"  - {text}")


def main() -> None:
    df = load_data()
    summarize(df)
    show_head(df)
    show_class_distribution(df)
    show_examples(df)
    print()


if __name__ == "__main__":
    main()
