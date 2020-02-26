### FOR STREAMING LIVE DATA ###

import tweepy 
from tweepy.streaming import StreamListener
from tweepy import API
from tweepy import Cursor 
from tweepy import OAuthHandler
from tweepy import Stream
import json 

## AUTHENTICATING CLASS ##
class Authenticate(keys_file):

    def __init__(self):
        pass

    def authenticate_app(self, keys_file):
        with open(keys_file, 'r') as f:
            keys = json.load(f)
        auth = tweepy.OAuthHandler(keys['CONSUMER_KEY'], keys['CONSUMER_SECRET'])
        auth.set_access_token(keys['ACCESS_TOKEN'], keys['ACCESS_SECRET'])
        return auth

    def give_api(self):
        auth = self.auth
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        return api 


## LISTENER CLASS ## 
class MyStreamListener(StreamListener):
    
    def __init__(self, tweets_file):
        self.tweets_file = tweets_file
    
    def on_status(self, status):
        print(status.text)

    def on_data(self, data):
        try:
            with open(self.tweets_file, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data: %s " % str(e))
        return True

    def on_error(self, status_code):
        if status_code == 420:
            return False


## STREAMING CLASS ##
class StreamNProcess():
    
    def __init__(self):
        self.authenticator = Authenticate()

    def stream_live(self, tweets_file, input_hashtag):
        #starting a stream 

        listener = MyStreamListener()
        auth = self.Authenticate.authenticate_app(keys_file)
        api = self.Authenticate.give_api(auth)
        myStream = tweepy.Stream(auth = api.auth, listener=listener)
        myStream.filter(track = [input_hashtag], is_async = True)


def main_streaming_function(tweets_file, input_hashtag):

    twitter_streamer = StreamNProcess()
    twitter_streamer.stream_live(tweets_file, input_hashtag)


'''
    live_tweets_list = []
    for a_tweet in streamed_tweets:
        live_tweets_list.append(json.dumps(a_tweet._json))

    #convert tweets to json as in search_words
    file_name = input_hashtag + '.json'
    with open(file_name, 'w') as outfile:
        json.dump(live_tweets_list, outfile, indent = 4)

    return live_tweets_list
'''



