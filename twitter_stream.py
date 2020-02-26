### FOR STREAMING LIVE DATA ###

import tweepy as tw
from tw.streaming import StreamListener
from tw import API
from tw import Cursor 
from tw import OAuthHandler
from tw import Stream
import numpy as np 
import pandas as pd 
import json 

## AUTHENTICATING CLASS ##
class Authenticate(keys_file):

    def __init__(self, keys_file):
        self.key_file = keys_file
        self.auth = self.authenticate_app()
        self.api = self.give_api()

    def authenticate_app(self):
        with open(self.keys_file, 'r') as f:
            keys = json.load(f)
        auth = tw.OAuthHandler(keys['CONSUMER_KEY'], keys['CONSUMER_SECRET'])
        auth.set_access_token(keys['ACCESS_TOKEN'], keys['ACCESS_SECRET'])
        return auth

    def give_api(self):
        auth = self.auth
        api = tw.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        return api 

## LISTENER CLASS ## 
class MyStreamListener():
    
    def __init__(self, tweets_file):
        self.tweets_file = tweets_file

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
            # to check if rate limit occurs
            return False
        print(status_code.text)

## STREAMING CLASS ##
class StreamNProcess():
    
    def __init__(self):
        pass

    def stream_live(self, tweets_file, input_hashtag, keys_file):
        # starting a stream 
        listener = MyStreamListener(tweets_file)
        authenticator = Authenticate(keys_file)
        api = authenticator.api
        myStream = tw.Stream(auth = api.auth, listener=listener)

        # we should think about taking advantage of the track as well as location arguments 
        myStream.filter(track = [input_hashtag], is_async = True, locations = None, languages = None)


def main_streaming_function(tweets_file, input_hashtag, keys_file):

    twitter_streamer = StreamNProcess()
    twitter_streamer.stream_live(tweets_file, input_hashtag, keys_file)



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



