import gensim.models.keyedvectors as word2vec
from pycorenlp import StanfordCoreNLP

class FindSimilarOpinions:
    extracted_opinions = {}
    word2VecObject = []
    cosine_sim = 0

    def __init__(self, input_cosine_sim, input_extracted_ops):
        self.cosine_sim = input_cosine_sim
        self.extracted_opinions = input_extracted_ops
        word2vec_add = "data//assign4_word2vec_for_python.bin"
        self.word2VecObject = word2vec.KeyedVectors.load_word2vec_format(word2vec_add, binary=True)
        self.sentiment = self.sentimentList()
        self.negative, self.positive, self.neutral = self.sentiment
        return

    def get_word_sim(self, word_1, word_2):
        return self.word2VecObject.similarity(word_1, word_2)


    def findSimilarOpinions(self, query_opinion):
        similar_opinions = {}
        # example data, which you will need to remove in your real code. Only for demo.
        self.cosine_sim = 0.33
        query = query_opinion.split(", ")
        q_atr = query[0]
        q_qlty = query[1]
        
        for opinion in self.extracted_opinions:
            op = opinion.split(", ")
            op_atr = op[0]
            op_qlty = op[1]
            #Checking whether opinion exist in our word embedding or not
            if op_atr in self.word2VecObject and op_qlty in self.word2VecObject:
                #checking sentiments of query and opinion to retrieve opinions of same sentiment
                same_sentiment = 1
                if q_qlty in self.positive and op_qlty in self.negative:
                        same_sentiment = 0
                if q_qlty in self.negative and op_qlty in self.positive:
                        same_sentiment = 0
                if same_sentiment == 1:
                    qlty_similarity = self.get_word_sim(q_qlty, op_qlty)
                    atr_similarity = self.get_word_sim(q_atr, op_atr)
                    #retrieving attributes with similarity score > 0.5 and quality of attributes with similar sentiments
                    
                    if atr_similarity >= self.cosine_sim and qlty_similarity >0.2  :
                        print("["+ q_qlty + ', ' + op_qlty  + ": " + str(qlty_similarity))
                        similar_opinions[opinion] = self.extracted_opinions[opinion]
        return similar_opinions
    
    #function to create segregate sentiments into 3 category : positive, negative and neutral
    def sentimentList(self):  
        nlp = StanfordCoreNLP('http://localhost:9000')
        with open ('data//assign4_reviews.txt','r') as file:
            text = file.read().split("\n")
        positive = []
        negative = []
        neutral = []
        for i in range(len(text)-1):
            output = nlp.annotate(text[i],properties={
                    'annotators': ' tokenize, ssplit, lemma, depparse, sentiment, ner, pos',
                    'outputFormat': 'json',
                    'openie.triple.strict':'true',
                    'timeout': 50000,
                    })

            for s in output["sentences"]:

                if s["sentiment"] == "Negative":
                    for t in s["tokens"]:
                        if t["pos"] == "JJ":
                            if t["word"] not in negative:
                                negative.append(t["word"].lower())
                elif s["sentiment"] == "Positive":
                    for t in s["tokens"]:
                        if t["pos"] == "JJ":
                            if (t["word"] not in negative) and (t["word"] not in positive):
                                positive.append(t["word"].lower())
                else:
                    for t in s["tokens"]:
                        if t["pos"] == "JJ":
                            if (t["word"] not in negative) and (t["word"] not in positive) and (t["word"] not in neutral):
                                neutral.append(t["word"].lower())
        return negative, positive, neutral