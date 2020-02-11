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
from datetime import datetime
import tweepy as tw
import pandas as pd
import json

# obtain consumer and access keys from json
with open('twitter_credentials.json', 'r') as f:
    keys = json.load(f)

auth = tw.OAuthHandler(keys['CONSUMER_KEY'], keys['CONSUMER_SECRET'], \
    secure=True)
auth.set_access_token(keys['ACCESS_TOKEN'], keys['ACCESS_SECRET'], \
    secure=True)

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

def get_data(promoted=False):
    '''
    Function that 
    '''
    # Get trends for a location (loop over all locations)
    # Note: Need to have a list of woeids as our default batch collect for the whole US
    # Get tweets for each trend (loop over all trends)

def get_trends(woeid):
    '''
    Get the current trends for a particular location. Saves json file with current date and time
    and returns trend data as a pandas dataframe.

    This function can only get current trends. There is no way to get past trends without using
    third party archive websites, which only save trend names.

    Inputs:
        woeid (int): "where on earth id" a 32-bit integer identifier for any location on earth
        incl_promoted: boolean

    Outputs: 
        json file saved with current date and time
        trend_info: pandas dataframe with 
    '''
    trends = tw.Cursor(api.trends_place, woeid)

    dt = datetime.now()
    formatted_dt = dt.strftime("%Y/%m/%d_%H:%M")
    filename = "trends_{}.json".format(formatted_dt)

    with open(filename, "w") as output_file:
        json.dump(trends, output_file)

    trend_info = pd.read_json(trends)
    trend_info.drop(columns=["url", "query"], inplace=True)
    trend_info.replace("null", False, inplace=True)

    return None

def search_words(input_hashtag, day_since=None, limit=100):
    '''
    Use the cursor function to gather a collection of tweets associated with a hashtag

    Inputs:
        input_hashtag (string): hashtag that the user entered (*potential: we could check to 
            see if they included '#')
        date_since (???) : optional parameter; specifies how long back in the tweet 
            history we're restricting the search to (*replace None with appropriate default value)
        ** What are other parameters we could include?

    Returns: a collection of tweets in "SearchResults" object
    '''
    tweets = tw.Cursor(api.search,
              q=search_words,
              lang="en",
              #since=day_since
              ).items(limit)
    print(keys)
              
    return tweets

# The results will be in a JSON file
# https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/intro-to-tweet-json


    
  
# Functions we need:
# 

