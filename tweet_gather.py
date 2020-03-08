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

# authenticate API
auth = tw.OAuthHandler(keys['CONSUMER_KEY'], keys['CONSUMER_SECRET'])
auth.set_access_token(keys['ACCESS_TOKEN'], keys['ACCESS_SECRET'])
api = tw.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def collect_data(search_term, mode, timespan, endpoint):
    '''
    "Go" function that runs the necessary helper functions in sequence in
    response to the inputs given by the user.
    '''
    bins = time_bins(mode, timespan, endpoint)
    # load mapping dict
    # load abbr dict
    tweet_data = []

    for period in bins:
        before, after = period

        if mode == "past"
            batch = search_words(search_term, before, after)
        elif mode == "live":
            # call stream start and stop functions
        state_counts = convert_location(batch, mapping_dict, abbr_dict)
        tweet_data.append(state_counts)

    data_array = pd.DataFrame(tweet_data)
    data_array = data_array.transpose()
    # name the bins

    return data_array


def time_bins(mode, timespan, endpoint):
    '''
    Determines the time bin for each batch of tweets
    '''

def search_words(input_query, lang="en", limit=1000, entities=False):
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
        # check if geotag exists
        # if tweet["place"]:
        #     # only considers tweets from US
        #     if tweet["place"]["country"] == "United States":
        #         coordinates = tweet["place"]["bounding_box"]["coordinates"]
        #         state = geotag_state(coordinates)
        #         if state:
        #             location_counts[state] += 1
        # need to check sth with geotag info consistency first

        # checks if home location field is filled
        # elif tweet["user"]["location"]:
        if tweet["user"]["location"]:
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

    # Case-sensitive and thus wil avoid picking up fragments in other words
    # eg. only recognises "IL" not "illness"
    for abbr, state in abbr_dict.items():
        if abbr in string:
            return state

    for state, cities in mapping_dict.items():
        for city in cities:
            if city in string:
                return state

    return None

# ARCHIVED FUNCTIONS

def get_trends(woeid=23424977):
    '''
    Optional function. Not part of the program's primary use but useful
    to get starting points

    Get current trends for a particular location.
    Saves as json file with current date and time.
    Returns trend data as a pandas dataframe.

    Note: There is no way to get past trends without using third party
    archive websites, which only save trend names.

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
    Reads in location data for US cities and returns dictionaries that map
    cities and state abbreviations to states, as well as a dictionary with the
    coordinates for the largest city by population in the state.

    Inputs: database (database from https://simplemaps.com/data/us-cities)
    Outputs:
        mapping_dict: {state1: {city1, city2 ...}, ...}
        abbr_dict: {id1: state1, ...}
        state_coords = {state1: (city, pop, lat, lon), ...}
    '''
    location_data = pd.read_csv(database)
    mapping_dict = {}
    abbr_dict = {}
    state_coords = {}

    for index, row in location_data.iterrows():
        state = row["state_name"]
        city = row["city"]
        abbr = row["state_id"]
        pop = row["population"]
        lat = row["lat"]
        lng = row["lng"]

        if state not in mapping_dict.keys():
            mapping_dict[state] = set()
            abbr_dict[abbr] = state
            state_coords[state] = (None, 0, None, None)

        mapping_dict[state].add(city)

        if pop > state_coords[state][1]:
            state_coords[state] = (city, pop, lat, lng)

    return mapping_dict, abbr_dict, state_coords


# NOTES

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

# Tips for JSON readability (if not indented during output)
# Install Notepad++
# Plugins -> Plugins Admin -> Install JSON Viewer
# Open JSON file then go to plugins -> JSON Viewer -> Format JSON
# This doesn't always work. If it doesn't there's an issue with the
# JSON formatting that will probably screw the function up

# Consider representing each state as an object of the State class to hold all
# the information instead.
# class State:
#     def __init__(self):
#         self.name = None
#         self.abbr = None
#         self.all_cities = set()
#         self.tweeted_cities = {} # {"city1": tweets, ...}
#         self.total_tweets = 0

# function that looks up coordinates for each city in self.tweeted_cities
# returns tuple of (cityname, tweets, lat, lng)