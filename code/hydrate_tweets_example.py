import json
import tweepy
import csv

dateseg = 'april28-june3'

auth = tweepy.OAuthHandler('41t43pHXAP36syFu4bwolohZx', 'B1UQytW8diMBppbB4LEPQ5CbwL1lFa09TB2zdihdGCAsCQpru1')
auth.set_access_token('166182762-7m8FaI0pj09l1sRmX51wsnWWP2I7VLj0PPA0l3Op', 's3Dxguueiay4IWsV5iSjWC0ol51yqgNFBroUMXtXUG7JM')
api = tweepy.API(auth)

# open csv file
with open(f'../data/tweet_processed/{dateseg}.csv', mode='w') as out_file:
    #write csv heder

    csv_writer = csv.writer(out_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    csv_header = ['id','status','date','country','country_code','place','type','sentiment','fav','retweet','lang','source']
    csv_writer.writerow(csv_header)

    #load json file
    with open(f'../data/tweet/{dateseg}.json', 'r') as f:
      data = json.load(f)
      tweets = data['rows']
      for t in tweets:
          id = t[0]
          sentiment = t[1]
          try:
            tweet = api.get_status(id)
            status = tweet.text
            type = tweet.place.place_type
            country_code = tweet.place.country_code
            country = tweet.place.country
            place = tweet.place.name
            time = tweet.created_at
            fav = tweet.favorite_count
            retweet = tweet.retweet_count
            lang = tweet.lang
            source = tweet.source
            date  = time.strftime('%m/%d/%y')

            # write
            csv_data = [id, status, date, country, country_code, place, type, sentiment, fav, retweet, lang, source]
            csv_writer.writerow(csv_data)
          except Exception as e:
              print(e)
              pass