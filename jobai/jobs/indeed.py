from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import time
from datetime import datetime, timedelta
from .models import Jobs

from groq import Groq
import json

client = Groq(api_key="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")

def indeed_crawl():
    browser = webdriver.Chrome()
    job_urls=[]
    pageno=0
    for i in range(10):
        if i <2:
            time.sleep(5)
            browser.get(f'https://in.indeed.com/jobs?q=work+from+home&sc=0kf%3Acmpsec%28NKR5F%29%3B&start={pageno}')
            pageno = pageno + 10
            last_height = browser.execute_script("return document.body.scrollHeight")

            while True:
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # Wait for the new page segment to load
                time.sleep(2)
                new_height = browser.execute_script("return document.body.scrollHeight")


                if new_height == last_height:
                    break
                last_height = new_height

            job_cards = browser.find_elements(By.CSS_SELECTOR,"li.css-5lfssm.eu4oa1w0")

            for job_card in job_cards:
                try:
                    job_url = job_card.find_element(By.CSS_SELECTOR, "h2.jobTitle.css-198pbd.eu4oa1w0").find_element(By.TAG_NAME,"a").get_attribute("href")
                    job_post_txt = job_card.find_element(By.CSS_SELECTOR,"div.heading6.tapItem-gutter.css-193h767.eu4oa1w0").find_element(By.CSS_SELECTOR, "span.css-qvloho.eu4oa1w0").text.split("\n")[-1]
                    match = re.search(r'\d+', job_post_txt)
                    if match :
                        job_post_time = match.group()
                        days_before = job_post_time
                        current_date = datetime.now()
                        previous_date = current_date - timedelta(days=days_before)

                        # Format the previous date as a string (optional)
                        previous_date_str = previous_date.strftime('%d %B %Y')

                        job_urls.append({"url":job_url,"job_post_time":job_post_time})
                except:
                    job_urls.append({"url": job_url, "job_post_time": None})
        else:
            break

    def crawl_details(browser:webdriver,data):
        browser.get(data["url"])
        job_name = browser.find_element(By.CSS_SELECTOR,"div.jobsearch-JobInfoHeader-title-container.css-bbq8li.eu4oa1w0").text
        text = browser.find_element(By.CSS_SELECTOR,"div.jobsearch-JobComponent-description.css-10ybyod.eu4oa1w0")
        text_data = text.text
        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {
                    "role": "user",
                    "content": """extract data from this text in this json schema: {"jobdesc":"description of the job in 100 words if exist else fallback value will be None,"jobbenifits":"benifits of the job if exist else fallback value will be None","jobqualification":"qualification of the job if exist else fallback value will be None","jobskills":"skills needed for the job if exist else fallback value will be None example of jobskills example:python,javascript etc","joblocation":"what is the location of the job if exist else fallback value will be None","companyname":"name of the company posted the job if exist else fallback value will be None"}""" + f"""      text:{text_data}"""
                }
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False,
            response_format={"type": "json_object"},
            stop=None,
        )
        final_data = json.loads(completion.choices[0].message.content)
        final_data["job_posted_date"]=data["job_post_time"]
        final_data["jobname"]=job_name
        final_data["jobpostdate"] = data["job_post_time"]
        final_data["joburls"] = data["url"]

        return final_data

    final_lst=[]
    for i in job_urls:
        x=crawl_details(browser,i)

        #check if url already exist
        try:
            data1 = Jobs.objects.get(joburl=x["job"])
            print("data already exist")
            pass
        except:
            data1 = Jobs(jobname=x["jobname"],joburl=x["joburls"],jobdescription=x["jobdesc"],jobbenefit=x["jobbenifits"],jobqualification=x["jobqualification"],jobskills=x["jobskills"],joblocation=x["joblocation"],companyname=x["companyname"],jobpostdate=x["jobpostdate"])
            data1.save()
            print("data stored to database")



