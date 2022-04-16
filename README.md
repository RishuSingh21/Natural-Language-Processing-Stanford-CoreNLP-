# Natural-Language-Processing-Stanford-CoreNLP-
Programming Language: Python (Version: 3.8.8)
Libraries Used: Stanford CoreNLP, genism.models.keyedvectors

Brief about this project:
This project focuses on natural language processing by designing a reviewer opinion extraction and querying system.
Features of the underlying system:
(1) Automatically extracts opinions from all the reviews 
(2) The user inputs an opinion as a query, and it compares the input opinion with the extracted opinions and returns  similar opinions 
(3) A set of reviews are returned as supporting evidence for this opinion

Steps to Install standfordCoreNLP:
1. Download Stanford CoreNLP (link)
2. Install Java 8 (for mac): Open terminal and use below commands:
    a. brew update
    b. brew install jenv
    c. brew cask install java
3. (if brew is not installed then first intsall brew on mac)
4. Running Stanford CoreNLP Server:
    a. java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -annotators     "tokenize,ssplit,pos,lemma,parse,sentiment" -port 9000 -timeout 30000
5. Accessing Stanford CoreNLP Server using Python
    a. Download pycorenlp: pip install pycorenlp
    
Designing of Opinion Extraction Module with CoreNLP
First we need to install standfordCoreNLP (instructions given above)
Annotator used: tokenize, sentiment, ner, pos
Reason why I chose above annotators for designing my opinion extraction module:
tokenize: To detect words in a sentence
pos: To get the tagging of a word which I have further utilized to extract only relevant
‘enhanced dependencies’.
Sentiment: To identify the sentiment of a query and retrieve only matching sentiment
query.

Objective: To create a dictionary ‘extracted_opinions’ of format {opinion: [list_of_docs]}
where opinion = ‘attribute’, ‘quality’

Process:
1. First a dictionary mapping all the words in a review with its corresponding ‘pos’ is
created.
2. for each sentence in a review, extract ‘enhanced dependencies’ of following types:
   (a)‘amod’: Retrived all amod type dependencies without any conditions. In this case
    opinion is stored as ‘governorGloss’, ‘dependentGloss’
   (b) ‘nsubj’: Retrived only ‘governorGloss’ = ‘JJ’ (‘adjective’) and ‘dependentGloss’
    = ‘NN’ (‘noun’). In this case opinion is stored as ‘dependentGloss’,‘governorGloss’
   (c)‘discourse’: Retrived only ‘governorGloss’ = ‘NN’ (‘noun’) and
    ‘dependentGloss’ = ‘UH’ (‘interjection’). In this case opinion is stored as
    ‘dependentGloss’, ‘governorGloss’
To extract above dependencies, I have referred research paper on ‘Aspect-Based Opinion Mining Using Dependency Relations” by Amani K Samha.( ‘Amani K Samha, “Aspect- Based Opinion Mining Using Dependency Relations”, International Journal of Computer Science Trends and Technology (IJCST) – Volume 4 Issue 1, Jan - Feb 2016’)
3. After extracting relevant opinions from a review, I stored it in the extracted_opinions along with the review_id. So, for each review we have multiple dictionary entry.
Opinion Similarity Score Calculation:
1. Split query_opinion to get ‘attribute’ and ‘quality’ of the query_opinion
2. Split each opinion in extracted_opinion into 2 parts – ‘attribute’ and ‘quality’
3. Check if the ‘attribute’ and ‘quality’ of an opinion exist in our word embedding –
‘assign4_word2vec1.bin’
4. Now check the sentiment of the query quality and opinion quality.
5. If opinion’s ‘attribute’ and ‘quality’ exist in our word embedding and sentiments of the
query and the opinion is same, then calculate similarity between query and opinion. To calculate similarity between a query and an opinion calculate:
  a. Attribute similarity between the query and the opinion
  b. Quality similarity between the query and the opinion
6. Decide a threshold of similarity to retrieve only relevant opinions.
7. Tuning cosine similarity threshold:
  a. cosine similarity threshold for attribute is kept at 0.33 to retrieve opinion
  attributes like ‘salad’, ‘fries’, ‘taco’ for query attribute ‘food’
  b. cosine similarity threshold for attribute is kept at 0.2 to retrieve opinion
  attributes like ‘tender ’, ‘excellent’, ‘good’ for query attribute ‘delicious’




