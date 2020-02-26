###for streaming live data

import tweepy 
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json 

# obtain consumer and access keys from json
with open('twitter_credentials.json', 'r') as f:
    keys = json.load(f)

auth = tweepy.OAuthHandler(keys['CONSUMER_KEY'], keys['CONSUMER_SECRET'])
auth.set_access_token(keys['ACCESS_TOKEN'], keys['ACCESS_SECRET'])

# authenticate API
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

#overwrite already existing StreamListener class 
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)

    def on_error(self, status_code):
        if status_code == 420:
            return False


def stream_live(input_hashtag):
    '''
    This function is to stream the live tweets based on a given input hastag. 

    '''
    #starting a stream 
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
    myStream.filter(track = [input_hashtag], is_async = True)

    live_tweets_list = []
    for a_tweet in streamed_tweets:
        live_tweets_list.append(json.dumps(a_tweet._json))

    #convert tweets to json as in search_words
    file_name = input_hashtag + '.json'
    with open(file_name, 'w') as outfile:
        json.dump(live_tweets_list, outfile, indent = 4)

    return live_tweets_list




