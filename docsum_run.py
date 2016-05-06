import docsum as ds 
import nltk
import string 
import math 
#from sklearn.feature_extraction.text import TfidfVectorizer

#from nltk.book import * 
def main():
	#array of Document objects 
	print "Generating Documents .... " + "\n"  
	list_of_docs = ds.document_objects( "craft-1.0/articles/ids/craft-idmappings-release" )
	#print(list_of_docs)
	#array of corpus sentences part of speech tagged 
	print "Generating Corpus ... " + "\n" 
	corpus = ds.corpus_sentences(list_of_docs) 
	#print(corpus[0]), '\n'
	#print(corpus[1]) 
	

	list_of_abstracts = ds.list_abstracts(list_of_docs)
	#print(list_of_abstracts[0])

	list_of_texts = ds.list_texts(list_of_docs)
	#print(list_of_texts[0]) 
	
	number_docs = len(list_of_docs) 
	print("number of docs in corpus: " , number_docs) 
	
	#word_count_dic = ds.word_count_dic(list_of_docs) 

	print("\n\n\n\n\n") 
	test_doc = list_of_texts[0] 
	
	#print(test_doc) 
	#print(type(test_doc)) 
	
	print("\n\n\n\n\n\n\n\n\n\n") 
	#split texts into sentences 
	sentences = ds.text_sentences(test_doc) 
	number_of_sentences = len(sentences) 
	#print(sentences) 
	print("number of sentences = " , number_of_sentences) 

	#tokenize each word in each sentence  
	
	tokenized_sentences = [] 
	for sentence in sentences:
		sentence = sentence.encode('utf8')
		#print(type(sentence))
		tokenized_sentences.append(ds.sentence_tokens(sentence)) 
	print("\n\n\n\n\n\nTokenized Sentences: \n\n\n\n") 
	#print(tokenized_sentences) 

	print("Displaying dictionary of tokenized sentences with occurences .....") 
	tokenized_sentences_dic = ds.word_dic(tokenized_sentences) 
	#print(tokenized_sentences_dic) 

	tokenized_sentences_dic_tf = ds.tf_word_dic(tokenized_sentences_dic) 
	#print(tokenized_sentences_dic_tf) 
	print(tokenized_sentences_dic_tf.keys()) 	
	
	print("Displaying corpus dics.................") 
	#create a list of dictionaries

	#print(corpus[0])
	#print("chicken") 	
	
	
	dictionary = ds.corpus_occurence_dic(corpus)
#	print(dictionary.keys())
	#print '\n\n\n'
	corpus_idf = ds.corpus_idf(dictionary,number_docs) 
	#print(corpus_idf.keys()) 
	#print("corpus_idf....") 
	#print(corpus_idf) 



	



	"""print("..........................Test IDF Section.....................") 

	#docs where corpus appears

	print(dictionary['lean']) 
	count = 0 
	for i in dictionary['lean']:
		#count = 0
		if i > 0:
			count+=1

	print(count) 
	
	divide = float(number_docs) / float(count) 
	print(divide) 
	idf = math.log(divide) 
	print(idf) 
	""" 
#	print(dictionary) 	

	#ds.corpus_sentences_file(corpus) 
	
	#print "Corpus File DONE \nOpen File: full_tagged_corpus.txt \n"

	print("#############################TF-IDF Weighting of test document #############################") 
	

	print(tokenized_sentences) 















"""
	#transformer = TfidfTransformer()
	
	#list of document texts, without POS_tagging 

	#idef tokenize_and_stem(text):
	
	tf = TfidfVectorizer(analyzer='word', ngram_range=(1,3), min_df = 0, stop_words = 'english')
	tfidf_matrix =  tf.fit_transform(list_of_texts)
	feature_names = tf.get_feature_names() 
	print(len(feature_names))
	print(tfidf_matrix)
	print(feature_names)
	#vectorizer = TfidfVectorizer(min_df=1)
	#vectorizer.fit_transform(list_of_texts) 

	#print(vectorizer) 
	#test
	#get abstracts for all documents 
	#list_of_abstracts = ds.list_abstracts(list_of_docs)  	
	#print(list_of_abstracts[0]) 
	#ds.abstract_tag(list_of_docs[0].abstract,sentences[0])   
	print("done") 
	""" 
	#TODO: TFIDF 


main() 
