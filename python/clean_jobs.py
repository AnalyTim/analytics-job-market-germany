from pathlib import Path

import pandas as pd


INPUT_PATH = Path("data/raw/jobs.csv")
OUTPUT_PATH = Path("data/clean/jobs_clean.csv")

DATE_COLUMNS = [
    "date_posted",
    "date_modified",
    "publication_start",
    "start_date",
]


def load_jobs(input_path: Path) -> pd.DataFrame:
    df = pd.read_csv(
        input_path,
        sep=";",
        encoding="utf-8-sig",
    )

    print(f"Loaded {len(df)} rows from {input_path}")

    return df


def clean_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    text_columns = df.select_dtypes(include="str").columns

    for column in text_columns:
        df[column] = df[column].str.strip()

    return df


def clean_city(df: pd.DataFrame) -> pd.DataFrame:
    def remove_state_from_city(row: pd.Series) -> str | None:
        city = row.get("city")
        state = row.get("state")

        if pd.isna(city):
            return None

        city = str(city).strip()

        if pd.notna(state):
            state = str(state).strip()

            suffix = f", {state}"

            if city.lower().endswith(suffix.lower()):
                city = city[: -len(suffix)].strip()

        return city

    df["city"] = df.apply(
        remove_state_from_city,
        axis=1,
    )

    return df


def normalize_urls(df: pd.DataFrame) -> pd.DataFrame:
    def normalize_url(url: str | None) -> str | None:
        if pd.isna(url):
            return None

        url = str(url).strip()

        if not url:
            return None

        if not url.startswith(("http://", "https://")):
            url = f"https://{url}"

        return url

    df["company_url"] = df["company_url"].apply(normalize_url)

    return df


def convert_dates(df: pd.DataFrame) -> pd.DataFrame:
    for column in DATE_COLUMNS:
        if column in df.columns:
            df[column] = pd.to_datetime(
                df[column],
                errors="coerce",
            )

    return df


def add_salary_columns(df: pd.DataFrame) -> pd.DataFrame:
    df["salary_midpoint"] = (
        df["salary_min"] + df["salary_max"]
    ) / 2

    df["has_salary"] = (
        df["salary_min"].notna()
        | df["salary_max"].notna()
    )

    df["salary_yearly"] = df["salary_midpoint"].where(
        df["salary_period"].eq("JAHRESGEHALT")
    )

    df["salary_monthly"] = df["salary_midpoint"].where(
        df["salary_period"].eq("MONATSGEHALT")
    )

    df["salary_hourly"] = df["salary_midpoint"].where(
        df["salary_period"].eq("STUNDENLOHN")
    )

    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    rows_before = len(df)

    df = df.drop_duplicates(
        subset=["job_id"],
        keep="first",
    )

    removed_rows = rows_before - len(df)

    print(f"Removed {removed_rows} duplicate rows")

    return df


def save_jobs(
    df: pd.DataFrame,
    output_path: Path,
) -> None:
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        output_path,
        sep=";",
        index=False,
        encoding="utf-8-sig",
        date_format="%Y-%m-%d",
    )

    print(f"Saved {len(df)} cleaned rows to {output_path}")


def main() -> None:
    df = load_jobs(INPUT_PATH)

    df = clean_text_columns(df)
    df = clean_city(df)
    df = normalize_urls(df)
    df = convert_dates(df)
    df = add_salary_columns(df)
    df = remove_duplicates(df)

    save_jobs(
        df,
        OUTPUT_PATH,
    )

    print()
    print("Cleaned dataset shape:", df.shape)
    print()
    print(df.head())


if __name__ == "__main__":
    main()