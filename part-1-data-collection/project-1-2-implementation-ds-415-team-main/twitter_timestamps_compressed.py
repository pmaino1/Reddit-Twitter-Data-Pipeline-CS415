import requests
import json
import sys
import pymongo


def create_headers(bearer_token):
	headers = {"Authorization": "Bearer {}".format(bearer_token)}
	return headers
def create_params():
	params = {"tweet.fields" : "created_at,public_metrics,lang,entities,referenced_tweets", "expansions" : "geo.place_id"}
	return params

#Can only set rules for the search stream
'''
def set_rules(headers, bearer_token):
	rules_people = [
		{"value" : "donald trump has:mentions", "tag" : "trump tweets"},
		{"value" : "joe biden has:mentions" , "tag" : "biden tweets"},
		{"value" : "-is:retweet", "tag" : "not a retweet"},
	]
	load = {"add" : rules_people}
	response = requests.post("https://api.twitter.com/2/tweets/search/stream/rules",
        headers=headers, json=load,)
	if response.status_code == 201:
		print(json.dumps(response.json()))
'''

def main():
	myclient = pymongo.MongoClient("mongodb://localhost:27017/")

	mydb = myclient["cs415"]
	mycol_comp = mydb["compressed_timestamps"]

	bearer_token = "AAAAAAAAAAAAAAAAAAAAAKfnIQEAAAAAeiu1HESI8e%2F6tglAmWHhVX4QamI%3Dk8Dz71iPtonmfCCxs2nVbOGbhgHmyKrVMdHoR0W4ZmDvXTrZok"
	#create header
	headers = create_headers(bearer_token)
	#create stream params
	parameters = create_params()
	print("Getting the response")
	response = requests.get("https://api.twitter.com/2/tweets/sample/stream", params = parameters,  headers = headers, stream=True,)
	#print(response.status_code)

	#check if response worked
	if(response.status_code == 200):
		#read through json data of response
		for response_line in response.iter_lines():
			if response_line:
				json_response = json.loads(response_line)
				j_dump = json.dumps(json_response, indent=4,sort_keys=True)
				ts = {
					"created_at": json_response['data']['created_at']
				}
				y = mycol_comp.insert_one(ts)
	else:
		print("Error with request, error code =", response.status_code)
	#'''
main()