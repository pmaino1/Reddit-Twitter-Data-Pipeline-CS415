import pymongo
import os
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import csv
from google.cloud import language_v1

def main():
  os.system('export GOOGLE_APPLICATION_CREDENTIALS="/home/tgabrie2/project-2-implementation-ds-415-team/cs415-project2-c1ebb7c627b0.json"')
  myclient = pymongo.MongoClient("mongodb://localhost:27017/")
  mydb = myclient["cs415"]

  store_collection = mydb["tweets_gcp"]
  cur = store_collection.find( { "gcp": None} )

  client = language_v1.LanguageServiceClient()

  i = 0
  for doc in cur:
    print(i)
    if i > 149990:
      print("exceeded max gcp")
      break

    text = doc['text']
    sentiment = 0
    magnitude = 0
    try:
      document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
      sentimentObj = client.analyze_sentiment(request={'document': document}).document_sentiment
      sentiment = sentimentObj.score
      magnitude = sentimentObj.magnitude
    except:
      e = 0
    

    ob = {
      "_id": doc['_id'],
      "text": text,
      "created_at": doc['created_at'],
      "hashtags": doc['hashtags'],
      "tagged": doc['tagged'],
      "gcp": sentiment,
      "mag": magnitude
    }
    filter = { '_id': doc['_id'] } 
    store_collection.replace_one(filter,ob)
    i = i + 1
    time.sleep(.020)

main()