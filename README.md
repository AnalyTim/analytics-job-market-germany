# 🇩🇪 German Analytics Job Market Analysis

## Project Overview

This is an end-to-end data analytics project exploring the German job market for Analytics-related positions.

The project collects job postings through a job-search API, transforms the raw JSON responses with Python and Pandas, and exports the results to CSV.

The next stages will include data cleaning, PostgreSQL storage, SQL analysis and an interactive Power BI dashboard.

---

## Project Goals

The project aims to answer the following questions:

- Which Analytics roles are most frequently advertised?
- Which companies hire Analysts most actively?
- Which German cities and federal states have the highest demand?
- Which technical skills are requested most often?
- Which BI tools and data technologies are most popular?
- How common are remote, hybrid and on-site positions?
- What salary ranges are offered when salary information is available?
- How does demand differ between Junior, Mid-level and Senior roles?

---

## Data Source

The current version collects job postings from the job-search interface of the German Federal Employment Agency.

Search configuration:

- Search query: `Analyst`
- Location: `Deutschland`
- Page size: `100`
- Automatic pagination: enabled

The number of available job postings changes over time. A recent test run collected more than 1,000 postings.

Generated CSV and JSON data files are excluded from Git because they can be recreated by running the collection script.

---

## Current Dataset Fields

The current collection pipeline extracts the following fields:

| Column | Description |
|---|---|
| `job_id` | Unique job reference number |
| `title` | Original vacancy title |
| `profession` | Profession category provided by the source |
| `company` | Employer name |
| `postal_code` | Postal code of the workplace |
| `city` | Workplace city |
| `state` | German federal state |
| `country` | Workplace country |
| `latitude` | Workplace latitude |
| `longitude` | Workplace longitude |
| `date_posted` | Publication date |
| `date_modified` | Last modification timestamp |
| `start_date` | Expected employment start date |

Additional fields such as job descriptions, employment type, skills, remote-work information and salary will be investigated during the next development stage.

---

## ETL Pipeline

```text
Job Search API
      ↓
Python Requests
      ↓
JSON Responses
      ↓
Automatic Pagination
      ↓
Data Transformation
      ↓
Pandas DataFrame
      ↓
Raw CSV Export
      ↓
Data Cleaning
      ↓
PostgreSQL
      ↓
SQL Analysis
      ↓
Power BI Dashboard
```

---

## Current Features

- Connects to the job-search API
- Searches for Analytics-related vacancies in Germany
- Downloads all available result pages automatically
- Handles pagination with 100 postings per request
- Extracts selected fields from nested JSON objects
- Converts the collected records into a Pandas DataFrame
- Exports the raw dataset as a semicolon-separated CSV
- Uses UTF-8 encoding for compatibility with German characters and Excel
- Keeps generated datasets outside Git version control

---

## Tech Stack

- Python
- Pandas
- Requests
- SQL
- PostgreSQL
- Power BI
- Git
- GitHub
- VS Code

---

## Repository Structure

```text
analytics-job-market-germany/

├── data
│   ├── raw
│   └── clean
│
├── docs
│   ├── data_dictionary.md
│   ├── database_schema.md
│   └── project_plan.md
│
├── python
│   └── collect_jobs.py
│
├── sql
├── powerbi
├── images
│
├── .gitignore
├── LICENSE
└── README.md
```

---

## How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/AnalyTim/analytics-job-market-germany.git
cd analytics-job-market-germany
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate
```

### 4. Install the required packages

```bash
pip install pandas requests
```

### 5. Run the collection pipeline

```bash
python python/collect_jobs.py
```

The generated dataset will be saved to:

```text
data/raw/jobs.csv
```

---

## Project Status

### Completed

- [x] Repository setup
- [x] Project documentation
- [x] Initial database design
- [x] Python development environment
- [x] API connection
- [x] Automatic pagination
- [x] JSON transformation
- [x] Pandas DataFrame creation
- [x] Raw CSV export

### In Progress

- [ ] Detailed vacancy data collection
- [ ] Data cleaning and normalization
- [ ] Skill extraction from job descriptions
- [ ] Job-title categorization
- [ ] PostgreSQL database implementation
- [ ] SQL analysis
- [ ] Power BI dashboard
- [ ] Final business insights

---

## Important Notes

- Generated data files are not stored in this repository.
- Search results may change between pipeline runs.
- The project is intended for learning, portfolio development and labour-market analysis.
- Source availability and API behaviour may change over time.

---

## Author

Created by [AnalyTim](https://github.com/AnalyTim)