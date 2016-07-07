from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from speech import *
import dataOperations

sentiment_dictionary = {}

for line in open('AFINN-111.txt'):
    word, score = line.split('\t')
    sentiment_dictionary[word] = int(score)

def calculateSentiment(sentence):
    result = []
    pos = 0
    neg = 0
    for word in word_tokenize(sentence):
        score = sentiment_dictionary.get(word, 0)
        if score > 0:        
            pos += score
        if score < 0:
            neg += score
    result.append([pos, neg])
    return result

def characterOverallSentiment():
    characters_overall_sentiment = {}
    for x in dataOperations.person_list:
        if len(character_speech[x]) > 3: 
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
            characters_overall_sentiment[x] = result
    return characters_overall_sentiment

def characterToCharacterSentiment():
    sentiment_anal = {}
    for x in dataOperations.person_list:
        if len(character_speech[x]) > 3: 
            sentiment_anal[x] = {}
            for sentence in sent_tokenize(character_speech[x]):
                foundCharacter = ""
                for charName in dataOperations.person_list:
                    if sentence.find(charName) != -1:
                        foundCharacter = charName
                        cur_score = calculateSentiment(sentence)
                        if foundCharacter in sentiment_anal[x]:
                            # cur_score == [[pos, neg]]
                            sentiment_anal[x][foundCharacter][0][0] += cur_score[0][0]
                            sentiment_anal[x][foundCharacter][0][1] += cur_score[0][1]
                        else:
                            sentiment_anal[x][foundCharacter] = cur_score
    return sentiment_anal

print(characterToCharacterSentiment())
