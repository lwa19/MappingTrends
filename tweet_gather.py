# Scraping Tweets as an initial file

# Note: We are limited to 7 days of archive searching with the free API
# https://developer.twitter.com/en/pricing

# https://developer.twitter.com/en/docs/developer-utilities/twitter-libraries
## python-twitter by the Python-Twitter Developers
## tweepy by the tweepy Developers
## twitter by the Python Twitter Tools developer team
## TwitterSearch by @ckoepp
## twython by @ryanmcgrath and @mikehelmick
## TwitterAPI by @geduldig

# https://stackabuse.com/accessing-the-twitter-api-with-python/
# https://stackoverflow.com/questions/3577399/python-twitter-library-which-one

# http://www.mikaelbrunila.fi/2017/03/27/scraping-extracting-mapping-geodata-twitter/
# https://www.earthdatascience.org/courses/earth-analytics-python/using-apis-natural-language-processing-twitter/get-and-use-twitter-data-in-python/

# Let's use Tweepy

# import necessary libraries
import tweepy


# obtain consumer and access keys from json



auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


# authenticate API
api = tweepy.API(auth)

# The Cursor -> tweepy.Cursor()
# Apparently this is a thing that manages pagination for you
# You use it with the twitter API methods
# Example:
# tw.Cursor(api.search, q=search_words, lang="en", since=date_since).items(5)
# Basically you put the api method as api.method, and then you fill the rest of the
# parentheses with the arguments


public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)

# First get trend objects to find popular hashtags
# https://developer.twitter.com/en/docs/trends/trends-for-location/api-reference/get-trends-place

# After this we can search tweets by hashtag
# https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets



