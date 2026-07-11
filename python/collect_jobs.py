from pathlib import Path

import pandas as pd
import requests


API_URL = "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v4/jobs"


def main():
    params = {
        "was": "Analyst",
        "wo": "Deutschland",
        "page": 1,
        "size": 10,
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

    print("Status code:", response.status_code)
    print("Requested URL:", response.url)

    response.raise_for_status()

    data = response.json()

    print("Response type:", type(data))
    print("Top-level keys:", data.keys())

    jobs = data["stellenangebote"]

    jobs_list = []

    print()
    print("Number of jobs:", len(jobs))
    print()

    for job in jobs:
        jobs_list.append(
    {
        "title": job["titel"],
        "profession": job["beruf"],
        "company": job["arbeitgeber"],
        "city": job["arbeitsort"]["ort"],
        "state": job["arbeitsort"]["region"],
        "country": job["arbeitsort"]["land"],
    }
)
    df = pd.DataFrame(jobs_list)

    output_path = Path("data/raw/jobs.csv")

    df.to_csv(
    output_path,
    index=False,
    encoding="utf-8-sig",
)

    print()
    print(df)
    print()
    print(f"Saved {len(df)} jobs to {output_path}")


if __name__ == "__main__":
    main()