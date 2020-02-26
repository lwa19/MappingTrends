 # Scraping Tweets as an initial file

# Note: We are limited to 7 days of archive searching with the free API
# https://developer.twitter.com/en/pricing

# http://www.mikaelbrunila.fi/2017/03/27/scraping-extracting-mapping-geodata-twitter/
# https://www.earthdatascience.org/courses/earth-analytics-python/using-apis-natural-language-processing-twitter/get-and-use-twitter-data-in-python/

# Let's use Tweepy
# http://docs.tweepy.org/en/latest/api.html

# import necessary libraries
# from datetime import datetime
import tweepy as tw
import pandas as pd
import datetime
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
# Note: Only use this for methods that give results involving pagination

'''
# An example of how api is used:
public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)
'''

# Tips for JSON readability
# Install Notepad++
# Plugins -> Plugins Admin -> Install JSON Viewer
# Open JSON file then go to plugins -> JSON Viewer -> Format JSON

##### REMOVED DUE TO RESTRUCTURING FRAMEWORK
#
# def get_data(locations, promoted=False):
#     '''
#     Function that requests and saves a batch of trend data.

#     Inputs:
#         locations: list of woeids for the desired locations
#         promoted: boolean on whether to include promoted tweets
#     '''
#     # Get trends for a location (loop over all locations)
#     # Note: Need to have a list of US woeids as our default batch
#     # Get tweets for each trend (loop over all trends)

#     # Question of if we're keeping track of trends by location or
#     # if we're just getting global trends then mapping tweet volume spread
#     for woeid in locations:
#         trends = get_trends(woeid)

#         for trend in trends.name:
#             search_words(trend)


def get_trends(woeid=23424977):
    '''
    Optional function. Not part of the program's primary use but useful
        to get starting points

    Get current trends for a particular location.
    Saves as json file with current date and time.
    Returns trend data as a pandas dataframe.

    Note: There is no way to get past trends without using third party
    archive websites, which only save trend names.

    https://developer.twitter.com/en/docs/trends/trends-for-location/api-reference/get-trends-place
    http://docs.tweepy.org/en/latest/api.html#trends-methods

    Inputs:
        woeid (int): "where on earth id" a 32-bit integer identifier for
            any location on earth (default=entire US)

    Outputs:
        json file saved with current date and time
        trend_info: pandas dataframe w/columns for trend name, tweet volume,
            and promoted content info
    '''
    # trends_json = api.trends_place(woeid)

    # dt = datetime.now()
    # formatted_dt = dt.strftime("%Y-%m-%d_%H.%M")
    # # tw_datetime = trends_json[0]["created_at"] # issue with colon character
    # filename = "trends_{}_{}.json".format(woeid, formatted_dt)
    # with open(filename, "w") as output_file:
    #     json.dump(trends_json, output_file)

    # trends = trends_json[0]["trends"] # list of dictionaries

    # trend_info = pd.read_json(trends)
    # trend_info.drop(columns=["url", "query"], inplace=True)
    # trend_info.replace(None, False, inplace=True)

    # return trend_info

######### Should be replaced by Leah's simpler function #####################
######### Reuse concept for counting code in separate counting function #####

# def search_words(input_hashtag, day_since=None, limit=100):
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

    Returns:
        tweets: a collection of tweets in "SearchResults" object
        location_counts (dict): number of tweets for each location (for available data)
        geotagged_ratio (float): proportion of tweets that are geotagged
        profile_geotagged-ratio (float): proportion of tweets where user has profile location
    '''
    # sample_size = 0
    # geotags = 0
    # profile_locs = 0
    # # valid profile_locs = 0
    # tweets_with_locations = 0
    # location_counts = {}

    # tweets = tweepy.Cursor(api.search, q=search_words, lang="en").items(limit)

    # for tweet in tweets:
    #     sample_size += 1
    #     geotagged = False
    #     profile_geotagged = False

    #     # https://simplemaps.com/data/us-cities
    #     # add to location counts for each location

    #     if tweet["geo"] is not None:
    #         geotags += 1
    #         tweets_with_locations += 1

    #         # map geotags/profile locs to states/cities

    #         if location in location_counts:
    #             location_counts[location] = 1
    #         else:
    #             location_counts[location] += 1
    #         geotagged = True

    #     if tweet["user"]["location"] is not None:
    #         profile_locs += 1
    #         tweets_with_locations += 1

    #         # map geotags/profile locs to states/cities

    #         if location in location_counts and not geotagged:
    #             location_counts[location] = 1
    #         else:
    #             location_counts[location] += 1

    # geotagged_ratio = geotagged / tweets_with_locations
    # profile_geotagged_ratio = profile_geotagged / tweets_with_locations

    # return tweets, location_counts, geotagged_ratio, profile_geotagged_ratio


# The results will be in a JSON file
# https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/intro-to-tweet-json


def convert_location(data, scale="state"):
    '''
    Given a scale input of county or state:
        Assigns country/state location to each geotagged tweet.
        Recognizes cities from profile locations and assigns their
          corresponding county/state to the tweet.

    Inputs:
        data: a json file
        scale (str): sets scale to convert locations to
          only county/state recognized)

    Outputs:
        output_data: a json file with the state_loc or county_loc
          fields added to each tweet
    '''
    location_data = pd.read_csv("locations/uscities.csv")

    # for tweet in batch:

    #     geotag = tweet["place"]["name"]
    #     home_location = tweet["user"]["location"]

    #     if geotag:
    #         to_convert = geotag
    #     elif:
    #         to_convert = home_location