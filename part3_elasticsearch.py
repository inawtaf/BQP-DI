import time
import os
from elasticsearch import Elasticsearch
import datetime

Index_List = []
dictionary = {}

def query_to_elasticsearch():
	#Read the query file
	query_file = open('/Users/Kartikeya/Documents/IR/Assignment/query.txt','r')
	for query in query_file:
		#Read a query and remove leading spaces
		query = query.strip()
		#Distribute current query into words
		words = query.split(" ")
		#We get our query number
		query_number = words[0]
		#Generating query to feed into elasticsearch
		if len(words) > 2:
			query = words[1]
			#Resetting words
			words = words[2:]
			for word in words:
				query = query+" "+word
		elif len(words) == 2:
			query = words[1]
		else:
			query = ""
		#Here we have query for elasticsearch, feeding the query
		current_query = es_connection.search(index='alldocs', doc_type='text', body={"from":0,"size":300,"query":{"match":{"content":query}}})
		#Query made
		print("processed query number: "+query_number)
		#Saving query number in Index_List
		Index_List.append(query_number)
		#Creating a list of result
		result=[]
		#Iterating over the documents in result
		for document in current_query['hits']['hits']:
			#Checking if we have already taken this document, otherwise appending
			if (document['_source']['name']) not in result:
				result.append(doc['_source']['name'])
			#Maximum result limit is 75
			if len(result) > 75:
				break
		#Adding the result set obtained to the dictionary
		dictionary[query_number] = result
		#Current query processed
	#All queries processed
	#Closing query file
	query_file.close()

#Connect to elasticasearch
es_connection = Elasticsearch('http://localhost:9200/', timeout = 30, max_retries = 10, retry_on_timeout = True)
#Setup a request to create a new index in elastic search
es_request = {
	"setting":{
	"number_of_shards":"1",
	"number_of_replicas":"0"
	}
}
#Create an index
index = es_connection.create(index = 'alldocs', doc_type = 'text', body = es_request)
#Creating a list of all our data files
files_directory = []
for root, dirs, files in os.walk('/Users/Kartikeya/Documents/IR/Assignment/alldocs'):
	for file in files:
		#Setting path from os
		path = os.path.join(root,file)
		#Appending to files directory
		files_directory.append(path)
#Now iterating over the list of the files and indexing that data
count = 0
for file in files_directory:
	#Open the current file
	current_data_file = open(file, 'rb')
	#Red content as string
	data = str(current_data_file.read())
	#Removing leading spaces
	data = data.strip()
	#Creating a document
	document = {'count': count, 'file': file, 'data': data}
	#Indexing document to our alldocs index
	add = es_connection.create(index = 'alldocs', doc_type = 'text', body = document)
	count = count+1
#Indexing complete
#Now we will start making queries at t = start
start = time.time()
#Making queries
query_to_elasticsearch()
#End of searching at t = end
end = time.time()
#Evaluating time taken
time_taken = end - start
#Creating new response file
response_file = open('response_from_es.txt','w')
#Writing final result to the response file
response_file.write('Time_taken for making queries with elastic search = '+str(time_taken)+' milli seconds\n')
#Closing file
response_file.close()