import tweepy
import json

consumer_key = 'CONSUMER KEY'
consumer_secret = 'CONSUMER SECRET'
access_token = 'ACCESS TOKEN'
access_token_secret = 'ACCESS TOKEN SECRET'

# Filter retweets
QUERY = 'marijuana canada -filter:retweets'    
FILE_NAME = './marijuana_tweets2.json'


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

all_data = []

done = 0
for tweet in tweepy.Cursor(api.search, 
        q=QUERY,
        tweet_mode='extended', 
        lang="en").items(50000):
    done += 1
    print(done)
    all_data.append(tweet._json)

with open(FILE_NAME, 'w') as file:
    file.write(json.dumps(all_data, indent=2))

print(len(all_data))








# ******* CLEAN DATA (only tweets/texts) AND SAVE TO A CSV FILE

# import json
# import os
# import re

# with open('bc_tweets2.json') as f:
#     data = json.load(f)

# def clean(tweet):
#     return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 

# with open('bc_tweets_cleaned.txt', 'a') as f1:
#     for d in data:
#         f1.write(clean(d['full_text']) + os.linesep)

