import json
import tweepy
import pandas as pd
import sys

auth = tweepy.OAuthHandler('41t43pHXAP36syFu4bwolohZx', 'B1UQytW8diMBppbB4LEPQ5CbwL1lFa09TB2zdihdGCAsCQpru1')
auth.set_access_token('166182762-7m8FaI0pj09l1sRmX51wsnWWP2I7VLj0PPA0l3Op', 's3Dxguueiay4IWsV5iSjWC0ol51yqgNFBroUMXtXUG7JM')
api = tweepy.API(auth,wait_on_rate_limit =True)


#load file
with open('../data/tweet/april28-june3.json', 'r') as f:
  data = json.load(f)
  tweets = data['rows']
  # tweet = api.get_status(tweets[0][0])

  errorList=[]
  count=0
  df = pd.DataFrame(columns=['ID','Status','Country','City','Type','Sentiment'])
  length=len(tweets)
  
  for t in tweets:
      try:
        count+=1
        progress = count/len(tweets)
        sys.stdout.write("Download progress: %d / %d\r"%(count,length))
        sys.stdout.flush()
        id = t[0]
        sentiment = t[1]
        tweet = api.get_status(id)
        tweetEntry = {'ID':t[0], 'Status': tweet.text.replace(',','\',\''), 'Country': tweet.place.country, 'City': tweet.place.name, 'Type' : tweet.place.place_type, 'Sentiment' : t[1]}
        df = df.append(pd.DataFrame([tweetEntry]),  ignore_index=True)
      except Exception as e:
        errorMessage = "\ntweet #" + str(count) + "was not proccessed due to " + str(e)
        print(errorMessage)
        errorList.append({"count": count,"id" : t[0],  "msg" : str(e)})
        oldCount=0
        if(count-oldCount>10):
          oldCount=count
          f = open("error.json", "w")
          f.write(str(errorList))
          f.close()

  sys.stdout.write("Writing to csv\n")
  df.to_csv("../data/tweet_processed/april28-june3.csv", sep=',',index=False)
  sys.stdout.write("Process Completed!")