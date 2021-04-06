import pymongo
from google.cloud import language_v1
import os
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import csv


## FROM GEEKS FOR GEEKS SEE PAPER SOURCE ##
def intersection(lst1, lst2): 
    # Use of hybrid method 
    temp = set(lst2) 
    lst3 = [value for value in lst1 if value in temp] 
    return lst3 

def main():
  myclient = pymongo.MongoClient("mongodb://localhost:27017/")
  mydb = myclient["cs415"]

  headers = ['subreddit','name','vader','upvotes','total']
  print(headers)
  rows = []

  people = [['biden'],['kamala','harris'],['trump','donald'],['pence']]
  names = ['Joe Biden','Kamala Harris','Donald Trump','Mike Pence']
  subreddits = ["politics", "news", "worldnews", "pics", "videos", "science", "technology",
            "sports", "upliftingnews", "philosophy", "twoxchromosomes", "democrats", "conservative", "libertarian", "republican",
            "liberal", "progun", "futurology", "economics", "socialism", "whitepeopletwitter", "blackpeopletwitter",
            "sandersforpresident", "atheism", "christianity", "politicalhumor", "selfawarewolves", "joebiden", "nottheonion",
            "teenagers", "latestagecapitalism", "lgbt", "unpopularopinion", "leopardsatemyface"]
  

  for subreddit in subreddits:
    p = 0
    for person in people:
      print(subreddit+" "+names[p])
      ##print("STARTING WITH: "+names[p])

      post_collection = mydb["posts_vader"]
      post_cur = post_collection.find()

      comment_collection = mydb["comments_vader"]
      comment_cur = comment_collection.find()

      weighted_sum_reddit_sent = 0;
      total_count = 0
      upvote_sum = 0

      

      for post in post_cur:
        inter = intersection(person,post['tagged'])
        if len(inter) > 0:
          if post['subreddit'] == subreddit:
            weighted_sum_reddit_sent = weighted_sum_reddit_sent + (post['vader']*post['upvotes'])
            total_count = total_count + 1
            upvote_sum = upvote_sum + post['upvotes']

      for comment in comment_cur:
        inter = intersection(person,comment['tagged'])
        if len(inter) > 0:
          if comment['subreddit'] == subreddit:
            weighted_sum_reddit_sent = weighted_sum_reddit_sent + (comment['vader']*comment['upvotes'])
            total_count = total_count + 1
            upvote_sum = upvote_sum + comment['upvotes']
      sr_avg = 0
      try:
        sr_avg = weighted_sum_reddit_sent/total_count
      except:
        sr_avg = 0
      
      row = (subreddit,names[p],sr_avg,upvote_sum,total_count)
      rows.append(row)

      p+=1

  
  


  with open('subreddit_bias.csv', 'w') as f: 
    write = csv.writer(f) 
    write.writerow(headers) 
    write.writerows(rows) 
  

main()
