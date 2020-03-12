# MappingTrends
CMSC 12200 project: projecting geographical data on twitter trends onto GIS map. 

This project is a python, Django, and GIS based twitter scraper and mapper. The basic function is that it takes a search term, collects tweets either in live time or from the past 7 days, and returns a GIS heatmap of tweet counts in states. Resulting data and maps are displayed on the website in a slide format. 

This project is a part of the University of Chicago CMSC 12200 course. Program is written by tema Twitter Trolls, and advisor is Professor Matthew Wachs. 

### Team members: 
Pooja Barai (pbarai@uchicago.edu)

Wesley Hsu (hsuerfan@uchicago.edu)

Kunal Mahajan (xxx)

Lijia Wang (lwang19@uchicago.edu)

## Developer notes:

### required packages

```
pip3 install tweepy
pip3 install django
pip3 install geopandas
pip3 install shapefile
pip3 install descartes
*
```

### file structure

```
MappingTrends
| test_website/    - all of the Django implementation
    | static/      - CSS
        | main.css - file used to format the website
    | trendmap/    - all of the template and index
    | ui/          - URLs
    | manage.py    - the code used to run the website
| Plot_pngs/       - all of the output png files
| states_21basic   - all of the GIS data files *
| past_files       - all of the past files that we no longer need
| tweet_gather.py  - scraping and parsing tweets
| mapper.py        - visualizing the parsed tweet data
| twitter_credentials_template.json     - template for formatting your twitter access credentials
| states.shp       - shape file for the states*
| uscities.csv     - && 
| Project Proposal.pdf     - project proposal
```

## Workflow

### Django Inputs:
 - Search term
    - string of the word or phrase 
 - Mode 
    - Past: scrape tweets from upto 7 days ago
    - Live: stream tweets in live time
 - Time Intervals
    - to divide the total duration into time blocks
    - there are 3 units: minutes, hours, days
 - Duration
    - the total time duration for streaming/scraping

### Django Outputs:
 - GIS heatmap
    - there is one heatmap for each time block
    - they are displayed as png files as a slideshow
    - *
    - && 
 - Summary stats
    - a table of the exact numbers per state per time block
 - && possibly a histogram for counts per state 

### Twitter Scraper:
 - utilising the Twitter API 
    - authentication - access tokens are obtained from Twitter Developer 
    - tweepy is the python library utilised to access the Twitter API
 - Tweet Collection 
    - based on the input search term, scrapes or streams tweets for a specified time 
    - collected tweets are stored in a json file
    - archive all searches collected into &&
 - Time bins division
    - time bins are calculated according to total duration and interval sizes
    - iterate through the collected tweets and sort them into corresponding json files in a new folder

### GIS *

### Integration into Django && 



## Challenges

1. Access Tokens took a significantly long time to work. Despite the fact that we received an email about the approval of our Developer rights, we were unable to get authentication using the access tokens. This issue took several days to resolve.

2. The standard search in Twitter has a rate limit on scraping the past data. We were able to overcome the issue by adding the wait_on_rate_limit functionality. 

3. Functionality to filter for tweets with geo-information was attempted. However, duplicates were incurred and there was no easy way of resolving the issue, so this attempt was ditched and replaced. 

4. Disconnecting the stream for the streaming function was difficult to do because the API was unhelpful. Manually interrupting the stream was easy, but finding the disconnect code functionality took several frustrating hours. 

5. GIS*

6. Django took a while to understand conceptually, especially given that the documentation was not clear and easily understood. &&


## Acknowledgements

We appreciate Professor Matthew Wachs' help and direction and the materials taught in the course CMSC 12100-12200. 