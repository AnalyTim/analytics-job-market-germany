from pathlib import Path
from pprint import pprint

import pandas as pd
import requests


API_URL = "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v4/jobs"

SEARCH_QUERY = "Analyst"
SEARCH_LOCATION = "Deutschland"

PAGE = 1
PAGE_SIZE = 100

OUTPUT_PATH = Path("data/raw/jobs.csv")


def fetch_jobs_page(
    query: str,
    location: str,
    page: int,
    size: int,
) -> tuple[list[dict], int]:
    params = {
        "was": query,
        "wo": location,
        "page": page,
        "size": size,
    }

    headers = {
        "X-API-Key": "jobboerse-jobsuche",
    }

    response = requests.get(
        API_URL,
        params=params,
        headers=headers,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    jobs = data.get("stellenangebote", [])
    total_jobs = data.get("maxErgebnisse", 0)
    
    print(
        f"Page {page}: received {len(jobs)} jobs "
        f"of {total_jobs} total"
    )

    return jobs, total_jobs


def fetch_all_jobs(
    query: str,
    location: str,
    page_size: int,
) -> list[dict]:
    all_jobs = []
    page = 1

    while True:
        jobs, total_jobs = fetch_jobs_page(
            query=query,
            location=location,
            page=page,
            size=page_size,
        )

        all_jobs.extend(jobs)

        if len(all_jobs) >= total_jobs or not jobs:
            break

        page += 1

    return all_jobs


def transform_jobs(jobs: list[dict]) -> pd.DataFrame:
    jobs_list = []

    for job in jobs:
        workplace = job.get("arbeitsort", {})
        coordinates = workplace.get("koordinaten", {})

        jobs_list.append(
            {
                "job_id": job.get("refnr"),
                "title": job.get("titel"),
                "profession": job.get("beruf"),
                "company": job.get("arbeitgeber"),
                "postal_code": workplace.get("plz"),
                "city": workplace.get("ort"),
                "state": workplace.get("region"),
                "country": workplace.get("land"),
                "latitude": coordinates.get("lat"),
                "longitude": coordinates.get("lon"),
                "date_posted": job.get("aktuelleVeroeffentlichungsdatum"),
                "date_modified": job.get("modifikationsTimestamp"),
                "start_date": job.get("eintrittsdatum"),
            }
        )

    return pd.DataFrame(jobs_list)


def save_jobs(df: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        output_path,
        sep=";",
        index=False,
        encoding="utf-8-sig",
    )


def main() -> None:
    jobs = fetch_all_jobs(
    query=SEARCH_QUERY,
    location=SEARCH_LOCATION,
    page_size=PAGE_SIZE,
)

    print("Number of jobs received:", len(jobs))

    df = transform_jobs(jobs)

    save_jobs(df, OUTPUT_PATH)

    print()
    print(df)
    print()
    print(f"Saved {len(df)} jobs to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()