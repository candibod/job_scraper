import os
import json

from linkedin_scraper import JobSearch
from selenium import webdriver

JOB_RESULTS_STORE_FILENAME = "job_listings.json"


def save_results(results):
    results_string = json.dumps({"results": results})
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
    new_driver.get("https://www.linkedin.com/login")

    for cookie in cookies:
        new_driver.add_cookie(cookie)
    else:
        url = "https://www.linkedin.com/jobs/search/?currentJobId=3928387949&distance=25&f_E=3,4&f_JT=F&f_T=9,39,25201&"
        +"f_TPR=r604800&geoId=103644278&keywords=software developer engineer&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=R"
        job_search = JobSearch(driver=new_driver, base_url=url, close_on_complete=False, scrape=False)
        job_listings = job_search.search("")

        save_results(job_listings)


if __name__ == "__main__":
    main()
