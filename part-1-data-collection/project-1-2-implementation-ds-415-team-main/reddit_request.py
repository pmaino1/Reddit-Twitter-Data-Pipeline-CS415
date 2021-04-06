import requests
import sys
import json
from datetime import datetime
import time
import pymongo

outputdict = {}
outputnum = 0
post_dict = {}

subreddits = ["politics", "news", "worldnews", "pics", "videos", "science", "technology",
            "sports", "upliftingnews", "philosophy", "twoxchromosomes", "democrats", "conservative", "libertarian", "republican",
            "liberal", "progun", "futurology", "economics", "socialism", "whitepeopletwitter", "blackpeopletwitter",
            "sandersforpresident", "atheism", "christianity", "politicalhumor", "selfawarewolves", "joebiden", "nottheonion",
            "teenagers", "latestagecapitalism", "lgbt", "unpopularopinion", "leopardsatemyface"]

keywords = ["donald", "trump", "joe", "biden", "elon", "musk", "jeremy blackburn",
            "anthony", "fauci", "mike", "pence", "kamala", "harris", "kanye", "west",
            "adolf", "hitler", "mao", "zedong", "joseph", "stalin", "jesus christ",
            "bill", "clinton", "jefferey", "epstein", "hillary", "clinton", "andrew",
            "yang", "mitch", "mcconnel", "mark", "zuckerberg", "tom", "cruise",
            "bernie", "sanders"]

myclient = pymongo.MongoClient("---")
mydb = myclient["cs415"]
mycol_comp = mydb["compressed_comments"]
mycol_comp_posts = mydb["compressed_posts"]

def checkKeywords(checkstring, post_json):
    global outputdict
    global outputnum
    global post_dict
    for keyword in keywords:
        if(checkstring.lower().find(keyword) != -1):
            #print("~~~match on: ", checkstring)
            #checks name to see if type comment or post
            if post_json['name'][:2] == 't1':
                outputdict[outputnum] = post_json
                outputnum += 1

                obj = {
					"_id": post_json['name'],
                    "comment": post_json
				}
                store = mycol_comp.insert_one(obj)
            #post json
            else :
                #print("Post with a keyword")
                post_dict[post_json['name']] = post_json
                obj = {
					"_id": post_json['name'],
                    "post": post_json
				}
                post_store = mycol_comp_posts.insert_one(post_json)
            return


def searchSubComments(comment):
    #print("------", type(comment['data']['replies']['data']['children']))

    replies = comment['data']['replies']['data']['children']

    for reply in replies:
        if(reply['kind'] != 't1'): #only get actual comments
            continue
        checkKeywords(reply['data']['body'], reply['data']) #check the text
        if(reply['data']['replies'] != ""):
            searchSubComments(reply)


def scanSubreddit(subreddit_name):

    r = requests.get(r'https://www.reddit.com/r/' + subreddit_name + '/top/.json?t=day', headers = {'User-agent': 'cs415_crawler'})

    subreddit_json = r.json()

    for postnum in range(len(subreddit_json['data']['children'])):
        
        post_url = subreddit_json['data']['children'][postnum]['data']['permalink']
        #print(post_url)
        # gets the postnum-th post on the front page of this subreddit
        c = requests.get(r'https://www.reddit.com'+post_url+'.json', headers = {'User-agent': 'cs415_crawler'})
        #print('https://www.reddit.com'+post_url+'.json')

        post_json = c.json()
        # comments json will become a list of dictionaries, one dictionary for the actual post and
        # one for the comments.

        #if post has any of our peeps in text, add it to the dictionary
        #to get post data, like title text : (post_json[0]['data']['children'][0]['data']['title'])
        checkKeywords(post_json[0]['data']['children'][0]['data']['title'], post_json[0]['data']['children'][0]['data'])

        base_comments = post_json[1]['data']['children']
        #num_comments = len(base_comments)
        #print("Number of base comments in this post: ", num_comments)
        # gets the number of base level comments in this post.

        if(len == 0):
            return #TODO placeholder exit condition

        #iterate through ALL base level comments in this post
        for basecomment in base_comments:
            if(basecomment['kind'] != 't1'): #only get actual comments
                continue
            try:
                checkKeywords(basecomment['data']['body'], basecomment['data']) #check the text
                if(basecomment['data']['replies'] != ""):
                    #print("---Subcomments found.")
                    searchSubComments(basecomment)
            except:
                print("Unexpected error:", sys.exc_info()[0])
                print("---comment: ", basecomment['data']['body'])

def main():
    day = 24 * 60 * 60
    while(True):
        now = datetime.now()
        for subreddit in subreddits:
            scanSubreddit(subreddit)
            break
        global outputdict
        global outputnum
        global post_dict
        #TODO change file path
        # with open('sample2.json', "w") as outfile:
        #     json.dump(outputdict, outfile, indent = 4)
        #print(len(post_dict))
        end = datetime.now()
        #calculate to sleep so we begin crawl at same time tomorrow
        sleep_time = day - (end-now).total_seconds()
        #print("A little sleepy")
        time.sleep(sleep_time) 
main()