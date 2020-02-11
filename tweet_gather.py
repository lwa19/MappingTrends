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
# from datetime import datetime
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

def get_data(locations, promoted=False):
    '''
    Function that requests and saves a batch of trend data.

    Inputs:
        locations: list of woeids for the desired locations
        promoted: boolean on whether to include promoted tweets
    '''
    # Get trends for a location (loop over all locations)
    # Note: Need to have a list of US woeids as our default batch
    # Get tweets for each trend (loop over all trends)

    # Question of if we're keeping track of trends by location or
    # if we're just getting global trends then mapping tweet volume spread
    for woeid in locations:
        trends = get_trends(woeid)

        for trend in trends.name:
            search_words(trend)


def get_trends(woeid=23424977):
    '''
    Get current trends for a particular location. 
    Saves as json file with current date and time.
    Returns trend data as a pandas dataframe.

    Note: There is no way to get past trends without using third party 
    archive websites, which only save trend names.

    https://developer.twitter.com/en/docs/trends/trends-for-location/api-reference/get-trends-place
    http://docs.tweepy.org/en/latest/api.html#trends-methods

    Inputs:
        woeid (int): "where on earth id" a 32-bit integer identifier for 
            any location on earth (default is woeid for entire US)

    Outputs: 
        json file saved with current date and time
        trend_info: pandas dataframe w/columns for trend name, tweet volume,
            and promoted content info
    '''
    trends_json = tw.Cursor(api.trends_place, woeid)

    # dt = datetime.now()
    # formatted_dt = dt.strftime("%Y/%m/%d_%H:%M")
    datetime = trends_json[0]["created_at"]
    filename = "trends/trends_{}_{}.json".format(woeid, datetime)
    with open(filename, "w") as output_file:
        json.dump(trends_json, output_file)

    trends = trends_json[0]["trends"] # list of dictionaries

    trend_info = pd.read_json(trends)
    trend_info.drop(columns=["url", "query"], inplace=True)
    trend_info.replace(None, False, inplace=True)

    return trend_info

def search_words(input_hashtag, day_since=None, limit=100):
    '''
    Use the cursor function to gather a collection of tweets associated with a hashtag
    (Function currently collects estimate of geotags/profile locs per dataset)
    
    https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets
    Inputs:
        input_hashtag (string): hashtag that the user entered (*potential: we could check to 
            see if they included '#')
        date_since (???) : optional parameter; specifies how long back in the tweet 
            history we're restricting the search to (*replace None with appropriate default value)
        ** What are other parameters we could include?

    Returns: a collection of tweets in "SearchResults" object
    '''
    # tweets = tw.Cursor(api.search,
    #           q=search_words,
    #           lang="en",
    #           #since=day_since
    #           ).items(limit)

    sample_size = 0
    geotags = 0
    profile_locs = 0
    # valid profile_locs = 0
    locations = 0
    location_counts = {}

    for tweet in tweepy.Cursor(api.search, q=search_words, lang="en").items(limit):
        sample_size += 1

        if tweet["geo"] is not None:
            geotags += 1
            locations += 1
        if tweet["user"]["location"] is not None:
            profile_locs += 1
            locations += 1

        # map geotags/profile locs to states/cities
        # https://simplemaps.com/data/us-cities
        # add to location counts for each location


    # should we save then process tweets, or process locations while
    #   parsing the search results?

              
    # return tweets

# The results will be in a JSON file
# https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/intro-to-tweet-json

