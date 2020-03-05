### STREAMING LIVE DATA ###
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
    	try:
    		with open('tweets.json', 'a') as f:
    			f.write(data)
    			print(data)
    			return True
    	except BaseException as e:
    		print("Error on_data: %s" % str(e))
    		return True

    def on_error(self, status_code): 
        if status_code == 420:
            # to check if rate limit occurs
            return False
        print(status_code.text)

def stream_tweets(input_hashtag):
	listener = MyStreamListener()

	stream = tweepy.Stream(auth, listener)

	stream.filter(track = [input_hashtag])
	