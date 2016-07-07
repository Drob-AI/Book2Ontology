from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from speech import *
import dataOperations

sentiment_dictionary = {}

for line in open('AFINN-111.txt'):
    word, score = line.split('\t')
    sentiment_dictionary[word] = int(score)

for x in dataOperations.person_list:
    if len(character_speech[x]) > 3: 
        print x
        result = []
        pos = 0
        neg = 0
        for sentence in sent_tokenize(character_speech[x]):
            
            for word in word_tokenize(sentence):
                score = sentiment_dictionary.get(word, 0)
                if score > 0:
                    pos += score
                if score < 0:
                    neg += score
        result.append([pos, neg])
        for s in result: print(s)