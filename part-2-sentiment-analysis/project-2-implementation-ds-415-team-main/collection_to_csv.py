import pymongo
from google.cloud import language_v1
import os
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import csv

def main():
  myclient = pymongo.MongoClient("mongodb://localhost:27017/")
  mydb = myclient["cs415"]

  collection = mydb["vader_gcp_comparison"]
  cur = collection.find()

  headers = ['_id','vader','gcp']
  rows = []

  for doc in cur:
    row = [doc['_id'],doc['vader'],doc['gcp']]
    rows.append(row)

  with open('vader_gcp_comparison.csv', 'w') as f: 
    write = csv.writer(f) 
    write.writerow(headers) 
    write.writerows(rows) 
  

main()
