# import StringDouble
# import ExtractGraph
from pycorenlp import StanfordCoreNLP

class ExtractOpinions:
    # Extracted opinions and corresponding review id is saved in extracted_pairs, where KEY is the opinion and VALUE
    # is the set of review_ids where the opinion is extracted from.
    # Opinion should in form of "attribute, assessment", such as "service, good".
    extracted_opinions = {}
    
    def __init__(self):
        return

    def extract_pairs(self, review_id, review_content):
        nlp = StanfordCoreNLP('http://localhost:9000')
        pos_dict = {}
        # example data, which you will need to remove in your real code. Only for demo.
        output = nlp.annotate(review_content,properties={
        'annotators': ' tokenize, sentiment, ner, pos',
        'outputFormat': 'json',
        'openie.triple.strict':'true',
        'timeout': 50000,
        })
        
        for sentence in output['sentences']:

            #Creating dictionary of words to store their pos type: {word:pos}
            for term in sentence["tokens"]:
                pos_dict[term["word"] ]= term["pos"]

            #Extracting enhancedDependencies
            result = [sentence["enhancedDependencies"] for item in output]
            for i in result:
                opinion = ""
                for rel in i:
                    #extracting 'amod' type dependencies and storing as (governor, dependent)
                    if rel['dep'] == 'amod':
                        opinion = rel['governorGloss'].lower() + ", " + rel['dependentGloss'].lower()  
                    #extracting 'nsubj' type dependencies and storing as (dependent, governor)
                    #Useful opinion of dep type 'nsubj' have governor = JJ and dependent = NN
                    if rel['dep'] == 'nsubj' and pos_dict[rel['governorGloss']] == 'JJ' and pos_dict[rel['dependentGloss']] == 'NN':
                        opinion = rel['dependentGloss'].lower() + ", " + rel['governorGloss'].lower()
                    #extracting 'discourse' type dependencies and storing as (dependent, governor)
                    #Useful opinion of dep type 'nsubj' have governor = NN and dependent = UH    
                    if rel['dep'] == 'discourse' and pos_dict[rel['governorGloss']] == 'NN' and pos_dict[rel['dependentGloss']] == 'UH':
                        opinion = rel['dependentGloss'].lower() + ", " + rel['governorGloss'].lower()
                    if opinion != "":
                        if opinion not in self.extracted_opinions.keys():
                            self.extracted_opinions[opinion] = [review_id]
                        else:
                            id_list = self.extracted_opinions[opinion]
                            if review_id not in id_list:
                                id_list.append(review_id)
                                self.extracted_opinions[opinion] = id_list
                
        return(self.extracted_opinions)
    
    
        
#         self.extracted_opinions = {'service, good': [1, 2, 5], 'service, excellent': [4, 6]}
