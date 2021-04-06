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

  headers = ['name','created_at','gcp']
  print(headers)
  rows = []

  # people = [['biden','kamala','harris','bernie','sanders','clinton','hillary','yang'],['trump','donald','mitch','mcconell','pence'],['putin','boris','boris johnson'],['fauci','elon','musk','bezos','kanye','zuckerberg','epstein']]

  people = [['fauci'],['elon'],['musk'],['bezos'],['kanye'],['zuckerberg'],['epstein']]
  # people = [['trump','donald'],['biden'],['bezos'],['elon','musk'],['jeremy blackburn'],['pence'],['fauci'],['kamala','harris'],['putin'],['boris','boris johnson'],['kanye'],['adolf','hitler'],['mao','zedong'],['stalin'],['jesus christ'],['clinton','hillary'],['epstein'],['yang'],['mitch','mcconnell'],['zuckerberg'],['tom cruise'],['bernie','sanders']]

  names = ['Anthony Fauci','Elon Musk','Elon Musk','Jeff Bezos','Kanye West','Mark Zuckerberg','Jeffrey Epstein']


  # names = ['Donald Trump','Joe Biden','Jeff Bezos','Elon Musk','Jeremy Blackburn','Mike Pence','Anthony Fauci','Kamala Harris','Vladimir Putin','Boris Johnson','Kanye West','Adolf Hitler','Mao Zedong','Joseph Stalin','Jesus Christ','Hillary Clinton','Jeffrey Epstein','Andrew Yang','Mitch Mcconell','Mark Zuckerberg','Tom Cruise','Bernie Sanders']
  #groups = ['Democrats','Republicans','World Figures','Unaffiliated Individuals']

  p = 0
  for person in people:
    print("STARTING WITH: "+names[p])

    tweet_collection = mydb["tweets_gcp"]
    tweet_cur = tweet_collection.find()

    for tweet in tweet_cur:
      inter = intersection(person,tweet['tagged'])
      if len(inter) > 0:
        if tweet['mag'] > .25:
          row = [names[p],tweet['created_at'],tweet['gcp']]
          rows.append(row)
    print("DONE WITH TWITTER")
    p+=1

  


  with open('twitter_grouped_gcp_tweets_unaff.csv', 'w') as f: 
    write = csv.writer(f) 
    write.writerow(headers) 
    write.writerows(rows) 
  

main()
