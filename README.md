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

## Acknowledgements