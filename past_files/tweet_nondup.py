############## DO NOT MODIFY ###############
# referenced from https://medium.com/@pytholabs/parsing-tweets-effectively-with-tweepy-module-python-7c7b6b030524
# We want to be able to specify the min number of tweets and scrape 
# non-repeating tweets from there. 
import sys
import jsonpickle
import os

maxTweets = 1000 # Some arbitrary large number
tweetsPerQry = 100  # this is the max the API permits
fName = 'tweets.txt' # We'll store the tweets in a text file.

def geo_tweets(searchQuery, min_tweets, filter=None):


    # If results from a specific ID onwards are read, set since_id to that ID.
    # else default to no lower limit, go as far back as API allows
    sinceId = None

    places = []
    time = []
    tweets = []

    # If results only below a specific ID are, set max_id to that ID.
    # else default to no upper limit, start from the most recent tweet matching the search query.
    max_id = -1

    tweetCount = 0

    with open(fName, 'w') as f:
        while tweetCount > min_tweets:
            try:
                if (max_id <= 0):
                    if (not sinceId):
                        new_tweets = api.search(q=searchQuery, count=100)
                    else:
                        new_tweets = api.search(q=searchQuery, count=100,
                                                since_id=sinceId)
                else:
                    if (not sinceId):
                        new_tweets = api.search(q=searchQuery, count=100,
                                                max_id=str(max_id - 1))
                    else:
                        new_tweets = api.search(q=searchQuery, count=100,
                                                max_id=str(max_id - 1),
                                                since_id=sinceId)
                if not new_tweets:
                    
                    print("No more tweets found")
                    break
                for tweet in new_tweets:
                    
                    #add data to lists
                    
                    #1. created at
                    time.append((tweet.created_at.month,tweet.created_at.year))
                    
                    #location of user
                    places.append(tweet.user.location)
                    
                    #text of tweet
                    tweets.append(tweet.text)
                    
                    f.write(jsonpickle.encode(tweet.text, unpicklable=False) +'\n')
                    
                tweetCount += len(new_tweets)
                print("Downloaded {0} tweets".format(tweetCount))
                max_id = new_tweets[-1].id
            
            except tweepy.TweepError as e:
                # Just exit if any error
                print("some error : " + str(e))
                break

print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))