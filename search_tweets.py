import base64
import requests
import datetime
import time
import json
from datetime import timezone

client_key = 'YOUR CONSUMER KEY'
client_secret = 'YOUR CONSUMER SECRET'
dev_env_label = 'DEV ENVIRONMENT LABEL'

QUERY = 'Hydro Ottawa'
FROM_DATE = '201809211500'    # format 'yyyyMMddHHmm', From Sept 21, 3:00 PM
TO_DATE = '201809241500'      # To Sept 24, 3:00 PM
MAX_RESULTS = 100
MAX_REQUESTS = 30

key_secret = '{}:{}'.format(client_key, client_secret).encode('ascii')
b64_encoded_key = base64.b64encode(key_secret)
b64_encoded_key = b64_encoded_key.decode('ascii')
base_url = 'https://api.twitter.com/'
auth_url = '{}oauth2/token'.format(base_url)

auth_headers = {
    'Authorization': 'Basic {}'.format(b64_encoded_key),
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
}
auth_data = {
    'grant_type': 'client_credentials'
}
auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
access_token = auth_resp.json()['access_token']
search_headers = {
    'Authorization': 'Bearer {}'.format(access_token)    
}
# Search Tweets: Full-archive endpoint → provides Tweets from as early as 2006
partial_url = '{}1.1/tweets/search/fullarchive/' + dev_env_label + '.json'
search_url = partial_url.format(base_url)

def get_searched_tweet_data(query, fromDate=None, toDate=None, maxResults=None, next=None):
    search_params = {
        'query': 'Hydro Ottawa'
    }
    if(fromDate):
        search_params['fromDate'] = fromDate
    if(toDate):
        search_params['toDate'] = toDate
    if(maxResults):
        search_params['maxResults'] = maxResults
    if(next):
        search_params['next'] = next
    search_resp = requests.get(search_url, headers=search_headers, params=search_params)
    if "test" in search_resp.json():
        print(search_resp.json()['error'])
        exit()
    return search_resp.json()

# get the first set of tweets
data = get_searched_tweet_data(QUERY, FROM_DATE, TO_DATE, MAX_RESULTS)
print('Collected data from first page')
all_data = []

# store the first set of data (in the first page)
for d in data['results']:
    all_data.append(d)

i=0 
while(i<MAX_REQUESTS):
    # Time delay before we make another request to account for rate limit (maximum 30 requests/min for me)
    time.sleep(2.1)
    # get data from the next page by setting 'next' parameter
    data = get_searched_tweet_data(QUERY, FROM_DATE, TO_DATE, MAX_RESULTS, data['next'])
    print('data collected. i = ', i, 'next= ', data['next'])
    # store result
    for d in data['results']:
        all_data.append(d)
    i += 1

# Write data to file
with open('tweet_data.txt', 'w') as file:
    file.write(json.dumps(all_data))
