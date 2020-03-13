 # Scraping Tweets as an initial file

# Note: We are limited to 7 days of archive searching with the free API
# https://developer.twitter.com/en/pricing

# http://www.mikaelbrunila.fi/2017/03/27/scraping-extracting-mapping-geodata-twitter/
# https://www.earthdatascience.org/courses/earth-analytics-python/using-apis-natural-language-processing-twitter/get-and-use-twitter-data-in-python/

# Let's use Tweepy
# http://docs.tweepy.org/en/latest/api.html

# import necessary libraries
from datetime import datetime, timedelta, timezone
import time
import os
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


def collect_data(search_term, mode, interval, duration):
    '''
    Master function that runs the necessary helper functions in sequence in
    response to the inputs given by the user.

    Inputs:
        search_term (str): input from the user
        mode (str): "past" (search historical tweets) or "live" (stream tweets)
        interval (int): size of time bins (minutes)
        duration (int): total length of time to collect data from (minutes)

    Outputs:
        tweet_data: list of dictionaries sent to GIS
        data_array: summary statistics table (rows: states, columns: time bins)

    Datetime offset-naive and offset-aware solved by link:
    '''
    now = datetime.now(timezone.utc)
    bins = time_bins(mode, now, interval, duration)

    if mode == "past":
        # Collect tweets from the past by popularity
        all_tweets = search_words(search_term, now)
        # all_tweets.reverse()
    if mode == "live":
        # stream tweets live (ascending time)
        all_tweets = stream_tweets(search_term, duration, now)

    # sort tweets into time intervals
    tweet_batches = sort_tweets(all_tweets, bins, search_term, now)

    # for each time interval, determine the number of tweets per state
    tweet_data = []
    mapping_dict, abbr_dict = read_location_info()
    for batch in tweet_batches:
        state_counts = convert_location(batch, mapping_dict, abbr_dict)
        tweet_data.append(state_counts)

    return tweet_data


def time_bins(mode, now, interval, duration):
    '''
    Determines the time bin for each batch of tweets

    Inputs:
        mode(str): "past" (search historical tweets) or "live" (stream tweets)
        now: datetime object for function run time
        interval (int): size of time bins (minutes)
        duration (int): total length of time to collect data from (minutes)

    Returns: a list of tuples with format (start_time, end_time) in datetime format.
    Each tuple represents a time interval
    '''
    # Calculate the number of intervals specified
    num_bins = int(float(duration) / interval)    # round down division

    # Convert to datetime workable format
    total_time = timedelta(minutes=duration)
    interval = timedelta(minutes=interval)

    # Determine the start time
    if mode == "past":
        start = now - total_time
    elif mode == "live":
        start = now

    # specify time intervals:
    bins = []
    for _ in range(num_bins):
        end = start + interval
        bins.append((start, end))
        start = end

    return bins


def search_words(input_query, now, limit=100, search_type="mixed"):
    '''
    Returns 1000 English tweets containing the searched word/hashtag.
    Result contains a mix of popular and recent tweets.

    Inputs:
        input_query(str): a word or hashtag
        now: datetime object
        limit(int): max number of tweets to return
        search_type: "mixed" or "recent" or "popular"

    Outputs:
        outfile: json file of streamed tweets for reference and archiving
        collection: list of tweet dictionaries

    Notes:
    Function is heavily crippled by the limitations of the standard search API.
    Very few tweets are marked "popular", and recent tweets are often only
    from the past few minutes. In addition, there is no argument for getting
    only tweets after a specified time. The function however works as it
    should and should produce good data with a Premium/Enterprise Search API.
    '''
    collection = []
    # gathering a collection of tweets. Output: tweepy.cursor.ItemIterator
    # excluding entities trims unneeded tweet info
    tweets = tw.Cursor(api.search,
                       input_query,
                       result_type=search_type,
                       lang="en",
                       include_entities=False
                       ).items(limit)

    # convert each tweet into a json object and add to collection (list)
    for entry in tweets:
        # print(type(entry))    --> <class 'tweepy.models.Status'>
        collection.append(entry._json)

    # get timestamp (twitter timestamp has colon, cannot be used for filename)
    formatted_dt = now.strftime("%Y-%m-%d_%H.%M")

    # write list into json file
    file_name = "searched_{}_{}.json".format(input_query, formatted_dt)
    with open(file_name, 'a') as outfile:
        # do not use json.dumps anywhere because it will string the dict
        json.dump(collection, outfile, indent=4)

    return collection


class MyStreamListener(tw.StreamListener):
    # Details about the StreamListener class
    # https://github.com/tweepy/tweepy/blob/master/tweepy/streaming.py

    def __init__(self):
        self.tweets = []

    def on_data(self, data):
        try:
            # json.loads() converts string dictionary to dictionary
            self.tweets.append(json.loads(data))
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            return True

    def on_error(self, status_code):
        if status_code == 420:
            # to check if rate limit occurs
            return False
        print(status_code)


def stream_tweets(input_hashtag, duration, now):
    '''
    Streams tweets that include a given hashtag for a certain amount of time.

    Inputs:
        input_hashtag(str): stream tweets containing this word
        duration(int): time to stream for (minutes)
        now: datetime object

    Outputs:
        outfile: json file of streamed tweets for reference and archiving
        streamed_tweets: list of tweet dictionaries
    '''
    # get sleep time in seconds
    wait_time = duration * 60

    listener = MyStreamListener()
    stream = tw.Stream(auth, listener)

    # start and stop stream
    stream.filter(track = [input_hashtag], is_async=True)
    time.sleep(wait_time)
    stream.disconnect()

    streamed_tweets = listener.tweets

    formatted_dt = now.strftime("%Y-%m-%d_%H.%M")
    file_name = "streamed_{}_{}.json".format(input_hashtag, formatted_dt)
    with open(file_name, 'a') as outfile:
        json.dump(streamed_tweets, outfile, indent=4)

    return streamed_tweets


def sort_tweets(batch, bins, search_term, now):
    '''
    Sorts a batch of tweets into given time interval bins.

    Inputs:
        tweets: a list of tweet-dictionaries
        bins: a list of start-end 2-tuples containing datetime objects
        search_term(str): the word that was searched
        now: datetime object

    Outputs:
        outfile: json files of tweets (one file per bin), in new folder
        tweets_by_interval: a list of lists of tweet-dictionaries
    '''
    tweets_by_interval = [ [] for i in enumerate(bins) ]

    for tweet in batch:
        # get time from tweet
        time = tweet['created_at']
        time = datetime.strptime(time, '%a %b %d %H:%M:%S %z %Y')

        # compare tweet and bin times and append to bin
        for ind_bin, timebin in enumerate(bins):
            start, end = timebin
            if start <= time <= end:
                tweets_by_interval[ind_bin].append(tweet)
                break

    # Create a new directory and put the divided json files into it
    formatted_dt = now.strftime("%Y-%m-%d_%H.%M")
    outdir = "{}_{}.json".format(search_term, formatted_dt)
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    # write file
    for ind_bin, timebin in enumerate(bins):
        file_name = "{}_{}.json".format(search_term, str(ind_bin))
        with open(os.path.join(outdir, file_name), 'a') as outfile:
            json.dump(tweets_by_interval[ind_bin], outfile, indent=4)

    return tweets_by_interval


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
    for abbr in mapping_dict.keys():
        location_counts[abbr] = 0

    # if replacing the direct input with a file
    # with open(tweet_data) as input_file:
    #     tweet_data = json.load(input_file)

    for tweet in tweet_data:
        # check if geotag exists
        if tweet["place"]:
            # only considers tweets from US
            if tweet["place"]["country"] == "United States":
                place = tweet["place"]["full_name"]
                # almost all geotagged locations in the US are of the form "city, ST"
                for abbr in mapping_dict.keys():
                    if abbr in place:
                        location_counts[abbr] += 1

        # checks if home location field is filled
        elif tweet["user"]["location"]:
            home_location = tweet["user"]["location"]
            state = parse_home_location(home_location, mapping_dict, abbr_dict)
            if state:
                location_counts[state] += 1

    del_keys = []
    for abbr, count in location_counts.items():
        if count == 0:
            del_keys.append(abbr)

    for abbr in del_keys:
        del location_counts[abbr]


    return location_counts


def parse_home_location(string, mapping_dict, abbr_dict):
    '''
    Recgonizes location phrases from a string (the user's home location).
    Priority is state abbreviation first, then state name, then city names.

    Inputs:
        string: the user's home location
        mapping_dict: {state_abbr: [list of cities], ...}
        abbr_dict: {state_name: state_abbr, ...}

    Output:
        abbr(str): the state id the user's home location is associated with

    Problem cases (treated as program limitations):
        1) a city which contains a word for a state will be treated
           as the state if no state is recognized
        2) if multiple cities have the same name, it will be treated as
           the first city it the dictionary it encounters
        3) if a city name contains the name of another city in it, it may
           recognize the substring first and return the state of that city
    '''
    # Case-sensitive and thus wil avoid picking up fragments in other words
    # eg. only recognises "IL" not "illness"
    for abbr in mapping_dict.keys():
        if abbr in string:
            return abbr

    for state, abbr in abbr_dict.items():
        if state in string:
            return abbr

    # Temporary. Possibly using a library to make this more efficient
    for abbr, cities in mapping_dict.items():
        for city in cities:
            if city in string:
                return abbr

    return None

# Will eventually be superseded by loading csv files with the results of this
# that we want instead of running this function every time
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
    # state_coords = {}

    for index, row in location_data.iterrows():
        state = row["state_name"]
        city = row["city"]
        abbr = row["state_id"]
        # pop = row["population"]
        # lat = row["lat"]
        # lng = row["lng"]

        if abbr not in mapping_dict.keys():
            mapping_dict[abbr] = set()
            abbr_dict[state] = abbr
            # state_coords[state] = (None, 0, None, None)

        mapping_dict[abbr].add(city)

        # if pop > state_coords[state][1]:
        #     state_coords[state] = (city, pop, lat, lng)

    return mapping_dict, abbr_dict

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

def geotag_state(coordinates):
    '''
    Determines the US state a set of coordinates corresponds to.
    '''
    return None

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