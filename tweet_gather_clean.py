##### Clean code that ABSOLUTELY WORKS 
############ DO NOT MODIFY! ###############

import tweepy as tw
import json

# obtain consumer and access keys from json
with open('twitter_credentials.json', 'r') as f:
    keys = json.load(f)

auth = tw.OAuthHandler(keys['CONSUMER_KEY'], keys['CONSUMER_SECRET'])
auth.set_access_token(keys['ACCESS_TOKEN'], keys['ACCESS_SECRET'])

# authenticate API
api = tw.API(auth)

# hashtag -> tweet collection (list of json objects)
def search_words(input_hashtag, limit=100):
    collection = []
    # gathering a collection of tweets. Output: tweepy.cursor.ItemIterator
    tweets = tw.Cursor(api.search, 
                       q=input_hashtag,
                       lang='en'
                       ).items(limit)   
    
    # convert each tweet into a json object and add to collection (list)
    for entry in tweets:
        # print(type(entry))    --> <class 'tweepy.models.Status'>
        collection.append(json.dumps(entry._json))

    # write list into json file
    file_name = input_hashtag + '.json'
    with open(file_name, 'w') as outfile:
        json.dump(collection, outfile)

    return collection

