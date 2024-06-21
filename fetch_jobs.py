import os
import time
import json

from linkedin_scraper import JobSearch
from selenium import webdriver


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
        job_search = JobSearch(driver=new_driver, close_on_complete=False, scrape=False)
        # job_search contains jobs from your logged in front page:
        # - job_search.recommended_jobs
        # - job_search.still_hiring
        # - job_search.more_jobs

        job_listings = job_search.search("Software Developer Engineer")  # returns the list of `Job` from the first page

        print(job_listings)


if __name__ == "__main__":
    main()
