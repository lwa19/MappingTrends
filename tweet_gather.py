# Scraping Tweets as an initial file

# Note: We are limited to 7 days of archive searching with the free API
# https://developer.twitter.com/en/pricing

# https://stackabuse.com/accessing-the-twitter-api-with-python/
# https://stackoverflow.com/questions/3577399/python-twitter-library-which-one

# http://www.mikaelbrunila.fi/2017/03/27/scraping-extracting-mapping-geodata-twitter/
# https://www.earthdatascience.org/courses/earth-analytics-python/using-apis-natural-language-processing-twitter/get-and-use-twitter-data-in-python/

# Let's use Tweepy
# http://docs.tweepy.org/en/latest/api.html

# import necessary libraries
import tweepy as tw
import json

# obtain consumer and access keys from json
with open('twitter_credentials.json', 'r') as f:
    keys = json.load(f)

auth = tw.OAuthHandler(keys['CONSUMER_KEY'], keys['CONSUMER_SECRET'])
auth.set_access_token(keys['ACCESS_TOKEN'], keys['ACCESS_SECRET'])

# authenticate API
api = tw.API(auth)

# The Cursor -> tweepy.Cursor()
# Apparently this is a thing that manages pagination for you
# http://docs.tweepy.org/en/latest/cursor_tutorial.html
# You use it with the twitter API methods
# Example:
# tweepy.Cursor(api.search, q=search_words, lang="en", since=date_since).items(5)
# Basically you put the api method as api.method, and then you fill the rest of the
# parentheses with the arguments

'''
# An example of how api is used:
public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)
'''

# First get trend objects to find popular hashtags
# https://developer.twitter.com/en/docs/trends/trends-for-location/api-reference/get-trends-place
# http://docs.tweepy.org/en/latest/api.html#trends-methods



# After this we can search tweets by hashtag and save the results
# https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets

def search_words(ui_input, day_since=None, limit=100):
    '''
    Use the cursor function to gather a collection of tweets associated with a hashtag

    Inputs:
        ui_input (string): hashtag that the user entered (*potential: we could check to 
            see if they included '#')
        date_since (???) : optional parameter; specifies how long back in the tweet 
            history we're restricting the search to (*replace None with appropriate default value)
        ** What are other parameters we could include?

    Returns: a collection of tweets in "SearchResults" object
    '''
    tweets = tw.Cursor(api.search,
              q=search_words,
              lang="en",
              since=day_since).items(limit)

# The results will be in a JSON file
# https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/intro-to-tweet-json


