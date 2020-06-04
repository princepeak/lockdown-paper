# lockdown-paper

## Tasks

### Sai - Hydrate Tweets 
from https://ieee-dataport.org/open-access/coronavirus-covid-19-geo-tagged-tweets-dataset

1. Latest JSON is here: /data/tweet/april28-june3.json
2. Sample code is here: /code/hydrate_tweets.py
3. Need to output as CSV - NOTE: Since status may have ',' - DOUBLE_QUETE all CSV fields

|ID|status|Country|City|Type|Sentiment|Date
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |

1. ID - original tweet id in the JSON first value in record (see hydrate_tweets.py code Line 14)
2. status - Tweet Text 
3. Country|City|Type - tweet.place.country_code, tweet.place.name, tweet.place.place_type
4. Sentiment - second field in the JSON (see hydrate_tweets.py code Line 15)
5. Date - date of the tweet in mm/dd/yy format without leading zero 

### Subhas - Set-up LDA

## Backlog

1. We have decided to consider New York, New Jersey and Illinois from US. Need to decide the group of control states for each.
2. We have decided to take Italy and Spain - control group for both.
3. We have decided to go with Maharashtra from India - control group for this has to be determined.
4. Gather graphs and Twitter analytics for all 5.
5. Write
