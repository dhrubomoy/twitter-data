import json
import re
from textblob import TextBlob

with open('bc_tweets2.json') as f:
    data = json.load(f)

def clean(tweet):
    return ' '.join(re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)', ' ', tweet).split()) 

cleaned_tweets = []
for d in data:
    cleaned_tweets.append(clean(d['full_text']))

# ****************** Word Cloud ******************
from wordcloud import WordCloud
import matplotlib.pyplot as plt

wordcloud_texts = ' '.join(cleaned_tweets)
remove_words = 'Trans|Mountain|TransMountain|pipeline|Pipeline'
wordcloud_texts = re.sub(remove_words, '', wordcloud_texts)

wordcloud = WordCloud().generate(wordcloud_texts)
plt.figure(figsize=(12,10))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()


# ****************** Pie chart ******************
positive = 0
negative = 0
neutral = 0

for t in cleaned_tweets:
    analysis = TextBlob(t)
    if analysis.sentiment.polarity > 0:     # Positive
        positive += 1
    elif analysis.sentiment.polarity < 0:   # Negative
        negative += 1
    else:                                   # Neutral
        neutral += 1

# Data to plot
labels = 'Positive', 'Negative', 'Neutral'
sizes = [positive, negative, neutral]
colors = ['yellowgreen', 'lightcoral', 'lightskyblue']
explode = (0, 0, 0.1)  # explode 1st slice
 
# Plot
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140)
plt.title('Twitter Reaction on Trans Mountain Pipeline')
plt.axis('equal')
plt.show()
