import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

title = "hr"  # Job title
location = "Nepal"  # Job location
start = 0           # Starting index for pagination
increment = 25      # Number of jobs per page, LinkedIn uses 25 by default

id_list = []

while True:
    print(f"Scraping jobs from start={start}...")
    list_url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={title}&location={location}&f_TP=3&start={start}"

    response = requests.get(list_url)
    if response.status_code != 200:
        print(f"Failed to get page at start={start}, status code: {response.status_code}")
        break

    list_soup = BeautifulSoup(response.text, "html.parser")
    page_jobs = list_soup.find_all("li")

    if not page_jobs:
        print("No more jobs found, stopping.")
        break

    for job in page_jobs:
        base_card_div = job.find("div", {"class": "base-card"})
        if base_card_div and base_card_div.get("data-entity-urn"):
            job_id = base_card_div.get("data-entity-urn").split(":")[3]
            if job_id not in id_list:
                print(f"Found job id: {job_id}")
                id_list.append(job_id)

    start += increment
    time.sleep(1) 
    
print(f"Total jobs found: {len(id_list)}")


job_list = []

for job_id in id_list:
    job_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
    job_response = requests.get(job_url)
    print(f"Scraping details for job {job_id} - Status code: {job_response.status_code}")

    job_soup = BeautifulSoup(job_response.text, "html.parser")
    job_post = {}

    try:
        job_post["job_title"] = job_soup.find("h2", {"class":"top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open text-color-text mb-0 topcard__title"}).text.strip()
    except:
        job_post["job_title"] = None

    try:
        job_post["company_name"] = job_soup.find("a", {"class": "topcard__org-name-link topcard__flavor--black-link"}).text.strip()
    except:
        job_post["company_name"] = None

    try:
        job_post["time_posted"] = job_soup.find("span", {"class": "posted-time-ago__text topcard__flavor--metadata"}).text.strip()
    except:
        job_post["time_posted"] = None

    try:
        job_post["num_applicants"] = job_soup.find("span", {"class": "num-applicants__caption topcard__flavor--metadata topcard__flavor--bullet"}).text.strip()
    except:
        job_post["num_applicants"] = None
    # try:
    #     job_description_div = job_soup.find("div", class_="show-more-less-html__markup")
    #     job_post["job_description"] = job_description_div.get_text(separator="\n").strip() if job_description_div else None
    # except Exception as e:
    #     job_post["job_description"] = None


    job_list.append(job_post)
    time.sleep(0.5)  

# Save to DataFrame and CSV
jobs_df = pd.DataFrame(job_list)
print(jobs_df.head())
print(list_url)
print(f"Total jobs scraped: {len(jobs_df)}")

jobs_df.to_csv('jobs.csv', index=False)
