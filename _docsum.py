from bs4 import BeautifulSoup
import lxml 
import math 
from nltk.corpus import stopwords
import string
from nltk.tokenize import sent_tokenize
import nltk

class Document:
    def __init__(self,PATH, FILE_NAME, PMCID, PMID):
        self.PATH = PATH 
        self.FILE_NAME = FILE_NAME
        self.PMCID = PMCID 
        self.PMID = PMID 
        self.FILE = PATH + FILE_NAME
        self.sentences = [] 
        self.tokenized_sentences= [] 
        
    def print_values(self): 
        print(self.FILE)
        print(self.PMCID)
        print(self.PMID) 
    
    def text_sentences(self):
	    path = "craft-1.0/genia-xml/pos/"+self.PMID+".txt.xml"
	    path = path.replace('\n','')
	    soup = BeautifulSoup(open(path), 'lxml') 
	    for sent in soup.find_all("sentence"):  
		    self.sentences.append(sent.text)
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

def corpus_tokenizer(list_of_docs):
    for doc in list_of_docs:
        doc.text_sentences() 
        doc.sentence_tokenizer() 



def corpus_occurence_dic(list_of_docs):
    dic = {} 
    count = 0 
    for doc in list_of_docs:
        tokens = doc.tokenized_sentences
        corpus_occurence_dic_helper(tokens,count,dic,len(list_of_docs)) 
        count = count + 1  
    return dic 


def corpus_occurence_dic_helper(tokenized_corp,index,dic,number_docs): 
    for sentence in tokenized_corp:
        for tok in sentence:
            if tok in dic:
                dic[tok][index] = dic[tok][index] + 1 
            else:
                dic[tok] = [0]*number_docs 
                dic[tok][index] = 1 

def corpus_idf(corpus_dic,number_docs): 
    dic = {} 
    for key in corpus_dic:
        doc_occurence = 0 
        for val in corpus_dic[key]:
            if val > 0:
                doc_occurence = doc_occurence + 1 
        divide =  float(number_docs) / float(doc_occurence) 
        dic[key] = math.log(divide) 
    return dic 













