### STREAMING LIVE DATA ###
### to use this section make sure to set which file to extract keys (keys_file), search term (input_hashtag)
###  and number of tweets (n_tweets) and then run just_stream

import tweepy
import json

### choose keys file ###
keys_file = 'twitter_credentials_template.json'

### authentication ###
with open(keys_file, 'r') as f:
    keys = json.load(f)

auth = tweepy.OAuthHandler(keys['CONSUMER_KEY'], keys['CONSUMER_SECRET'])
auth.set_access_token(keys['ACCESS_TOKEN'], keys['ACCESS_SECRET'])
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


### stream listener class ### 
class MyStreamListener(tweepy.StreamListener):
    
    def on_data(self, data):
        global tweet_count
        global n_tweets
        global stream
        if tweet_count < n_tweets:
            try:
                with open('tweets.json', 'a') as f:
                    f.write(data)
                    print(data)
                    tweet_count += 1
                    return True
            except BaseException as e:
                print("Error on_data: %s" % str(e))
                return True
        else:
            stream.disconnect()

    def on_error(self, status_code): 
        if status_code == 420:
            # to check if rate limit occurs
            return False
        print(status_code.text)

#inputs for this function would be the input hashtag as well as how many tweets we want:
tweet_count = 0
n_tweets = 10
input_hashtag = 'bernie'

listener = MyStreamListener()

stream = tweepy.Stream(auth, listener)

stream.filter(track = [input_hashtag])
	