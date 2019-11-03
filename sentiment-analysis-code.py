#libraries
from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from textblob import TextBlob  # for sentiment analysis

# twitter_credentials is a python file that contains my twitter API keys
import twitter_credentials
import numpy as np
import pandas as pd
import re  # regular expression
import matplotlib.pyplot as plt


#Twitter API Client and the different functionalities
class Twitter_client():

    # None defaults to getting tweets from your own timeline
    def __init__(self, twitter_user=None):
        self.auth = Twitter_Authenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

    def get_twitter_client_api(self):
        return self.twitter_client


#Twitter Authenticator
class Twitter_Authenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth


class Tweet_Analyzer():
    '''
    Functionality for analyzing and categorizing content from tweets.
    '''

    def clean_tweet(self, tweet):
        #to remove all special characters/hyperlinks from tweets then return the results of the clean tweets
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))

        # polarity which tells if a tweet is positive or negative in nature.
        if analysis.sentiment.polarity > 0:
            return 1  # 1 stands for 'Positive tweet'
        elif analysis.sentiment.polarity == 0:
            return 0  # 0 stands for 'Neutral tweet'
        else:
            return -1  # -1 stands for negative tweet

    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])

        #df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        # device used to tweet
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])

        return df


if __name__ == '__main__':

    twitter_client = Twitter_client()
    tweet_analyzer = Tweet_Analyzer()

    api = twitter_client.get_twitter_client_api()

    #tweets = api.user_timeline(screen_name='Zuku_WeCare', count=200)
#q will represent Specific hashtags of interest. It can mean company product or service.     
    # I'll use any comments that involves kplc that contains different sentiments
    tweets = api.search(q=['kplc', 'lights'], count=200)
    df = tweet_analyzer.tweets_to_data_frame(tweets)
    df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['tweets']])
    print(df.head(10))

        #Time series - Visualizing tweet data
    time_sentiment = pd.Series(data=df['sentiment'].values, index=df['date'])
    time_sentiment.plot(figsize=(16, 4), label='sentiment', legend=True)

    #time_likes = pd.Series(data=df['likes'].values, index=df['date'])
    #time_likes.plot(figsize=(16,4), label = 'likes', legend= True)

    plt.show()
