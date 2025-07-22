# 🔍 LinkedIn Job Scraper

A Python-based web scraper that collects job postings from LinkedIn's public job search pages using job title and location as search parameters.

## 📌 Features

- Scrapes job postings using LinkedIn's guest job search endpoint
- Extracts key job details:
  - Job Title
  - Company Name
  - Time Posted
  - Number of Applicants
- Saves data to a structured CSV file
- Built using `requests`, `BeautifulSoup`, and `pandas`

## 📂 Output

The scraper outputs a `jobs.csv` file with the following columns:
- `job_title`
- `company_name`
- `time_posted`
- `num_applicants`

## ⚙️ Dependencies

Install required Python libraries:

```bash
pip install requests beautifulsoup4 pandas
