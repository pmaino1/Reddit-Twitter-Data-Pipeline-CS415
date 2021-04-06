import pymongo
from google.cloud import language_v1
import os
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer



def main():
  os.system('')##replace this path to the key on your system

  os.system('$PATH')
  myclient = pymongo.MongoClient("mongodb://localhost:27017/")
  mydb = myclient["cs415"]
  ##collection = mydb["gcp_test"]
  collection = mydb["compressed_tweets"]
  store_collection = mydb["vader_gcp_comparison"]

  client = language_v1.LanguageServiceClient()

  cur = collection.find()
  i = 0
  for doc in cur:
    if i >= 1000:
      print("DONE")
      break
    #print (doc['data']['text'])
    #print(doc['data'])
    text = doc['data']['text']
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
    # print("Sentiment: {}, {}".format(sentiment.score, sentiment.magnitude))
    sia_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sia_obj.polarity_scores(text)
    ob = {
      "_id": doc['data']['id'],
      "vader": sentiment_dict['compound'],
      "gcp": sentiment.score
    }
    #print("VADER: ",sentiment_dict['compound'],"\nGCP: ",sentiment.score)
    print(ob)
    store_collection.insert_one(ob)
    i = i +1
    time.sleep(2)

main()

