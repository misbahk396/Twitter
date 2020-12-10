import platform
print(platform.python_version())
import tweepy
#import csv
import pandas as pd
import re
from textblob import TextBlob
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

##input your credentials here
consumer_key = 'xgVTpvws8ti1631b4WFJO5G0M'
consumer_secret = 'TzMdCrrZMw6oGtvk0GAxCHqMoimGdAdcRZvInuxl1b6L692uZc'
access_token = '1273654845010882560-PQPdbIQXvmA7vHsbKl3C3YCmSn2pEB'
access_token_secret = 'kTvBXb2jVWaPw6TcXpc9OM1JJy7bYJ2WeqC2rAoWNgjT2'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

doc = []

search = input("Enter the # to search ")
noOfTweets = input("How many time do you want to search ")

# tweepy scrap tweets from twitter
for tweet in tweepy.Cursor(api.search, q=search, count=int(noOfTweets),
                           lang="en",
                           since="2020-07-12").items(int(noOfTweets)):

    # print (type(tweet.text))
    doc.append(tweet.text)
# df is dataframe of panda
df = pd.DataFrame(doc, columns=['Tweets'])
print(df)

##print (tweet.created_at, tweet.text)
##csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])
# In[14]:
def cleanTxt(text):
    text = re.sub(r'@[A-Za-z0-9]+', ' ', text)  # remove @ mentioned
    text = re.sub(r'#', ' ', text)  # removing the # symbol

    text = re.sub(r'RT[\s]+', ' ', text)  # removing RT
    text = re.sub(r'https?:\/\/.*[\r\n]*', ' ', text, flags=re.MULTILINE)
    # text = re.sub(r'https?:\/\/\s+','',text) #remove hyper links
    # text = re.sub(r'https','',text)
    text = re.sub(r':', ' ', text)  # removing the : symbol
    return text


df['Tweets'] = df['Tweets'].apply(cleanTxt)
df.head()

def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity

def getPolarity(text):
    return TextBlob(text).sentiment.polarity

df['subjectivity'] = df['Tweets'].apply(getSubjectivity)
df['Polarity'] = df['Tweets'].apply(getPolarity)

##
stopwords = set(STOPWORDS)
stopwords.add('CoronaVirusUpdate')
stopwords.add('Covid_19')
allWords = ' '.join([twts for twts in df['Tweets']])
wordCloud = WordCloud(width=2000, height=900, random_state=21, max_font_size=119, stopwords=stopwords).generate(
    allWords)
plt.imshow(wordCloud, interpolation="bilinear")
plt.axis("off")
plt.savefig("pic" + ".jpeg")
plt.show()


def getAnalysis(score):

    if score < 0:
        return 'Negative'

    elif score == 0:
        return 'Neutral'

    else:
        return 'Positive'

df['SentimentAnalysis'] = df['Polarity'].apply(getAnalysis)
df.to_excel('sentimentAnalysis.xlsx')
#df.shape()

counts = df['SentimentAnalysis'].value_counts().to_dict()
Neutral = counts.get('Neutral')
Negative = counts.get('Negative')
Positive = counts.get('Positive')
print('---')
print(Neutral)
print(Positive)
print(Negative)
def percentage(part):
    whole = df['SentimentAnalysis'].count()
    if part is None:
        return 0
    else:
        return 100 * float(part)/float(whole)

positivepercentage = percentage(Positive)
negativepercentage = percentage(Negative)
neutralpercetage = percentage(Neutral)

positivepercentage = format(positivepercentage, '.2f')
negativepercentage = format(negativepercentage, '.2f')
neutralpercetage = format(neutralpercetage, '.2f')

labels = ['Positive ['+str(positivepercentage)+'%] , Neutral ['+str(neutralpercetage)+'%] , Negative['+str(negativepercentage)+'%]']
size = [positivepercentage, neutralpercetage, negativepercentage]
colors = ['green', 'gold', 'red']
patches, texts = plt.pie(size, colors=colors, startangle=90)
plt.legend(patches, labels, loc="best")
plt.title('tweets in percentage ')
plt.axis('equal')
plt.tight_layout()
plt.show()