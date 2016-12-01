import time
import os
import nltk
from nltk.corpus import state_union
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize

#Creating abasic filter
def filter(query):
	query = query.replace("\\r",' ')
	query = query.replace("\\n",' ')
	query = query.replace("\\",'')
	query = query.replace('=',' ')
	query = query.replace("'",' ')
	query = query.replace(',',' ')
	query = query.replace(':',' ')
	query = query.replace('|','')
	return query
#Defining wordnet
def wordnet(query):
		if query.startswith('J'):
			return nltk.corpus.wordnet.ADJ
		if query.startswith('V'):
			return nltk.corpus.wordnet.VERB
		if query.startswith('N'):
			return nltk.corpus.wordnet.NOUN
		if query.startswith('R'):
			return nltk.corpus.wordnet.ADV
		else:
			return nltk.corpus.wordnet.NOUN
#Defining my index
class my_index:
	#Blocking some words
	blocks = {'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', ',','.',';',':','-','"', 'him', 'each', 'the', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', "'",'?','/', "\\",'=','!','$','#','*','(',')','{','}','[',']', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those'}
	#Setting lemmatizer for removing plurals
	word_lemmatizer = nltk.WordNetLemmatizer()
	#Creating dictionary
	dictionary = {}
	def intialize():
		#Creating a list of all our data files
		files_directory = []
		for root, dirs, files in os.walk('/Users/Kartikeya/Documents/IR/Assignment/alldocs'):
			for file in files:
				#Setting path from os
				path = os.path.join(root,file)
				#Appending to files directory
				files_directory.append(path)
		
		count = 1
		for file in files_directory:
			current_data_file = open(file, 'rb')
			data = str(current_data_file.read()).lower()
			data = filter(data)
			for block in blocks:
				data = data.replace(block, '')
			Token = nltk.sent_tokenize(data)
			for flag in token:
				prs = nltk.word_tokenize(flag)
				lists = nltk.pos_tag(prs)
				for word, value in lists:
					if word not in self.blocks:
						value = wordnet(value)
						lemma = self.word_lemmatizer.lemmatize(word, value)
						if lemma not in self.dictionary:
							self.dictionary[lemma] = []
							self.dictionary[lemma].append(count)
						if count not in self.dictionary[lemma]:
							self.dictionary[lemma].append(count)
			count = count+1

	def merge(self,x,y):
		final = []
		if(len(x)<len(y)):
			for item in x:
				if any(item in s for s in y):
					final.append(i)
		else:
			for item in y:
				if any(item in s for s in x):
					final.append(i)
		return final

	def process(self,query):
		lists = []
		query = query.lower()
		query = filter(query)
		results = []
		prs = nltk.word_tokenize(query)
		words = nltk.pos_tag(prs)
		for word, value in words:
			if word not in self.blocks:
				value = wordnet(value)
				lemma = self.word_lemmatizer.lemmatize(word,value)
				lists.append(lemma)
		try:
			results = self.dictionary[lists[0]]
		except:
			pass
		for i in range(len(lists)-1):
			try:
				results = self.merge(results, self.dictionary[lists[i+1]])
			except:
				pass
		return results

	def generate(self,query):
		result_list = self.process(query)
		out = []
		for item in result_list:
			out.append(self.files_directory[item])
		return out


#Opening queries & response file
query_file = open('/Users/Kartikeya/Documents/IR/Assignment/query.txt','r')
response_file = open('response_from_my_index.txt','w')
#Creating new index
myindex = my_index()
#Initializing the index
myindex.intialize
#Initialize total time, will add time of every process to it
total_time = 0.0
for query in query_file:
	#Remove leading spaces from the query
	query = query.strip()
	for i in range(len(query)):
		if query[i] == ' ':
			break
	#Set serial number
	serial = query[0:i]
	query = query[i+1:]
	start = time.time()
	results = myindex.generate(query)
	end = time.time()
	total_time = total_time + (end-start)
	response_file.write('----------\n'+'Query: '+str(serial)+'\n')
	for req in results:
		response_file.write(str(req)+'\n')

#Writing final result to the response file
response_file.write('Time_taken for making queries with my_customised_index = '+str(total_time)+' milli seconds\n')
#Closing both the files
query_file.close()
response_file.close()
#End of code