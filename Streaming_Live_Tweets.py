#libraries
from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#twitter_credentials is a python file that contains my twitter API keys
import twitter_credentials

#Twitter API Client
class Twitter_client():

    def __init__(self, twitter_user=None):#None defaults to getting tweets from your own timeline
        self.auth = Twitter_Authenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        #Allow person of this code to specificy a user to get timeline tweets from
        self.twitter_user = twitter_user


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
    This ia a basic listener class that just captures and stores/write all tweets into a json file
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

if __name__ =='__main__':

    hash_tag_list = ['donald trump', 'hillary clinton', 'bernie sanders']
    fetched_tweet_filename = 'tweets.txt' #prefer json, it's easier to deal with this format but you can choose other format

    twitter_client = Twitter_client('PyData')
    print(twitter_client.get_user_timeline_tweets(1))
    #twitter_streamer = TwitterStreamer()
    #twitter_streamer.stream_tweets(fetched_tweet_filename, hash_tag_list)
    

    


