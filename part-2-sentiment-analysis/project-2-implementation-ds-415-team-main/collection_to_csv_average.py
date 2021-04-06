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

  headers = ['name','average_twitter','average_reddit','twitter','posts','comments','total']
  print(headers)
  rows = []
  people = [['trump','donald'],['biden'],['bezos'],['elon','musk'],['jeremy blackburn'],['pence'],['fauci'],['kamala','harris'],['putin'],['boris','boris johnson'],['kanye'],['adolf','hitler'],['mao','zedong'],['stalin'],['jesus christ'],['clinton','hillary'],['epstein'],['yang'],['mitch','mcconell'],['zuckerberg'],['tom cruise'],['bernie','sanders']]
  names = ['Donald Trump','Joe Biden','Jeff Bezos','Elon Musk','Jeremy Blackburn','Mike Pence','Anthony Fauci','Kamala Harris','Vladimir Putin','Boris Johnson','Kanye West','Adolf Hitler','Mao Zedong','Joseph Stalin','Jesus Christ','Hillary Clinton','Jeffrey Epstein','Andrew Yang','Mitch Mcconell','Mark Zuckerberg','Tom Cruise','Bernie Sanders']

  tweet_collection = mydb["tweets_vader"]
  tweet_cur = tweet_collection.find()

  post_collection = mydb["posts_vader"]
  post_cur = post_collection.find()

  comment_collection = mydb["posts_vader"]
  comment_cur = comment_collection.find()

  p = 0
  for person in people:
    print("STARTING WITH: "+names[p])
    sum_twitter_sent = 0
    twitter_count = 0

    sum_reddit_sent = 0
    reddit_posts_count = 0
    reddit_comments_count = 0


    tweet_collection = mydb["tweets_vader"]
    tweet_cur = tweet_collection.find()

    post_collection = mydb["posts_vader"]
    post_cur = post_collection.find()

    comment_collection = mydb["comments_vader"]
    comment_cur = comment_collection.find()

    for tweet in tweet_cur:
      inter = intersection(person,tweet['tagged'])
      if len(inter) > 0:
        sum_twitter_sent = sum_twitter_sent + tweet['vader']
        twitter_count = twitter_count + 1
    print("DONE WITH TWITTER")
    for post in post_cur:
      inter = intersection(person,post['tagged'])
      if len(inter) > 0:
        sum_reddit_sent = sum_reddit_sent + post['vader']
        reddit_posts_count = reddit_posts_count + 1

    print("DONE WITH POSTS")
    for comment in comment_cur:
      inter = intersection(person,comment['tagged'])
      if len(inter) > 0:
        sum_reddit_sent = sum_reddit_sent + comment['vader']
        reddit_comments_count = reddit_comments_count + 1
    print("DONE WITH COMMENTS")
    
    reddit_avg = 0
    try:
      reddit_avg = sum_reddit_sent/(reddit_comments_count+reddit_posts_count)
    except:
      reddit_avg = 0
    twitter_avg = 0
    try:
      twitter_avg = sum_twitter_sent/twitter_count
    except:
      twitter_avg = 0
    total_count = twitter_count+reddit_comments_count+reddit_posts_count

    print("DONE WITH CALCULATIONS")
    row = [names[p],twitter_avg,reddit_avg,twitter_count,reddit_posts_count,reddit_comments_count,total_count]
    rows.append(row)
    p+=1

  


  with open('average_scores.csv', 'w') as f: 
    write = csv.writer(f) 
    write.writerow(headers) 
    write.writerows(rows) 
  

main()
