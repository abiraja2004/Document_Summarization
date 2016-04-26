from bs4 import BeautifulSoup
import lxml 

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
        #print path
        soup = BeautifulSoup(open(path), 'lxml')
        count = 0 
	xml_sentences = [] #list of xml sentences 
	for sent in soup.find_all("sentence"):
		if count < 5:
			#print "sent ", sent
			count = count + 1
			xml_sentences.append(sent) 
		else:
			break
	
	#print(xml_sentences) 
        #print(sentences)
	
	sentences = [] 
	for sent in xml_sentences:
		tok_list = [] 
		sent = str(sent)
		print(sent) 
		soup = BeautifulSoup(sent,'lxml') 
		token = soup.find_all("tok") 
		for i in token:
			#print i 
			#print(i['cat'],i.string)
			pos = (i['cat'],i.string)
			#print(pos) 
			tok_list.append(pos) 
		sentences.append(tok_list)
	print sentences
		#for i in BeautifulSoup(sent
	"""
	for sent in xml_sentences:	
		print(sent) 
		token = soup.final_all("tok")
		for i in token:
			print i"""
		#soupify = BeautifulSoup(sent.string,"xml") 
	       	#print(soup)
		#token = soup.find_all("tok")  
	       	#print(token) 
        print("done")
        
        
    def abstract(self):
        soup = BeautifulSoup(open(self.FILE), 'xml')
        abstract = soup.abstract 
        abst = abstract.get_text() 
        print(abst) 
        return abst
        
    def text(self): 
        soup = BeautifulSoup(open(self.FILE), 'xml') 
        body = soup.body
        txt = body.get_text() 
        return txt

    

        
        
#Create a class for each file 
list_of_docs = [] 
file = "craft-1.0/articles/ids/craft-idmappings-release"
with open(file,'r') as f: 
    count = 0 
    for line in f:
        if count>0: 
            line_list = line.split('\t') 
            list_of_docs.append(Document("craft-1.0/articles/nxml/" , line_list[0],line_list[1],line_list[2])) 
        count = count + 1 

        
for doc in list_of_docs:
    doc.print_values()
print("\n\n") 
list_of_docs[0].print_values() 
print("\n\n") 
#list_of_docs[0].abstract() 
print("\n\n") 
#list_of_docs[0].text() 
list_of_docs[0].text_sentences() 

        
    
    
    
    
