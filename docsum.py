from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import string
import lxml 
from nltk.tokenize import sent_tokenize
import nltk
#from math import exp, expm1
import math 
#from nltk.book import * 

#class has abstract and main body 
#get POS tags from file
#create a part of speech tagger so that you can use this on other files 
#add pos:word pair 
#use viterbi algorithms from hw4 when dealing with an outside sentence 

#tf_idf 
#identify term frequencies inverse document frequencies use scikit learn to test first 
#Sentences list = 

class Document:
    def __init__(self,PATH, FILE_NAME, PMCID, PMID):
        self.PATH = PATH 
        self.FILE_NAME = FILE_NAME
        self.PMCID = PMCID 
        self.PMID = PMID 
        self.FILE = PATH + FILE_NAME
        
    def print_values(self): 
        print(self.FILE)
        print(self.PMCID)
        print(self.PMID) 
    def text_sentences(self):
	    path = "craft-1.0/genia-xml/pos/"+self.PMID+".txt.xml"
	    path = path.replace('\n','')
	    soup = BeautifulSoup(open(path), 'lxml') 
	    xml_sentences = []
	    for sent in soup.find_all("sentence"):
		    #print sent 
		   # encode = sent.text
		  
		    xml_sentences.append(sent.text)
	    	
	    return xml_sentences
    
    def text_sentences_tag(self):
        path = "craft-1.0/genia-xml/pos/"+self.PMID+".txt.xml" 
        path = path.replace('\n','')
        #print path
        soup = BeautifulSoup(open(path), 'lxml')
        count = 0 
	xml_sentences = [] #list of xml sentences 
	for sent in soup.find_all("sentence"):
		#print "sent ", sent
		count = count + 1
		xml_sentences.append(sent.encode('utf8'))#edit made here 3:07AM  
		
	sentences = [] 
	for sent in xml_sentences:
		tok_list = [] 
		sent = str(sent)
		#print(sent) 
		soup = BeautifulSoup(sent,'lxml') 
		token = soup.find_all("tok") 
		for i in token:
			pos = (i['cat'],i.string)
			tok_list.append(pos) 
		sentences.append(tok_list)
	#print sentences
	#print("done")

	return sentences 
        
    def abstract(self):
        soup = BeautifulSoup(open(self.FILE), 'lxml')
	abstract = soup.find("abstract") 
	"""
	print "The result is" 
	print abstract 

	print "contents" 
	print abstract.contents 

	print "the text"
	print abstract.get_text() 

	for a in abstract: 
		if a.string is None :
			a.string = ' ' 
	
	print abstract.get_text 
	"""
	"""abstract = soup.abstract
	#for a in abstract:
	#	if (a.string is None):
	#		a.string = " " 	

	abst = abstract.get_text()
	print(abst)
	print(self.FILE) 
	"""
	
	return abstract.get_text() 
        
    def text(self):
        soup = BeautifulSoup(open(self.FILE), 'lxml') 
        body = soup.find("body") 
        #txt = body.get_text()
        return body.get_text()


	    
def document_objects(file_path):
	#Create a class for each file 
	list_of_docs = [] 
	#file = "craft-1.0/articles/ids/craft-idmappings-release"
	with open(file_path,'r') as f: 
    		count = 0 
    		for line in f:
			if count>0: 
				line_list = line.split('\t') 
        			list_of_docs.append(Document("craft-1.0/articles/nxml/" , line_list[0],line_list[1],line_list[2])) 
        		count = count + 1 

	return list_of_docs 

def list_abstracts(documents):
	list_of_abstracts = [] 
	for doc in documents:
		list_of_abstracts.append(doc.abstract()) 
	return list_of_abstracts 

def list_texts(documents):
	list_of_texts = [] 
	for doc in documents:
		list_of_texts.append(doc.text())
	return list_of_texts 
def corpus_sentences(list_of_docs):
	corpus = [] 
	for doc in list_of_docs:
		corpus.append(doc.text_sentences()) 
	return corpus 
def corpus_sentences_file(corpus):
	write = open("full_tagged_corpus.txt","w") 
	for files in corpus:
		for sentences in files:
			for words in sentences:
				#print(words) 
				#print(type(words[0])) 
				#print(type(words[1]))
				#print(words[0],words[1]) 
				
				line = words[0].encode('utf-8')  + "\t" + words[1].encode('utf-8') + "\n" 
				#print(line) 
				write.write(line) 
				#write.write(str(words)+"\n")
				#write.write(line) 
			write.write("\n")
	write.close() 

def text_sentences(text):
	#nltk sentence tokenizer 
	sent_tokenize_list = sent_tokenize(text) 
	#print(len(sent_tokenize_list))
	return sent_tokenize_list 

def sentence_tokens_driver(sentences): 
	tokenized_sentences = [] 
	for sentence in sentences: 
		#sentence = sentence.encode('utf8')
		tokenized_sentences.append(sentence_tokens(sentence))
	return tokenized_sentences 

#tokenize word excluding stopwords 
def sentence_tokens(sentence):
	#sentence.encode('utf8')
	stopset = set(stopwords.words('english'))
	#if(val = 0):
	#	sentence = sentence.encode('utf8') 
	tokens = nltk.wordpunct_tokenize(sentence) 
	tokens = [w for w in tokens if not w in stopset]
	#type(tokens) 
	#ext = nltk.Text(tokens) 

	#punctuation + stopwords are not important 
	#stop = stopwords.words('english') + set(string.punctuation)
	#tokens = [i for i in word_tokenize(sent.lower()) if i not in stop]

	#print(len(tokens)) 
	"""sentence = "".join(l for l in sentence if l not in string.punctuation)
	stopset = set(stopwords.words('english'))
	tokens = nltk.word_tokenize(sentence)
	"""
	#cleanup = " ".join(filter(lambda word: word not in stopset, sentence.split()))
	#tokens = nltk.word_tokenize(cleanup) 
	#print("\n\n\n\n\n\n KESBFKDBGKFDBGKFDBGKFDBBGDF ........ \n\n\n\n\n")
	#return cleanup
	return tokens 

###########################FUNCTIONS FOR TF-IDF##############################

#counts occurence of tokens in file 
def word_dic(tokened_sentence_list):
	dic = {} 
	for sentence in tokened_sentence_list:
		for token in sentence:
			tok  = token.lower() 
			if tok in dic:
				dic[tok] = dic[tok] + 1 
			else:
				dic[tok] = 1 
	return dic 

#TO:DO 
#counts occurence and appearence in sentence 

def tf_word_dic(dic):
	number_of_words = len(dic)
	tf_dic = {} 
	for key in dic:
		tf = float(dic[key])/ float(number_of_words) 
		tf_dic[key] = tf 
	return tf_dic 

def corpus_occurence_dic_helper(tokenized_corp,index,dic,number_docs): 
	#empty list of size number_docs
	l = [0]*number_docs 
	for sentence in tokenized_corp:
		for token in sentence:
			tok = token.lower()
			tok = tok.encode('utf-8') 
			if tok in dic:
				dic[tok][index] = dic[tok][index] + 1 
			else:
				dic[tok] = l 
				dic[tok][index] = 1 

def corpus_occurence_dic(corpus):
	dic = {} 
	count = 0 
	number_docs = len(corpus) 
	for corp in corpus:
		tokenized_corp = sentence_tokens_driver(corp) 
		#print(tokenized_corp) 
		corpus_occurence_dic_helper(tokenized_corp,count,dic,number_docs) 
		count = count + 1  
	return dic 



def corpus_idf(corpus_dic,number_docs): 
	dic = {} 
	for key in corpus_dic:
		#number of docs where word appears 
		doc_occurence = 0 
		for val in corpus_dic[key]:
			if val!= 0:
				doc_occurence = doc_occurence + 1 
		
		
	#	print("key \t", key )
		divide =  float(number_docs) / float(doc_occurence) 
		dic[key] = math.log(divide) 
		#dic[key] = math.log(float(number_docs / doc_occurence)) 
	#	print(dic[key]) 

	return dic 


	

#structure: 
#		word : [ doc_1_appearence , doc_2_appearence, ..... , doc_n_appearence] 
#def corpus_word_dic

#takes in document in string format and tokenizes it and outputs 
#def input_tokenize(text):

"""def abstract_tag(abstract,corpus_sentence): 
	print("abstract\n\n") 
	print(abstract) 
	print("tags\n\n") 
	print(corpus_sentence) 

"""


#def text_tag(text):

#find sentences that pertain only to the text 

