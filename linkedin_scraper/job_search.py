import os
from typing import List
from time import sleep
import urllib.parse

from .objects import Scraper
from . import constants as c
from .jobs import Job

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class JobSearch(Scraper):
    AREAS = ["recommended_jobs", None, "still_hiring", "more_jobs"]

    def __init__(self, driver, base_url="https://www.linkedin.com/jobs/", close_on_complete=False, scrape=True, scrape_recommended_jobs=True):
        super().__init__()
        self.driver = driver
        self.base_url = base_url

        if scrape:
            self.scrape(close_on_complete, scrape_recommended_jobs)

    def scrape(self, close_on_complete=True, scrape_recommended_jobs=True):
        if self.is_signed_in():
            self.scrape_logged_in(close_on_complete=close_on_complete, scrape_recommended_jobs=scrape_recommended_jobs)
        else:
            raise NotImplemented("This part is not implemented yet")

    def scrape_job_card(self, base_element) -> Job:
        job_div = self.wait_for_element_to_load(name="job-card-list__title", base=base_element)
        job_title = job_div.text.strip()
        linkedin_url = job_div.get_attribute("href")
        linkedin_id = base_element.get_attribute("data-job-id")
        company = base_element.find_element(By.CLASS_NAME, "artdeco-entity-lockup__subtitle").text
        location = base_element.find_element(By.CLASS_NAME, "job-card-container__metadata-wrapper").text
        footer_info = base_element.find_element(By.CLASS_NAME, "job-card-list__footer-wrapper").text
        try:
            card_insight = base_element.find_element(By.CLASS_NAME, "job-card-container__job-insight-text").text
        except Exception:
            card_insight = ""

        job = Job(
            linkedin_id=linkedin_id,
            linkedin_url=linkedin_url,
            job_title=job_title,
            company=company,
            location=location,
            card_insight=card_insight,
            footer_info=footer_info,
            scrape=False,
            driver=self.driver,
        )
        return job

    def scrape_logged_in(self, close_on_complete=True, scrape_recommended_jobs=True):
        driver = self.driver
        driver.get(self.base_url)
        if scrape_recommended_jobs:
            self.focus()
            sleep(self.WAIT_FOR_ELEMENT_TIMEOUT)
            job_area = self.wait_for_element_to_load(name="scaffold-finite-scroll__content")
            areas = self.wait_for_all_elements_to_load(name="artdeco-card", base=job_area)
            for i, area in enumerate(areas):
                area_name = self.AREAS[i]
                if not area_name:
                    continue
                area_results = []
                for job_posting in area.find_elements_by_class_name("jobs-job-board-list__item"):
                    job = self.scrape_job_card(job_posting)
                    area_results.append(job)
                setattr(self, area_name, area_results)
        return

    def get_categorized_top_card_info(self, base_element):
        # print(base_element)
        test = {}
        try:
            for index, element in enumerate(base_element):
                if str(element.text).lower().find("employees") > -1:
                    emp_info = element.text.split(chr(183))
                    test["emp_count"] = emp_info[0].split(" ")[0]
                    test["emp_category"] = emp_info[1].strip() if len(emp_info) > 1 else ""
                    continue

                test[index] = element.text
        except Exception:
            pass

        return test

    def get_unified_data_dict(self, job, **kwargs):
        job_details = {
            "job_id": job.linkedin_id,
            "linkedin_url": job.linkedin_url,
            "job_title": job.job_title.split("\n")[0],
            "company": job.company,
            "company_linkedin_url": job.company_linkedin_url,
            "location": job.location,
            "posted_date": kwargs["date_info"] if "date_info" in kwargs else job.posted_date,
            "applicant_count": job.applicant_count,
            "job_description": kwargs["desc"] if "desc" in kwargs else "",
            "easy_apply": True if "easy_apply" in kwargs and kwargs["easy_apply"].lower().find("easy") > -1 else False,
            "apply_url": "",
            "emp_count": kwargs["top_card"]["emp_count"] if "top_card" in kwargs and "emp_count" in kwargs["top_card"] else "",
            "emp_category": kwargs["top_card"]["emp_category"] if "top_card" in kwargs and "emp_category" in kwargs["top_card"] else "",
            "benefits": job.benefits,
            "card_insight": job.card_insight,
            "footer_info": job.footer_info,
            "top_card": kwargs["top_card"] if "top_card" in kwargs else {},
            "job_role_summary": kwargs["job_role_summary"] if "job_role_summary" in kwargs else "",
            "hiring_manager": kwargs["hiring_manager"] if "hiring_manager" in kwargs else {},
        }

        return job_details

    def get_hiring_manager_info(self, base_element):
        try:
            hiring_manager = base_element.find_element(By.CLASS_NAME, "hirer-card__hirer-information")
            hiring_manager_info = hiring_manager.find_element(By.CLASS_NAME, "app-aware-link")

            return {"name": hiring_manager_info.text, "profile_url": hiring_manager_info.get_attribute("href")}
        except Exception:
            return {}

    def return_text_from_div(self, classname, base_element):
        text = ""

        try:
            return base_element.find_element(By.CLASS_NAME, classname).text
        except Exception:
            pass

        return text

    def search(self, search_term: str = "") -> List[Job]:
        # Overriding the default wait time to 2sec
        self.WAIT_FOR_ELEMENT_TIMEOUT = 2
        url = self.base_url if self.base_url == "" else os.path.join(self.base_url, "search") + f"?keywords={urllib.parse.quote(search_term)}&refresh=true"
        self.driver.get(url)
        self.scroll_to_bottom()
        self.focus()
        sleep(self.WAIT_FOR_ELEMENT_TIMEOUT)

        job_listing_class_name = "jobs-search-results-list"
        job_listing = self.wait_for_element_to_load(name=job_listing_class_name)

        self.scroll_class_name_element_to_page_percent(job_listing_class_name, 0.3)
        self.focus()
        sleep(self.WAIT_FOR_ELEMENT_TIMEOUT)

        # self.scroll_class_name_element_to_page_percent(job_listing_class_name, 0.6)
        # self.focus()
        # sleep(self.WAIT_FOR_ELEMENT_TIMEOUT)

        # self.scroll_class_name_element_to_page_percent(job_listing_class_name, 1)
        # self.focus()
        # sleep(self.WAIT_FOR_ELEMENT_TIMEOUT)

        job_results = []
        for index, job_card in enumerate(self.wait_for_all_elements_to_load(name="job-card-list", base=job_listing)):
            """
            Get basic details like role, company name
            """
            job = self.scrape_job_card(job_card)

            """
            Click on the element to get the job description & full details about the posting
            """
            job_card.click()
            sleep(1)

            job_details_element = self.wait_for_element_to_load(name="jobs-search__job-details--wrapper")
            top_card_element = self.wait_for_all_elements_to_load(name="job-details-jobs-unified-top-card__job-insight", base=job_details_element)

            job_results.append(
                self.get_unified_data_dict(
                    job=job,
                    top_card=self.get_categorized_top_card_info(top_card_element),
                    easy_apply=self.return_text_from_div("jobs-apply-button--top-card", job_details_element),
                    desc=self.return_text_from_div("jobs-description-content__text--stretch", job_details_element),
                    job_role_summary=self.return_text_from_div("job-details-segment-attribute-card-two-pane", job_details_element),
                    date_info=self.return_text_from_div("job-details-jobs-unified-top-card__primary-description-container", job_details_element),
                    hiring_manager=self.get_hiring_manager_info(job_details_element),
                )
            )

        return job_results
