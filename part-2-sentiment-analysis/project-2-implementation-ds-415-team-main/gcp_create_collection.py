import pymongo
import os
import time

def entity_checker(text_lower):
        entity_list = []
        if text_lower.find('trump') != -1:
            entity_list.append('trump')
        if text_lower.find('donald') != -1:
            entity_list.append('donald')
        if text_lower.find('biden') != -1:
            entity_list.append('biden')
        if text_lower.find('bezos') != -1:
            entity_list.append('bezos')
        if text_lower.find('musk') != -1:
            entity_list.append('musk')
        if text_lower.find('jeremy blackburn') != -1:
            entity_list.append('jeremy blackburn')
        if text_lower.find('elon') != -1:
            entity_list.append('elon')
        if text_lower.find('pence') != -1:
            entity_list.append('pence')
        if text_lower.find('fauci') != -1:
            entity_list.append('fauci')
        if text_lower.find('kamala') != -1:
            entity_list.append('kamala')
        if text_lower.find('harris') != -1:
            entity_list.append('harris')
        if text_lower.find('putin') != -1:
            entity_list.append('putin')
        if text_lower.find('menzel') != -1:
            entity_list.append('menzel')
        if text_lower.find('boris') != -1:
            entity_list.append('boris')
        if text_lower.find('boris johnson') != -1:
            entity_list.append('boris johnson')
        if text_lower.find('kanye') != -1:
            entity_list.append('kanye')
        if text_lower.find('adolf') != -1:
            entity_list.append('adolf')
        if text_lower.find('hitler') != -1:
            entity_list.append('hitler')
        if text_lower.find('mao')!= -1:
            entity_list.append('mao')
        if text_lower.find('zedong') != -1:
            entity_list.append('zedong')
        if text_lower.find('stalin') != -1:
            entity_list.append('stalin')
        if text_lower.find('jesus christ') != -1:
            entity_list.append('jesus christ')
        if text_lower.find('clinton') != -1:
            entity_list.append('clinton')
        if text_lower.find('epstein') != -1:
            entity_list.append('epstein')
        if text_lower.find('menzel') != -1:
            entity_list.append('menzel')
        if text_lower.find('hillary') != -1:
            entity_list.append('hillary')
        if text_lower.find('yang')!= -1:
            entity_list.append('yang')
        if text_lower.find('mitch') != -1:
            entity_list.append('mitch')
        if text_lower.find('mcconnell') != -1:
            entity_list.append('mcconnell')
        if text_lower.find('zuckerberg') != -1:
            entity_list.append('zuckerberg')
        if text_lower.find('tom cruise') != -1:
            entity_list.append('tom cruise')
        if text_lower.find('bernie') != -1:
            entity_list.append('bernie')
        if text_lower.find('sanders') != -1:
            entity_list.append('sanders')
        return entity_list

def main():
  myclient = pymongo.MongoClient("mongodb://localhost:27017/")
  mydb = myclient["cs415"]

  collection = mydb["compressed_tweets"]
  
  store_collection = mydb["tweets_gcp"]

  cur = collection.find({"data.created_at": {"$gte":"2020-11-06T06:59:59.999ZZ","$lt": "2020-11-07T23:59:59.999Z"}})

  i = 0
  for doc in cur:
    if i > 300000:
      print("exceeded max gcp")
      break

    hashtags = []
    try:
      eObj = doc['data']['entities'].get("hashtags",[])
      for h in eObj:
        hashtags.append(h['tag'])
    except:
      e = 0

    tagged = entity_checker(doc['data']['text'].lower())

    ob = {
      "_id": doc['data']['id'],
      "created_at": doc['data']['created_at'],
      "text": doc['data']['text'],
      "hashtags": hashtags,
      "gcp": None,
      "mag": 0,
      "tagged": tagged
    }
    print(i)
    #print(ob)
    store_collection.insert_one(ob)

    i = i + 1
    #time.sleep(.1)

main()