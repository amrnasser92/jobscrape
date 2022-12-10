import requests
import json
from requests.adapters import Retry,HTTPAdapter
import pandas as pd
import pickle
from datetime import datetime
import time


date_today = datetime.now().strftime('%b-%d-%Y')

print('Starting scraping')


url = "https://wuzzuf.net/api/search/job"

start_index = 0
page_size = 15

payload = json.dumps({
  "startIndex": 0,
  "pageSize": 5,
  "longitude": "0",
  "latitude": "0",
  "query": "",
  "searchFilters": {}
})
headers = {
  'Content-Type': 'application/json',
  'Referer': 'https://wuzzuf.net/search/jobs/?a=hpb&q=&start=1'

}

response = requests.request("POST", url, headers=headers, data=payload)

ids=[]
companies = []


def get_ids():

    url = "https://wuzzuf.net/api/search/job"


    session = requests.Session()
    retry = Retry(connect=3,backoff_factor=2)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://',adapter)
    session.mount('https://',adapter)

    start_index = 0
    page_size = 15

    headers = {
    'Content-Type': 'application/json',
    #'Referer': 'https://wuzzuf.net/search/jobs/?a=hpb&q=&start=1',


    }

    payload = json.dumps({
        "startIndex": 0,
        "pageSize": 15,
        "longitude": "0",
        "latitude": "0",
        "query": "",
        "searchFilters": {}
        })


    response1 = session.request("POST", url, headers=headers, data=payload)
    print(response1.status_code)
    data_init = json.loads(response1.text)
    count = data_init['meta']['totalResultsCount']
    print(count)
    num_pages = count//page_size
    left = count % page_size


    for page in range(1,num_pages+1):
        #time.sleep(2)
        print("Extracting page " + str(page))
        payload = json.dumps({
        "startIndex": start_index+page*page_size,
        "pageSize": page_size,
        "longitude": "0",
        "latitude": "0",
        "query": "",
        "searchFilters": {}
        })
        headers = {
        'Content-Type': 'application/json',
        'Referer': 'https://wuzzuf.net/search/jobs/?a=hpb&q=&start=1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
        }

        response = session.request("POST", url, headers=headers, data=payload)
        print('status',response.status_code)
        data = json.loads(response.text)
        for job_id in data['data']:
            ids.append(job_id['id'])
            companies.append(job_id['attributes']['computedFields'][1]['value'][0])
        print('Collected :'+str(len(ids))+ ' job ids')     




print(len(ids))
jobs = {}
jobs_error = {}


def job_details():

    for id in ids:
        url = f"https://wuzzuf.net/api/job?filter[other][ids]={id}"
        session = requests.Session()
        retry = Retry(connect=3,backoff_factor=2)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://',adapter)
        session.mount('https://',adapter)
        payload={}
        headers = {}

        response = session.request("GET", url, headers=headers, data=payload)
        print('Status: ',response.status_code)

        job_data = json.loads(response.text)

        print(job_data['data'][0]['attributes']['title'])
            
        jobs[job_data['data'][0]['id']] = {
        'title' : job_data['data'][0]['attributes']['title'],
        'country' : job_data['data'][0]['attributes']['location']['country']['name'],
        'city' : job_data['data'][0]['attributes']['location']['city']['name'],
        'min_salary' : job_data['data'][0]['attributes']['salary']['min'],
        'max_salary' : job_data['data'][0]['attributes']['salary']['max'],
        'currency_' : job_data['data'][0]['attributes']['salary']['currency'],
        'vacancies' : job_data['data'][0]['attributes']['vacancies'],
        'date_posted' : job_data['data'][0]['attributes']['postedAt'],
        'date_expire' :  job_data['data'][0]['attributes']['expireAt'],
        'tempWFH' : job_data['data'][0]['attributes']['tempWorkingFromHome'],
        'hot_score' : job_data['data'][0]['attributes']['hotScore'],
        'description' : job_data['data'][0]['attributes']['description'],
        'requirements' : job_data['data'][0]['attributes']['requirements'],
        'roles' : [value['name'] for value in job_data['data'][0]['attributes']['workRoles']],
        'types' : [value['displayedName'] for value in job_data['data'][0]['attributes']['workTypes']],
        'gender_pref' : job_data['data'][0]['attributes']['candidatePreferences']['gender'],
        'education_pref' : job_data['data'][0]['attributes']['candidatePreferences']['educationLevel']['name'],
        'bachelor_required' : job_data['data'][0]['attributes']['candidatePreferences']['requiresBachelorDegree'],
        'min_experience' : job_data['data'][0]['attributes']['workExperienceYears']['min'],
        #'company_id':job_data['data'][0]['relationships']['company']['data']['id']
        }
        try:
            jobs[job_data['data'][0]['id']]['company_id'] = job_data['data'][0]['relationships']['company']['data']['id']    
        except:
            jobs[job_data['data'][0]['id']]['company_id'] = None
        print('Collected '+str(len(jobs))+ ' jobs')


get_ids()
job_details()

print(len(jobs))
jobs_df = pd.DataFrame(jobs).transpose()
jobs_df.to_csv(f'jobs {date_today}.csv')
