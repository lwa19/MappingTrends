# MappingTrends
CMSC 12200 project: projecting geographical data on twitter trends onto GIS map.

This project is a python, Django, and GIS based twitter scraper and mapper. The basic function is that it takes a search term, collects tweets either in live time or from the past 7 days, and returns a GIS heatmap of tweet counts in states. Resulting data and maps are displayed on the website in a slide format.

This project is a part of the University of Chicago CMSC 12200 course. Program is written by team Twitter Trolls, and advisor is Professor Matthew Wachs.

### Team members:
Pooja Barai (pbarai@uchicago.edu)

Wesley Hsu (hsuerfan@uchicago.edu)

Kunal Mahajan (xxx)

Lijia Wang (lwang19@uchicago.edu)

## Developer notes:

### required packages

```
pip3 install tweepy
pip3 install Django
pip3 install geopandas
pip3 install descartes
*
```

### file structure

```
MappingTrends
| website/             		- all of the Django implementation
	| states_21basic   	- all of the GIS data files *
    	| static/          	- website accessible files
		| archive/     	- tweet jsons for each search/stream query made, for easy reanalysis (with different intervals etc)
		| Plot_pngs/   	- all of the output png files
		| main.css     	- file used to format the website
    | trendmap/                	- all of the template and index
		| templates/   	- website html files
		| views.py     	- views file where the django input is processed and page is returned
    | ui/                      	- URLs
		| settings.py  	-
    	| manage.py            	- the code used to run the website
	| tweet_gather.py      	- scraping and parsing tweets
	| mapper.py            	- visualizing the parsed tweet data
| twitter_credentials_template.json     - template for formatting your twitter access credentials
| past_files           		- all of the past files that we no longer need
| states.shp           		- shape file for the states*
| uscities.csv         		- data source for US cities https://simplemaps.com/data/us-cities (Basic)
| Project Proposal.pdf 		- project proposal
```

## Workflow

### Django Inputs:
 - Search term
    - string of the word or phrase
 - Mode
    - Past: scrape tweets from up to 7 days ago
    - Live: stream tweets in live time
 - Time Intervals
    - to divide the total duration into time blocks
    - there are 3 units: minutes, hours, days
 - Duration
    - the total time duration for streaming/scraping

### Django Outputs:
 - GIS heatmap
    - there is one heatmap for each time block
    - they are displayed as png files in a slideshow
 - Summary stats
    - a table of the exact numbers per state per time block

### Twitter Scraper:
 - Utilising the Twitter API
    - authentication - access tokens are obtained from Twitter Developer
    - tweepy is the python library utilised to access the Twitter API
 - Tweet Collection
    - based on the input search term, performs search or streams tweets for a specified time
    - collected tweets are archived in a json file with name, mode (search/stream), time of generation, and duration (for live)
	- format is list of dictionaries
 - Time bins division
    - time bins are calculated according to total duration and interval sizes
    - iterate through the collected tweets and sort them into groups (list of lists of dictionaries)
	- archive as json files in a folder
 - Parse tweets
	- iterate through each tweet and extract locations from geotag or profile location
	- compare against city/state info from uscities.csv, match cities to states
	- for each tweet with an associated US state, add count to dictionary
	- repeat for each time bin, return as list of dictionaries

### GIS *

### Integration into Django
 - User Interface
   - Query screen shows a form and helper info
   - Form has four fields: search term, mode (live/past), time interval, and
      duration (both integer + time units)
   - Returns a slideshow of heatmap images and a table of statistics (time on
      rows, states on columns, counts in cells)
 - Processing
   - Converts time inputs to minutes
   - Checks that time inputs are within min/max bounds
   - Calls master function of tweet_gather.py to collect and process data
   - Calls master function of mapper.py to map processed data
   - Arranges output of tweet_gather into array
   - Sends array, png filepaths, form, and error outputs for rendering on page

## Challenges

1. Access Tokens took a significantly long time to work. Despite the fact that we received an email about the approval of our Developer rights, we were unable to get authentication using the access tokens. This issue took several days to resolve.

2. The standard search in Twitter has a rate limit on scraping the past data. We were able to overcome the issue partially by adding the wait_on_rate_limit functionality, though this extends the runtime very much should one search for more tweets than the API allows in an interval.

3. Functionality to filter for tweets with geo-information was attempted. However, duplicates were incurred and there was no easy way of resolving the issue, so this attempt was ditched and replaced.

4. Disconnecting the stream for the streaming function was difficult to do because the API documentation was unhelpful. Manually interrupting the stream was easy, but finding the disconnect code functionality took several frustrating hours.

5. Many of our earlier JSON outputs were incorrectly formatted for one reason or another. These included excessive amounts of \ escapes, the dictionaries being placed into a string, lack of indentation (not incorrect but unreadable by humans), or dictionaries being placed back to back without being in a larger list. This problem prevented other parts of our code from reading the JSON files (or the tweet outputs themselves prior to file writing). The various problems were fixed in turn and the style of JSON writing finally standardized.

6. GIS*

7. Django took a long time to really understand as it used a lot of unfamiliar concepts and the explanations available often seemed to assume more knowledge than we had. We used the PA3 Django code as a starting point both for creating our website and understanding Django beyond Lab 5, but the code there basically had no documentation and used even more unfamiliar concepts (super, *args, etc).

## Notable Limitations

1. Twitter's Standard Search API is quite limited in terms of the number of tweets returnable, and does not return a nice spread of tweets. As stated by twitter, it is also not designed for completeness of results (as opposed to Premium and Enterprise paid APIs). The most recent tweets make up the vast majority of tweets. While popular tweets can be returned, the number of tweets that are marked "popular" by twitter is extremely low, as evident when the result type is changed to "popular". The function works best for less popular search terms, but will be still expected to give worse results than tweet streaming.

2. The city recognition function is quite inefficient due to needing to check the home location string for every single city. As some cities are made up of more than one word, it is not enough to simply look up every word of the home location in the city set for each state.


## Acknowledgements

We appreciate Professor Matthew Wachs' help and direction and the materials taught in the course CMSC 12100-12200.
