#libraries
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#twitter_credentials is a python file that contains my twitter API keys
import twitter_credentials

class TwitterStreamer():
    '''
    class for streaming and processing live tweets.
    '''
    #instead of showing stream of tweets in the terminal, i'll save them into a file(fetched_tweet_filename)
    def stream_tweets(self, fetched_tweet_filename, hash_tag_list):
        #This handles twitter authentication and connection to the twitter streaming API.
        # listener will deal with the data/tweets as well as the  errors
        listener = StdOutListener()
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)

        stream = Stream(auth, listener)

        #Providing with a list of things/hashtags which if tweets contains any of these items, it will add to stream
        stream.filter(track=hash_tag_list)

class StdOutListener(StreamListener):
    '''
    This ia a basic listener class that just prints received tweets to stdout
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
        print(status)

if __name__ =='__main__':

    hash_tag_list = ['donald trump', 'hillary clinton', 'bernie sanders']
    fetched_tweet_filename = 'tweets.json' #prefer json, it's easier to deal with this format but you can choose other format

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweet_filename, hash_tag_list)
    

    


