from subprocess import PIPE, Popen
import time
import os

Index_List = []
dictionary = {}

def make_queries():
	#Open query file
	query_file = open('/Users/Kartikeya/Documents/IR/Assignment/query.txt','r')
	#Open search response file
	response_file = open ('response_from_grep.txt', 'w')
	#Read queries from query file as a sentence
	for sentence in query_file:
		#Remove unneccesary spaces from every sentence
		sentence = sentence.strip()
		words = sentence.split(" ")
		#Save query_number in the index list
		query_number = words[0]
		Index_List.append(query_number)
		#Update words by removing query_number
		words = words[1:len(words)]
		#Defining a result set for saving the result of current query
		result_set = []
		for word in words:
			#Calling grep on the current query, word by word
			query_process = Popen(["grep", '-lr', word, '/Users/Kartikeya/Documents/IR/Assignment/alldocs/'], stdout = PIPE)
			#Read the result from stdout
			results = str(query_process.stdout.read())
			#Filter and save the result obtained from the current query in the result_set
			result = results.split("\\n")
			result_set.append(sorted(set(result)))
		#Now we will write the result obtained by this query to our response file
		try:
			#Give the heading for current query
			response_file.write('--------------'+'\n'+'Query in process: '+query_number+words+'\n'+'--------------')
			#Adding result to the main dictionary
			dictionary[query_number] = set.intersection(*result_set)
			#Writing the result from this query
			for line in dictionary[query_number]:
				try:
					print("processed query number = "+query_number)
					response_file.write(line+'\n')
				except:
					pass
		except:
			pass
	#Closing both the files
	query_file.close()
	response_file.close()

#Start processing these queries at time = start
start = time.time()
make_queries()
end = time.time()
#Evaluating time of the query processing
time_taken = end - start
#Writing the result in response file
response_file = open('response_from_grep.txt','w')
response_file.write('Time_taken for making queries with grep = '+str(time_taken)+' milli seconds\n')
response_file.close()