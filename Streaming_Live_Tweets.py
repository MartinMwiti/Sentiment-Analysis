#libraries
from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from textblob import TextBlob #for sentiment analysis

import twitter_credentials #twitter_credentials is a python file that contains my twitter API keys
import numpy as np
import pandas as pd
import re #regular expression
import matplotlib.pyplot as plt


#Twitter API Client and the different functionalities
class Twitter_client():

    def __init__(self, twitter_user=None):#None defaults to getting tweets from your own timeline
        self.auth = Twitter_Authenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        #Allow person of this code to specificy a user to get timeline tweets from
        self.twitter_user = twitter_user
    
    def get_twitter_client_api(self):
        return self.twitter_client


    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweets in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweets)
        return home_timeline_tweets

#Twitter Authenticator
class Twitter_Authenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth

class TwitterStreamer():
    '''
    class for streaming and processing live tweets.
    '''
    def __init__(self):
        self.twitter_authenticator = Twitter_Authenticator()

    #instead of showing stream of tweets in the terminal, i'll save them into a file(fetched_tweet_filename)
    def stream_tweets(self, fetched_tweet_filename, hash_tag_list):
        #This handles twitter authentication and connection to the twitter streaming API.
        # listener will deal with the tweets as well as any occured errors
        listener = Twitter_Listener(fetched_tweet_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        #Providing with a list of Shashtags which if tweets contains any of these items, it will add to stream
        stream.filter(track=hash_tag_list)

class Twitter_Listener(StreamListener):
    '''
    This ia a basic listener class that just captures and stores/write all tweets into a file
    '''
    def __init__(self, fetched_tweet_filename):
        self.fetched_tweet_filename = fetched_tweet_filename

    def on_data(self, data): 
        try:
            with open(self.fetched_tweet_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print('Error on data: %s'%str(e))
        return True

    def on_error(self, status):
        if status == 420:
            #return False on_data method in case rate limit occurs.
            return False
        print(status)


class Tweet_Analyzer():
    '''
    Functionality for analyzing and categorizing content from tweets.
    '''
    def clean_tweet(self, tweet):
        #to remove all special characters/hyperlinks from tweets then return the results of the clean tweets
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))

        if analysis.sentiment.polarity > 0: #polarity which tells if a tweet is positive or negative in nature.
            return 1 #1 stands for 'Positive tweet'
        elif analysis.sentiment.polarity ==0:
            return 0 #0 stands for 'Neutral tweet'
        else:
            return -1 #-1 stands for negative tweet

    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])
        
        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets]) #device used to tweet
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        
        return df


if __name__ == '__main__':

    twitter_client = Twitter_client()
    tweet_analyzer = Tweet_Analyzer()

    api = twitter_client.get_twitter_client_api()

    tweets = api.user_timeline(screen_name = 'Zuku_WeCare', count=200)
    df = tweet_analyzer.tweets_to_data_frame(tweets)
    df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['tweets']])
    print(df.head(10))
    #print(dir(tweets[0])) #tweet info directory i.e all types of features we can get from a tweet

#Get average length over all tweets.
    #print (np.mean(df['len']))
#Tweet that received the most likes
    #print(np.max(df['likes']))
#Tweet that received the most retweets
    #print(np.max(df['retweets']))


#Time series - Visualizing tweet data
    #time_retweets = pd.Series(data=df['retweets'].values, index=df['date'])
    #time_retweets.plot(figsize=(16,4), label = 'retweets', legend= True)
    
    #time_likes = pd.Series(data=df['likes'].values, index=df['date'])
    #time_likes.plot(figsize=(16,4), label = 'likes', legend= True)

    #plt.show()


    #hash_tag_list = ['safaricom', 'mpesa', 'data bundles']
    #fetched_tweet_filename = 'tweets.csv' 

    #twitter_client = Twitter_client('Safaricom_Care')
    #print(twitter_client.get_user_timeline_tweets(1))
    #twitter_streamer = TwitterStreamer()
    #twitter_streamer.stream_tweets(fetched_tweet_filename, hash_tag_list)
    