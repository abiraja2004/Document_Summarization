import _docsum as ds 
import nltk
import string 
import math 
import io
from nltk.corpus import stopwords

class test_docs:
	def __init__(self,file_name,doc_PMID,doc_index):
		self.file_name = file_name 
		self.PMID = doc_PMID 
		self.doc_index = doc_index 
		self.sentences = []
		self.length_sentences = 0 
		self.tokenized_sentences = [] 
		self.tf = {}
		self.tf_idf = [] 
		self.scores = [] 
		self.top_n = [] 
		self.sum_file = ""


	def print_values(self):
		print(self.file_name)
		print(self.PMID)
		print(self.doc_index) 


	def test_sentence_tokens(self):
		with io.open(self.file_name, "r") as f:
			text = f.read() 
			sents = nltk.sent_tokenize(text)
			self.sentences = sents 

	def sentence_tokenizer(self):
		for sent in self.sentences:
			s = sent.lower()
			stopset = [word for word in stopwords.words('english')]
			stop_punc = list(string.punctuation)
			stops = stopset+stop_punc

			tokens = nltk.wordpunct_tokenize(s) 

			tokens = [w for w in tokens if w.lower() not in stops ] 

			filtered_tokens = [x for x in tokens if not (x.isdigit() or x[0] == '-' and x[1:].isdigit())]

			self.tokenized_sentences.append(filtered_tokens) 

	def sentence_length(self):
		self.length_sentences = len(self.sentences)

	def term_freq(self):
		for s in self.tokenized_sentences:
			for tok in s:
				if tok in self.tf:
					self.tf[tok] = self.tf[tok] + 1 
				else:
					self.tf[tok] = 1 


	def calc_tf_idf(self,idf):
		for sent in self.tokenized_sentences:
			sentence = [] 
			for tok in sent:
			    tok_tf = 0 
			    try:
			        tok_tf = self.tf[tok]    
			    except:
			        tok_tf = 0          
			    tok_idf = 0 
			    try:
			        tok_idf = idf[tok]
			    except:
			        tok_idf = 0         
			    token_tf_idf = float(tok_tf * tok_idf) 
			    sentence.append(token_tf_idf)
	  		self.tf_idf.append(sentence)
	def sentence_scores(self):
		count = 0 
		for sentence in self.tf_idf:
			length = len(sentence)
			sentence_score = 0 
			for tok in sentence:
				sentence_score = sentence_score + tok 
			#acount for size of sentence 
			sentence_score = float(sentence_score / length)
			tup = (count,sentence_score)
			self.scores.append(tup) 
			count = count + 1 

		self.scores = sorted(self.scores, key=lambda x: x[1], reverse=True)
	
	def top_n_sentences(self,cutoff): 
		count = 0 
		for score in self.scores:
			if count < cutoff :
				sent_num = score[0]
				self.top_n.append(self.sentences[sent_num]) 
				count = count + 1 
			else:
				break 

	def to_file(self,path,cutoff):
		self.sum_file = path + self.PMID + "_summary" + "_" + str(cutoff) + ".txt"
		f = open(self.sum_file, "w")
		for sentence in self.top_n:
			f.write(sentence.encode("utf-8"))
		f.close() 








def text_docs(list_of_docs,files_list):
	test_doc_files = [] 
	for f in files_list:
		doc = list_of_docs[f] 
		doc_PMID = doc.PMID.strip()
		file_name = "craft-1.0/articles/txt/"+doc_PMID+".txt"
		doc = test_docs(file_name,doc_PMID,f)
		test_doc_files.append(doc)
	return test_doc_files 


def main():
	print "Generating Documents ... "

	list_of_docs = ds.document_objects( "craft-1.0/articles/ids/craft-idmappings-release" )

	

	###################### CORPUS SECTION ###############################



	print "Generating Corpus Dictionary ... "

	ds.corpus_tokenizer(list_of_docs)  

	corpus_dic = ds.corpus_occurence_dic(list_of_docs)

	corpus_idf = ds.corpus_idf(corpus_dic,len(list_of_docs))



	###################### TEST DOCUMENT SECTION ###########################

	#list of docs to test/ numbers chosen at random 
	count = 0 
	"""for doc in list_of_docs:
		if "16110338" in doc.PMID :
			print count 
		count = count + 1 """

	doc_indexes_to_test = [5,27,35,36,16,24,60]

	print("Test values : ")
	for index in doc_indexes_to_test:
		list_of_docs[index].print_values() 
		print("\n ")


	print "Loading Test Document Files ... "
	test_docs = text_docs(list_of_docs,doc_indexes_to_test)

	print "Tokenizing and computing term frequencies ... "
	for test in test_docs:
		test.test_sentence_tokens() 
		test.sentence_tokenizer() 
		test.sentence_length()
		test.term_freq() 
		test.calc_tf_idf(corpus_idf)
		test.sentence_scores()


	################### This Section is for the Evaluation Part ################ 
	#In this python script we will only generate the summary files 
	#uses pyrouge to compute scores 
	#precision 
	#value 
	#f measure 

	print("Generating Summaries ... ")

	#cutoff = 10 #does changing the cutoff provide me with any difference in rouge score? 

	path = "pythonROUGE/Summaries/"
	
	#cutoffs will be used to compare best percentage of sentences to extract and
	#run rouge on 

	cut_off = 10 
	for test in test_docs:
		test.top_n_sentences(cut_off)
		test.to_file(path,cut_off)

	cutoff_list = [.05,.10,.15,.20]
	
	for cut in cutoff_list:
		for test in test_docs:
			new_cut = int(test.length_sentences * cut) 
			print(new_cut)
			test.top_n_sentences(new_cut)
			test.to_file(path,cut)



	print "Done ..."


main() 




