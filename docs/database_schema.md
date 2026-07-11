# Database Schema

## Overview

The database is designed to store job postings, companies, required skills and job benefits.

Each job posting belongs to one company and may contain multiple skills and benefits.

## Entity Relationship Diagram

```mermaid
erDiagram
    COMPANIES ||--o{ JOB_POSTINGS : publishes
    JOB_POSTINGS ||--o{ JOB_SKILLS : requires
    SKILLS ||--o{ JOB_SKILLS : appears_in
    JOB_POSTINGS ||--o{ JOB_BENEFITS : offers
    BENEFITS ||--o{ JOB_BENEFITS : appears_in

    COMPANIES {
        int company_id PK
        text company_name
        text industry
        text company_size
        text headquarters_country
    }

    JOB_POSTINGS {
        text job_id PK
        int company_id FK
        text job_title
        text normalized_job_title
        text city
        text federal_state
        text country
        text work_model
        text employment_type
        text seniority_level
        numeric salary_min
        numeric salary_max
        text salary_currency
        text job_language
        text education_required
        text experience_required
        date date_posted
        date date_collected
        text source_platform
        text job_url
        text job_description
    }

    SKILLS {
        int skill_id PK
        text skill_name
        text skill_category
    }

    JOB_SKILLS {
        text job_id FK
        int skill_id FK
    }

    BENEFITS {
        int benefit_id PK
        text benefit_name
    }

    JOB_BENEFITS {
        text job_id FK
        int benefit_id FK
    }
```

## Table Purpose

### companies

Stores company-level information that may be reused across multiple job postings.

### job_postings

Stores the main details of each collected vacancy.

### skills

Stores the standardized list of technical and business skills.

Examples:

- SQL
- Python
- Power BI
- Tableau
- Excel
- SAP
- AWS
- Azure

### job_skills

Connects job postings with required skills.

One job posting may require multiple skills, and one skill may appear in many job postings.

### benefits

Stores standardized employee benefits.

Examples:

- Remote work
- Flexible working hours
- Training budget
- Company pension
- 30 vacation days

### job_benefits

Connects job postings with offered benefits.