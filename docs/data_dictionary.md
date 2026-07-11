# Data Dictionary

This document describes the fields planned for the job postings dataset.

| Column | Data Type | Description | Example |
|---|---|---|---|
| job_id | TEXT | Unique identifier for the job posting | stepstone_12345 |
| job_title | TEXT | Original job title from the posting | Business Analyst |
| normalized_job_title | TEXT | Standardized job category | Business Analyst |
| company_name | TEXT | Name of the employer | Bosch |
| city | TEXT | City listed in the job posting | Berlin |
| federal_state | TEXT | German federal state | Berlin |
| country | TEXT | Country of the job location | Germany |
| work_model | TEXT | Remote, hybrid or on-site working model | Hybrid |
| employment_type | TEXT | Full-time, part-time, internship or other contract type | Full-time |
| seniority_level | TEXT | Junior, mid-level, senior or unspecified | Junior |
| salary_min | DECIMAL | Minimum annual gross salary, if available | 50000 |
| salary_max | DECIMAL | Maximum annual gross salary, if available | 65000 |
| salary_currency | TEXT | Currency used in the salary information | EUR |
| date_posted | DATE | Date when the job was published | 2026-07-11 |
| date_collected | DATE | Date when the posting was collected | 2026-07-11 |
| job_description | TEXT | Full text of the job advertisement | ... |
| source_platform | TEXT | Job platform where the posting was found | StepStone |
| job_url | TEXT | Direct URL to the job posting | https://... |