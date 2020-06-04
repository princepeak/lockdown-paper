import json
import tweepy

auth = tweepy.OAuthHandler('41t43pHXAP36syFu4bwolohZx', 'B1UQytW8diMBppbB4LEPQ5CbwL1lFa09TB2zdihdGCAsCQpru1')
auth.set_access_token('166182762-7m8FaI0pj09l1sRmX51wsnWWP2I7VLj0PPA0l3Op', 's3Dxguueiay4IWsV5iSjWC0ol51yqgNFBroUMXtXUG7JM')
api = tweepy.API(auth)


#load file
with open('../data/tweet/april28-june3.json', 'r') as f:
  data = json.load(f)
  tweets = data['rows']
  for t in tweets:
      id = t[0]
      sentiment = t[1]
      try:
        tweet = api.get_status(id)
        print(tweet.text, tweet.place.place_type, )
      except:
        pass