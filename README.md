# lockdown-paper

## Tasks

### Sai - Hydrate Tweets 
from https://ieee-dataport.org/open-access/coronavirus-covid-19-geo-tagged-tweets-dataset

1. Latest JSON is here: /data/tweet/april28-june3.json
2. Sample code is here: /code/hydrate_tweets.py
3. Need to output as CSV - NOTE: Since status may have ',' - DOUBLE_QUETE all CSV fields

|ID|status|Country|City|Type|Sentiment|
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |

1. ID - original tweet id in the JSON first value in record (see hydrate_tweets.py code Line 14)
2. status - Tweet Text 
3. Country|City|Type - tweet.place.country_code, tweet.place.name, tweet.place.place_type
4. Sentiment - second field in the JSON (see hydrate_tweets.py code Line 15)

### Subhas - Set-up LDA
