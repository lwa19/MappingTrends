 # Scraping Tweets as an initial file

# Note: We are limited to 7 days of archive searching with the free API
# https://developer.twitter.com/en/pricing

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
# This doesn't always work. If it doesn't there's an issue with the
# JSON formatting that will probably screw the function up

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
        trend_info: pandas dataframe for trend data
    '''
    trends_json = api.trends_place(woeid)

    # getting date/time for filename
    dt = datetime.now()
    formatted_dt = dt.strftime("%Y-%m-%d_%H.%M")
    # tw_datetime = trends_json[0]["created_at"] # issue with colon character

    # writing file
    filename = "trends_{}_{}.json".format(woeid, formatted_dt)
    with open(filename, "w") as output_file:
        json.dump(trends_json, output_file, indent=4)

    trends = trends_json[0]["trends"] # list of dictionaries

    return pd.DataFrame(trends)


def search_words(input_query, limit=1000):
    '''
    Performs a generic query according to query input with no filtering.

    Input:
        input_query(str): a standard input to search bar
        limit(int): max of tweets returned

    Returns:
        a list of tweets, each in json format (a json file is also outputted)
    '''
    collection = []
    # gathering a collection of tweets. Output: tweepy.cursor.ItemIterator
    tweets = tw.Cursor(api.search,
                       q=input_query,
                       lang='en'
                       ).items(limit)

    # convert each tweet into a json object and add to collection (list)
    for entry in tweets:
        # print(type(entry))    --> <class 'tweepy.models.Status'>
        collection.append(entry._json)

    # get timestamp (twitter timestamp has colon, cannot be used for filename)
    dt = datetime.now()
    formatted_dt = dt.strftime("%Y-%m-%d_%H.%M")

    # write list into json file
    file_name = "tweets_{}_{}.json".format(input_query, formatted_dt)

    with open(file_name, 'a') as outfile:
        # do not use json.dumps anywhere because it will string the dict
        json.dump(collection, outfile, indent=4)

    return collection

def geo_tweets(input_query, min_count=100, min_geo=0):
    '''
    Filter for tweets with either geotag or profile location. Collected
    tweets only have relevant information (tweet.created_at,tweet.id_str,
    tweet.text, tweet.user, tweet.coordinates, tweet.place). Datetime is
    converted to string for json storage.

    Inputs:
        input_query (str): standard search bar input
        min_count (int): the minimum tweets want to be returned
        min_geo (int): the minimum geotagged tweets we want to be returned

    Returns: tuple of lists (all tweets, geotagged tweets, profile location
    tweets)
    '''
    collection = []
    geotagged = []
    user_loc = []
    num_searched = 0

    while len(collection) < min_count or len(geotagged) < min_geo:
        for tweet in api.search(q=input_query, count=100, lang='en'):
        # Appending chosen tweet data:
            item = (tweet.created_at, tweet.id_str, tweet.text, tweet.user, \
                    tweet.coordinates, tweet.place)

            if item[-2] or item[-1]:
                # then there is location data associated with this tweet
                collection.append(item)
                geotagged.append(item)

            elif item[3].location:
                collection.append(item)
                user_loc.append(item)

            num_searched += 1

    print(len(collection), len(geotagged), len(user_loc))
    tup = (collection, geotagged, user_loc)
    cats = ['all', 'geotagged', 'user_loc']

    # get timestamp (twitter timestamp has colon, cannot be used for filename)
    dt = datetime.now()
    formatted_dt = dt.strftime("%Y-%m-%d_%H.%M")

    for ind, lst in enumerate(tup):
        file_name = "{}_{}_{}.json".format(input_query, cats[ind], formatted_dt)
        json_str = json.dumps(lst, default=str)
        with open(file_name, 'w') as outfile:
            json.dump(json_str, outfile, indent=4)

    return collection, geotagged, user_loc


def read_location_info(database="uscities.csv"):
    '''
    Converts location data for all US cities into a dictionary format mapping
        them to states.

    Inputs: database (database from https://simplemaps.com/data/us-cities)
    Outputs:
        mapping_dict: maps cities (values) to states (keys)
        abbr_dict: maps state abbreviations (values) to states (keys)
    '''
    location_data = pd.read_csv(database)
    mapping_dict = {}
    abbr_dict ={}

    for index, row in location_data.iterrows():
        if row["state_name"] not in mapping_dict.keys():
            mapping_dict[row["state_name"]] = set()

        mapping_dict[row["state_name"]].add(row["city"])

        if row["state_name"] not in abbr_dict.values():
            abbr_dict[row["state_id"]] = row["state_name"]

    return mapping_dict, abbr_dict


def convert_location(tweet_data, mapping_dict, abbr_dict):
    '''
    Given a scale input of county or state:
        Assigns country/state location to each geotagged tweet.
        Recognizes cities from profile locations and assigns their
          corresponding county/state to the tweet.

    Inputs:
        tweet_data: a list of tweet-json dictionaries
        mapping_dict: a dictionary mapping cities (values) to states (keys)
        abbr_dict: a dictionary mapping abbreviations (keys) to states (values)

    Outputs:
        output_data: a json file with the state_loc or county_loc
          fields added to each tweet
    '''
    # initialise counts dictionary
    location_counts = {}
    for state in mapping_dict.keys():
        location_counts[state] = 0

    # if replacing the direct input with a file
    # with open(tweet_data) as input_file:
    #     tweet_data = json.load(input_file)

    for tweet in tweet_data:

        # geotag = tweet["place"]["name"]
        # home_location = tweet["user"]["location"]

        # check if geotag exists
        if tweet["place"]:
            # only considers tweets from US
            if tweet["place"]["country"] == "United States":
                coordinates = tweet["place"]["bounding_box"]["coordinates"]
                state = geotag_state(coordinates)
                if state:
                    location_counts[state] += 1

        # checks if home location field is filled
        elif tweet["user"]["location"]:
            home_location = tweet["user"]["location"]
            state = parse_home_location(home_location, mapping_dict, abbr_dict)
            if state:
                location_counts[state] += 1

    return location_counts

def geotag_state(coordinates):
    '''
    Determines the US state a set of coordinates corresponds to.
    '''

def parse_home_location(string, mapping_dict, abbr_dict):
    '''
    Recgonizes location phrases from a string (the user's home location).
    Priority is state abbreviation first, then state name, then city names.

    Inputs:
        string: the user's home location
        mapping_dict: {state_name: [list of cities], ...}
        abbr_dict: {state_abbr: state_name, ...}

    Output:
        state(str): the state the user's home location is associated with

    Problem cases (treated as program limitations):
        1) a city which contains a word for a state will be treated 
           as the state if no state is recognized
        2) if multiple cities have the same name, it will be treated as
           the first city it the dictionary it encounters
        3) if a city name contains the name of another city in it, it may
           recognize the substring first and return the state of that city
    '''
    for state in mapping_dict.keys():
        if state in string:
            return state

    for abbr, state in abbr_dict.items():
        if abbr in string:
            return state

    for state, cities in mapping_dict.items():
        for city in cities:
            if city in string:
                return state

    return None


