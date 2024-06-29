# from selenium import webdriver
#
# browser = webdriver.Chrome()
# browser.get('http://selenium.dev/')



text="""
&nbsp;
Job details
Here’s how the job details align with your profile.
Pay
₹10,000 - ₹12,000 a month
Job type
Full-time
Shift and schedule
Day shift
&nbsp;
Location
Bengaluru, Karnataka
&nbsp;
Full job description
Job Description:

We are seeking a detail-oriented and efficient Data Entry Operator to join our team. The primary responsibility of this role is to input data into our systems accurately and promptly, ensuring the integrity and security of the data.

Qualification : High school diploma or equivalent / Any Graduate

Job Type: Full-time

Pay: ₹10,000.00 - ₹12,000.00 per month

Schedule:

Day shift
Education:

Bachelor's (Preferred)
Experience:

Microsoft Office: 1 year (Preferred)
total work: 1 year (Preferred)
Language:

English (Preferred)
Work Location: Remote

Expected Start Date: 15/06/2024"""
completion = client.chat.completions.create(
    model="mixtral-8x7b-32768",
    messages=[
        {
            "role": "user",
            "content": """extract data from this text in this json schema: {"jobdesc":"description of the job in 100 words if exist else fallback value will be None,"jobbenifits":"benifits of the job if exist else fallback value will be None","jobqualification":"qualification of the job if exist else fallback value will be None","jobskills":"skills needed for the job if exist else fallback value will be None example of jobskills example:python,javascript etc","joblocation":"what is the location of the job if exist else fallback value will be None"}"""+  f"""      text:{text}"""
        }
    ],
    temperature=1,
    max_tokens=1024,
    top_p=1,
    stream=False,
    response_format={"type": "json_object"},
    stop=None,
)

print(json.loads(completion.choices[0].message.content))