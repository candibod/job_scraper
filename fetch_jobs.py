import os
import time
import json

from linkedin_scraper import JobSearch
from selenium import webdriver

JOB_RESULTS_STORE_FILENAME = "job_listings.json"

"""
@todo:
1. Run script to Create .logs/errors folder to store the screenshots of the errors
"""


def process_results(results=[]):
    # f = open(os.path.join(os.getcwd(), "job_listings_copy.json"), "r")
    # info = f.read()
    # data = json.loads(info)
    # results = data["results"]

    # Debug the following json to resolve error
    #     {'job_id': '3976376814', 'linkedin_url': 'https://www.linkedin.com/jobs/view/3976376814/?eBP=CwEAAAGRKLKZrZFUj0ZhEK2kLcAjw0ufvE5jhWm25qyUBLvTIXJWIRNm1srUlObTnpbEteND-Z9yEWBCv1B02JPJrG1GqHvNOxNrgqy3tXhpCs-nl2lhFlBM5sVa_xKmhVrH8tg13qWS6-MnRI8y6h43JFFlkaRguu_72lTtodUYB_Xig2F5lj2L_2OhcT8BMs54UeQxJrY-887aGOaxM67f6jkplsx2Y-x0hj-p_37m9uN6rRg_1vfPQM6V9cc95LUm6EAsC680jimxUi1Ej7h36kBkgSY1Oq4Y22hVcr6ziwMzhjoy4xd4fDiM3G4Li0pol-wsiYRPJxhhWJXYtU65Lm3l9bd4qHNv0grmii3rFvP04Fbf_cCuqBjc3gDx0oIskPsXBNkkXbEJFxZ0uZDhzp40NuK2CG4c8LeAi1xJhzeWa_L9ybAj9eknUJfv9X5KxsQyEf0B_RxB2xDmDPW130NX1klAVIXgp-Fh&refId=7drinRyN3RG1kihBnsEpjA%3D%3D&trackingId=LbDr8CvBMiqeSs7LJAs7EQ%3D%3D&trk=flagship3_search_srp_jobs', 'job_title': 'Senior Software Engineer', 'company': 'AvidXchange, Inc.', 'company_linkedin_url': None, 'location': 'Charlotte, NC (On-site)', 'posted_date': 'Charlotte, NC · Reposted 1 hour ago', 'applicant_count': None, 'job_description': "About the job\nJob Overview\n\nAvidXchange is seeking a Senior Software Engineer to build best-in-class products. You will collaborate, analyze, design, develop, test, maintain, and implement premier software while working with cross-et is everything. We are Connected as People, Growth Minded, and Customer Obsessed. These\u202fthree mindsets represent our culture – who we\u202fare, who we’ve always been, and they guide us\u202fto improve every day.\u202fSince our founding in 2000 in Charlotte, NC, we’ve created a compan
    # improve every day.\u202fSince our founding in 2000 in Charlotte, NC, we’ve created a company of over 1,600 teammates working in one of our 5 offices across the U.S., or remotely. AvidXchange is proud us data from our teammates and makes official what our teammates have known for years – tha
    # to be Certified™ as a Great Place to Work®. The prestigious recognition is based on anonymous data from our teammates and makes official what our teammates have known for years – that AvidXchange is a understands that business is people centric. Connecting with others as humans first allows Great Place to Work®.\n\nWho You Are\n\nA go-getter with an entrepreneurial mindset – that means you are not afraid of taking risks, winning big or facing the unknown. \nSomeone who understands that  our potential. \n\nWhat You’ll Get\n\nAvidXchange teammates (we call them AvidXers) get th
    # business is people centric. Connecting with others as humans first allows you to develop mutually beneficial working relationships. \nFocused on making a difference for our customers. AvidXchange exisnce, development programs, competitive benefits and equity options. At AvidXchange, we are ts to help solve complex problems for our customers so we can all realize our potential. \n\nWhat You’ll Get\n\nAvidXchange teammates (we call them AvidXers) get the perks and prestige of a publicly tact. If you want to help us grow while realizing your potential and creating stories you’llraded tech company paired with the flexibility of a founder-led startup. We help our AvidXers develop as professionals and as human beings, providing work/life balance, development programs, competitipetitive Healthcare \nHigh Deductible Heath Plan Option that has $0 monthly premium for teave benefits and equity options. At AvidXchange, we are building more than a tech company – we are building an experience. We remain committed to a culture where you can fully be 'you’ – connected withnEmployee Assistance Program (EAP) - Provides counseling services, legal and financial cons others, chasing big goals, and making a meaningful impact. If you want to help us grow while realizing your potential and creating stories you’ll tell for years, you’ve come to the right place.\n\nAvtal Leave: 8 weeks 100% paid by AvidXchange*** \nDiscounts on Pet, Home, and Auto insuranceidXers Enjoy\n\n18 days PTO* \n11 Holidays (8 company recognized & 3 floating holidays) \n16 hours per year of paid Volunteer Time Off (VTO) \nCompetitive Healthcare \nHigh Deductible Heath Plan Optio centers \nPerks at Work: free discount program that provides teammates the opportunity to n that has $0 monthly premium for teammate-only coverage \n100% AvidXchange paid Dental Base Plan Coverage\n100% AvidXchange paid Life Insurance \n100% AvidXchange paid Long-Term Disability \n100% Avi,250*****\nHybrid Workplace Flexibility\nFree parking\nFully granted from beginning of yeardXchange paid Short-Term Disability \nEmployee Assistance Program (EAP) - Provides counseling services, legal and financial consultations and health advocacy for Teammates and their eligible dependentdXchange is an equal opportunity employer. AvidXchange is committed to equal employment opps\nOnsite Health Clinic with Atrium Health** - available to Teammates and their eligible dependents\n401k Match up to 4% \nParental Leave: 8 weeks 100% paid by AvidXchange*** \nDiscounts on Pet, Home,mited to veteran status, race, color, religion, sex, sexual orientation, gender identity, g and Auto insurance \nBrightDime Financial Wellness Tool, offered free to teammates \nWeeCare Childcare Service: helps teammates find affordable daycare, childcare, and tutors 40% less expensive than ': '1,751', 'benefits': None, 'card_insight': '2 school alumni work here', 'footer_info': '
    # traditional daycare centers \nPerks at Work: free discount program that provides teammates the opportunity to save on items from electronics, movie tickets, car buying, vacations, and more \nOnsite gymore', 2: '2 school alumni work here', 3: 'Skills: Microsoft Azure, C#'}, 'job_role_summarym fitness center, yoga studio, and basketball court****\nTuition Reimbursement up to the federal maximum of $5,250*****\nHybrid Workplace Flexibility\nFree parking\nFully granted from beginning of year, pro-rated if hired mid-year\nCharlotte location only \nMust be full-time for at least 3 months\nCharlotte location only\nMust be full-time for at least one year \nEqual Employment Opportunity\n\nAvidXchange is an equal opportunity employer. AvidXchange is committed to equal employment opportunity in accordance with applicable federal, state, and local laws. AvidXchange will not discriminate against applicants for employment on any legally recognized basis. This includes, but is not limited to veteran status, race, color, religion, sex, sexual orientation, gender identity, gender expression, national origin, age and physical or mental disability.", 'easy_apply': False, 'apply_url': '', 'emp_count': '1,001-5,000', 'emp_category': 'Software Development ', 'emp_count_linkdn': '1,751', 'benefits': None, 'card_insight': '2 school alumni work here', 'footer_info': 'Promoted', 'top_card': {0: 'On-site\nMatches your job preferences, workplace type is On-site.\nFull-time\nMatches your job preferences, job type is Full-time.\nMid-Senior level', 1: 'Back-End C# Show more', 2: '2 school alumni work here', 3: 'Skills: Microsoft Azure, C#'}, 'job_role_summary': 'Details found in the job post\nRetrieved from the description\nDeveloper Role\nBack-End\nTechnology\nC#, HTML, Docker, Kubernetes, CSS, Azure', 'hiring_manager': {}}

    processed_results = []
    for result in results:
        try:
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
                "company_emp_count_linkdn": result["emp_count_linkdn"],
                "hiring_manager_name": result["hiring_manager"]["name"].split("\n")[0].strip() if result["hiring_manager"] else "",
                "hiring_manager_url": result["hiring_manager"]["profile_url"] if result["hiring_manager"] else "",
                "posted_date": result["posted_date"].split(chr(183))[1].strip(),
                "applicant_count": result["posted_date"].split(chr(183))[2].strip(),
                "is_easy_apply": result["easy_apply"],
                "card_insight": result["card_insight"],
                "footer_info": result["footer_info"],
                "stack_summary": result["job_role_summary"].split("\n")[5] if len(result["job_role_summary"].split("\n")) > 5 else "",
                "top_card_summary": "\n".join([i for i in result["top_card"].values()]),
                "timestamp": int(time.time()),
            }
        except Exception as e:
            print(e)
            print(result)
            continue

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
                "https://www.linkedin.com/jobs/search/?currentJobId=3977979024&distance=25&f_E=3,4&f_JT=F&f_T=9,39,25201&"
                "f_TPR=r604800&geoId=103644278&keywords=software developer engineer&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=R"
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
