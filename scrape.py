import requests
import json
from requests.adapters import Retry,HTTPAdapter
from wuzzuf import ids
import pandas as pd
import pickle



len(ids)
jobs = {}
jobs_error = {}



def job_details():

    for id in ids:

        if ids[id] not in jobs and ids[id] not in jobs_error:

            url = f"https://wuzzuf.net/api/job?filter[other][ids]={id}"

            session = requests.Session()
            retry = Retry(connect=3,backoff_factor=2)
            adapter = HTTPAdapter(max_retries=retry)
            session.mount('http://',adapter)
            session.mount('https://',adapter)
            payload={}
            headers = {}

            response = session.request("GET", url, headers=headers, data=payload)
            print(response.status_code)

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
            'company_id':job_data['data'][0]['relationships']['company']['data']['id']
            }
            try:
               jobs[job_data['data'][0]['id']]['company_id'] = job_data['data'][0]['relationships']['company']['data']['id']    
            except:
                jobs[job_data['data'][0]['id']]['company_id'] = None
            print('Collected '+str(len(jobs))+ ' jobs')


job_details()



print(len(jobs))
len(jobs_error)
jobs_df = pd.DataFrame(jobs).transpose()
pd.DataFrame(jobs_error).transpose()

x = 1970

len(jobs) + len(jobs_error)
ids[x] in jobs or ids[x] in jobs_error

with open('jobs_dict.pickle','wb') as f:
    pickle.dump(jobs,f)


with open('jobs_dicterror.pickle','wb') as f:
    pickle.dump(jobs_error,f)

jobs_df[['min_salary','city','max_salary']].groupby('city').mean().sort_values('min_salary')

jobs_df[['min_salary','max_salary','title']].sort_values('max_salary',ascending=False).head(50)['title']

jobs_df[jobs_df['company_id'] == None]

keys = list(jobs_error.keys())

jobs_error[keys[0]]['relationships']['company']['data']['id']



for key in keys:
    job = jobs_error[key]
    print(job['attributes']['title'])
    jobs[job['id']] = {
                'title' : job['attributes']['title'],
                'country' : job['attributes']['location']['country']['name'],
                'city' : job['attributes']['location']['city']['name'],
                'min_salary' : job['attributes']['salary']['min'],
                'max_salary' : job['attributes']['salary']['max'],
                'currency_' : job['attributes']['salary']['currency'],
                'vacancies' : job['attributes']['vacancies'],
                'date_posted' : job['attributes']['postedAt'],
                'date_expire' :  job['attributes']['expireAt'],
                'tempWFH' : job['attributes']['tempWorkingFromHome'],
                'hot_score' : job['attributes']['hotScore'],
                'description' : job['attributes']['description'],
                'requirements' : job['attributes']['requirements'],
                'roles' : [value['name'] for value in job['attributes']['workRoles']],
                'types' : [value['displayedName'] for value in job['attributes']['workTypes']],
                'gender_pref' : job['attributes']['candidatePreferences']['gender'],
                'education_pref' : job['attributes']['candidatePreferences']['educationLevel']['name'],
                'bachelor_required' : job['attributes']['candidatePreferences']['requiresBachelorDegree'],
                'min_experience' : job['attributes']['workExperienceYears']['min'],
                #'company_id':job['relationships']['company']['data']['id']
                }

    try:
        jobs[job['id']]['compayn_id'] = job['relationships']['company']['data']['id']  

    except:
        jobs[job['id']]['compayn_id'] = None 
