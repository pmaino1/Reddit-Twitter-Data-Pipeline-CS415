import json
import sys
import pymongo

def main():
  myclient = pymongo.MongoClient("---")
  mydb = myclient["cs415"]
  mycol_comp = mydb["compressed_timestamps"]
  mycol_comp_tweets = mydb["compressed_tweets"]
  mycol_comp_comments = mydb["compressed_comments"]
  mycol_comp_posts = mydb["compressed_posts"]
  
  timestamps = mycol_comp.estimated_document_count()
  tweets = mycol_comp_tweets.estimated_document_count()
  comments = mycol_comp_comments.estimated_document_count()
  posts = mycol_comp_posts.estimated_document_count()
  print("Compressed Timestamps: ")
  print(timestamps)
  print("Compressed Tweets: ")
  print(tweets)
  print("Compressed Comments: ")
  print(comments)
  print("Compressed Posts: ")
  print(posts)

main()