from pathlib import Path

import pandas as pd
import requests


API_URL = "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v4/jobs"

OUTPUT_PATH = Path("data/raw/jobs.csv")


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
    jobs = data["stellenangebote"]

    print("Number of jobs received:", len(jobs))

    jobs_list = []

    for job in jobs:
        workplace = job.get("arbeitsort", {})

        jobs_list.append(
            {
                "title": job.get("titel"),
                "profession": job.get("beruf"),
                "company": job.get("arbeitgeber"),
                "city": workplace.get("ort"),
                "state": workplace.get("region"),
                "country": workplace.get("land"),
            }
        )

    df = pd.DataFrame(jobs_list)

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        OUTPUT_PATH,
        sep=";",
        index=False,
        encoding="utf-8-sig",
    )

    print()
    print(df)
    print()
    print(f"Saved {len(df)} jobs to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()