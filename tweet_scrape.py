############ DO NOT MODIFY!!! -- LW ###############

import tweepy as tw
import json

# obtain consumer and access keys from json
with open('twitter_credentials.json', 'r') as f:
    keys = json.load(f)

auth = tw.OAuthHandler(keys['CONSUMER_KEY'], keys['CONSUMER_SECRET'])
auth.set_access_token(keys['ACCESS_TOKEN'], keys['ACCESS_SECRET'])

# authenticate API
api = tw.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# hashtag -> tweet collection (list of json objects)
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
        collection.append(json.dumps(entry._json))

    # write list into json file
    file_name = input_query + '.json'
    with open(file_name, 'w') as outfile:
        json.dump(collection, outfile)

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

    tweets = tw.Cursor(api.search, 
                       q=input_query,
                       lang='en'
                       ).items(1000)   
    
    # convert each tweet into a json object and add to collection (list)
    for entry in tweets:
        # print(type(entry))    --> <class 'tweepy.models.Status'>
   
        tweet = json.loads(json.dumps(entry._json))
        # Appending chosen tweet data:
        item = (tweet['created_at'],tweet['id_str'],tweet['text'], \
            tweet['user'], tweet['coordinates'], tweet['place'])

        if item[-2] or item[-1]:
            # then there is location data associated with this tweet
            collection.append(item)
            geotagged.append(item)
        
        elif item[3].location:
            collection.append(item)
            user_loc.append(item)
        
        if len(collection) >= min_count and len(geotagged) >= min_geo:
            break
    
    print(len(collection), len(geotagged), len(user_loc))
    tup = (collection, geotagged, user_loc)
    cats = ['all', 'geotagged', 'user_loc']
    
    for ind, lst in enumerate(tup):
        file_name = input_query + '_' + cats[ind] + '.json'
        json_str = json.dumps(lst, default=str)
        with open(file_name, 'w') as outfile:
            json.dump(json_str, outfile)

    return collection, geotagged, user_loc


def get_locations(tweets, tag='user'):
    '''
    Get location data from a list of tweets depending on category

    Inputs: 
        tweets (list): tweets with only essential information
        tag (str): one of 'user', 'coor', or 'geo' 

    Returns: a list of locations as strings (formatted strangely)
    '''
    locations = []

    for entry in tweets:

        if tag == 'user':
            locations.append(entry[3].location)
        elif tag == 'coor':
            locations.append(entry[-2])
        elif tag == 'geo':
            locations.append(entry[-1])
    
    return locations

