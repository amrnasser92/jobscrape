import requests
import json
import time
from requests.adapters import Retry,HTTPAdapter


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

response.status_code

ids=[]
ids
ids_saved

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


    for page in range(num_pages+2):
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
        print(response.status_code)
        data = json.loads(response.text)
        for job_id in data['data']:
            ids.append(job_id['id'])
        print('Collected :'+str(len(ids))+ ' job ids')     



get_ids()


for page in range(97,8196+2):
    time.sleep(2)
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

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.status_code)
    data = json.loads(response.text)
    for job_id in data['data']:
        ids.append(job_id['id'])
    print('Collected :'+str(len(ids))+ ' job ids')   

len(ids)    