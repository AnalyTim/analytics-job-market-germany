import base64
import time
from pathlib import Path

import pandas as pd
import requests


API_URL = (
    "https://rest.arbeitsagentur.de/"
    "jobboerse/jobsuche-service/pc/v6/jobs"
)

DETAILS_API_URL = (
    "https://rest.arbeitsagentur.de/"
    "jobboerse/jobsuche-service/pc/v4/jobdetails"
)

SEARCH_QUERY = "Analyst"
SEARCH_LOCATION = "Deutschland"

PAGE_SIZE = 100
DETAILS_TEST_LIMIT = None
REQUEST_DELAY_SECONDS = 0.5

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

    jobs = data.get("ergebnisliste", [])
    total_jobs = data.get("maxErgebnisse", 0)

    print(
        f"Page {page}: received {len(jobs)} jobs "
        f"of {total_jobs} total"
    )

    return jobs, total_jobs


def fetch_job_details(job_id: str) -> dict:
    encoded_job_id = base64.b64encode(
        job_id.encode("utf-8")
    ).decode("utf-8")

    headers = {
        "X-API-Key": "jobboerse-jobsuche",
    }

    response = requests.get(
        f"{DETAILS_API_URL}/{encoded_job_id}",
        headers=headers,
        timeout=30,
    )

    print("Details status code:", response.status_code)

    response.raise_for_status()

    return response.json()

def enrich_jobs_with_details(
    jobs: list[dict],
    limit: int | None = None,
    delay_seconds: float = 0.5,
) -> list[dict]:
    enriched_jobs = []

    jobs_to_process = jobs[:limit] if limit is not None else jobs

    for index, job in enumerate(jobs_to_process, start=1):
        job_id = job.get("referenznummer")

        if not job_id:
            print(f"Job {index}: missing reference number")
            enriched_jobs.append(job)
            continue

        try:
            details = fetch_job_details(job_id)

            enriched_job = job.copy()
            enriched_job.update(details)

            enriched_jobs.append(enriched_job)

            print(
                f"Details {index}/{len(jobs_to_process)}: "
                f"{job.get('stellenangebotsTitel')}"
            )

        except requests.RequestException as error:
            print(f"Could not fetch details for {job_id}: {error}")
            enriched_jobs.append(job)

        time.sleep(delay_seconds)

    return enriched_jobs


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
        locations = job.get("stellenlokationen", [])
        location = locations[0] if locations else {}

        address = location.get("adresse", {})
        start_period = job.get("eintrittszeitraum", {})
        publication_period = job.get("veroeffentlichungszeitraum", {})

        all_professions = job.get("alleBerufe") or []

        jobs_list.append(
            {
                "job_id": job.get("referenznummer"),
                "title": job.get("stellenangebotsTitel"),
                "profession": job.get("hauptberuf"),
                "all_professions": ", ".join(all_professions),
                "company": job.get("firma"),
                "postal_code": address.get("plz"),
                "city": address.get("ort"),
                "state": address.get("region"),
                "country": address.get("land"),
                "latitude": location.get("breite"),
                "longitude": location.get("laenge"),
                "date_posted": job.get("datumErsteVeroeffentlichung"),
                "date_modified": job.get("aenderungsdatum"),
                "publication_start": publication_period.get("von"),
                "start_date": start_period.get("von"),
                "employment_type": job.get("stellenangebotsart"),
                "full_time": job.get("arbeitszeitVollzeit"),
                "contract_duration": job.get("vertragsdauer"),
                "salary_type": job.get("artDerVerguetung"),
                "salary_period": job.get("verguetungsangabe"),
                "salary_min": job.get("gehaltsspanneVon"),
                "salary_max": job.get("gehaltsspanneBis"),
                "mini_job": job.get("istGeringfuegigeBeschaeftigung"),
                "career_changer": job.get("quereinstiegGeeignet"),
                "description": job.get("stellenangebotsBeschreibung"),
                "company_url": job.get("allianzpartnerUrl"),
                "alliance_partner": job.get("allianzpartnerName"),
                "temporary_employment": job.get("istArbeitnehmerUeberlassung"),
                "private_job_agency": job.get("istPrivateArbeitsvermittlung"),
                "disability_required": job.get("istBehinderungGefordert"),
            }
        )

    return pd.DataFrame(jobs_list)


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
    )


def main() -> None:
    jobs = fetch_all_jobs(
        query=SEARCH_QUERY,
        location=SEARCH_LOCATION,
        page_size=PAGE_SIZE,
    )

    print("Number of jobs received:", len(jobs))

    enriched_jobs = enrich_jobs_with_details(
    jobs,
    limit=DETAILS_TEST_LIMIT,
    delay_seconds=REQUEST_DELAY_SECONDS,
    )

    df = transform_jobs(enriched_jobs)

    save_jobs(
        df,
        OUTPUT_PATH,
    )

    print()
    print(df)
    print()
    print(f"Saved {len(df)} jobs to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()