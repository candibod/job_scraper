import os
import time
import json

from linkedin_scraper import JobSearch
from selenium import webdriver

JOB_RESULTS_STORE_FILENAME = "job_listings.json"


def process_results(results=[]):
    # f = open(os.path.join(os.getcwd(), "job_listings_copy.json"), "r")
    # info = f.read()
    # data = json.loads(info)
    # results = data["results"]

    processed_results = []
    for result in results:
        job_details = {
            "job_id": result["job_id"],
            "job_title": result["job_title"],
            "job_location": result["location"],
            "job_role": result["job_role_summary"].split("\n")[3] if result["job_role_summary"] else "",
            "job_description": result["job_description"],
            "linkedin_url": result["linkedin_url"].split("/?")[0],
            "company_name": result["company"],
            "company_category": result["emp_category"],
            "company_emp_count": result["emp_count"],
            "hiring_manager_name": result["hiring_manager"]["name"].split("\n")[0].strip() if result["hiring_manager"] else "",
            "hiring_manager_url": result["hiring_manager"]["profile_url"] if result["hiring_manager"] else "",
            "posted_date": result["posted_date"].split(chr(183))[1].strip(),
            "applicant_count": result["posted_date"].split(chr(183))[2].strip(),
            "is_easy_apply": result["easy_apply"],
            "card_insight": result["card_insight"],
            "footer_info": result["footer_info"],
            "stack_summary": result["job_role_summary"].split("\n")[5] if len(result["job_role_summary"].split("\n")) > 5 else "",
            "timestamp": int(time.time()),
        }

        processed_results.append(job_details)

    return processed_results


def save_results(results):
    results_string = json.dumps({"results": process_results(results)})
    try:
        with open(os.path.join(os.getcwd(), JOB_RESULTS_STORE_FILENAME), "x") as file:
            file.write(results_string)
    except FileExistsError:
        with open(os.path.join(os.getcwd(), JOB_RESULTS_STORE_FILENAME), "w", encoding="utf-8") as f:
            f.write(results_string)


def main():
    f = open(os.path.join(os.getcwd(), ".session_info"), "r")
    session_info_text = f.readline()
    cookies_dict = json.loads(session_info_text)
    cookies = cookies_dict["cookies"]

    new_driver = webdriver.Chrome()
    new_driver.set_window_size(1600, 1000)
    new_driver.get("https://www.linkedin.com/login")

    job_listings = []
    for cookie in cookies:
        new_driver.add_cookie(cookie)
    else:
        page_count = 10
        current_page = 0
        while current_page < page_count:
            url = (
                "https://www.linkedin.com/jobs/search/?currentJobId=3928387949&distance=25&f_E=3,4&f_JT=F&f_T=9,39,25201&"
                "f_TPR=r86400&geoId=103644278&keywords=software developer engineer&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=R"
                "&start="
            ) + str(current_page * 25)
            # 86400 604800
            print("Scraping URL: ", url)
            job_search = JobSearch(driver=new_driver, base_url=url, close_on_complete=False, scrape=False)
            job_listings = job_listings + job_search.search()
            print("Fetched results")
            current_page += 1

        save_results(job_listings)


if __name__ == "__main__":
    main()
