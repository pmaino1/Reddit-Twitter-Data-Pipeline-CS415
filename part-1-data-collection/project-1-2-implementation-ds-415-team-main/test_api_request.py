import requests
import json
import sys
import pymongo
import timeit


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
	myclient = pymongo.MongoClient("---")

	mydb = myclient["cs415"]
	mycol_comp = mydb["compressed_tweets"]

	bearer_token = "AAAAAAAAAAAAAAAAAAAAAMOgJQEAAAAAJjuSJAiCn0qYsWO5pXCJMDQRjRw%3DXohxNgIbLuEorM61rOuQC6WKgUqSSulOU7y3QbQhkONXrpSzV4"
	#create header
	headers = create_headers(bearer_token)
	#create stream params
	parameters = create_params()
	print("Getting the response")
	response = requests.get("https://api.twitter.com/2/tweets/sample/stream", params = parameters,  headers = headers, stream=True,)
	#print(response.status_code)
	start_time = timeit.default_timer()
	end_time = 0
	#check if response worked
	if(response.status_code == 200):
		#read through json data of response
		for response_line in response.iter_lines():

			if response_line:
				json_response = json.loads(response_line)
				# j_dump = json.dumps(json_response, indent=4,sort_keys=True)
				# ts = {
				# 	"created_at": json_response['data']['created_at']
				# }
				search_string = json_response['data']['text'].lower()
				flagged = False
				if search_string.find('trump') != -1:
					flagged = True
				elif search_string.find('donald') != -1:
					flagged = True
				elif search_string.find('biden') != -1:
					flagged = True
				elif search_string.find('bezos') != -1:
					flagged = True
				elif search_string.find('musk') != -1:
					flagged = True
				elif search_string.find('jeremy blackburn') != -1:
					flagged = True
				elif search_string.find('elon') != -1:
					flagged = True
				elif search_string.find('pence') != -1:
					flagged = True
				elif search_string.find('fauci') != -1:
					flagged = True
				elif search_string.find('kamala') != -1:
					flagged = True
				elif search_string.find('harris') != -1:
					flagged = True
				elif search_string.find('putin') != -1:
					flagged = True
				elif search_string.find('menzel') != -1:
					flagged = True
				elif search_string.find('boris') != -1:
					flagged = True
				elif search_string.find('boris johnson') != -1:
					flagged = True
				elif search_string.find('kanye') != -1:
					flagged = True
				elif search_string.find('adolf') != -1:
					flagged = True
				elif search_string.find('hitler') != -1:
					flagged = True
				elif search_string.find('mao')!= -1:
					flagged = True
				elif search_string.find('zedong') != -1:
					flagged = True
				elif search_string.find('stalin') != -1:
					flagged = True
				elif search_string.find('jesus christ') != -1:
					flagged = True
				elif search_string.find('clinton') != -1:
					flagged = True
				elif search_string.find('epstein') != -1:
					flagged = True
				elif search_string.find('menzel') != -1:
					flagged = True
				elif search_string.find('hillary') != -1:
					flagged = True
				elif search_string.find('yang')!= -1:
					flagged = True
				elif search_string.find('mitch') != -1:
					flagged = True
				elif search_string.find('mcconnell') != -1:
					flagged = True
				elif search_string.find('zuckerberg') != -1:
					flagged = True
				elif search_string.find('tom cruise') != -1:
					flagged = True
				elif search_string.find('bernie') != -1:
					flagged = True
				elif search_string.find('sanders') != -1:
					flagged = True

				if json_response['data']['lang'] != "en":
					flagged = False

				if flagged :
					y = mycol_comp.insert_one(json_response)
					#print(json_response)
	else:
		print("Error with request, error code =", response.status_code)
	#'''
main()