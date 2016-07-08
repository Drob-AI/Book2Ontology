import nltk
import string
import os
import dataReader
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer

#path = './tf-idf'
text = dataReader.read_hary_potter()
token_dict = {}


def tokenize(text):
    tokens = nltk.word_tokenize(text)
    stems = []
    for item in tokens:
        stems.append(PorterStemmer().stem(item))
    return stems

# for dirpath, dirs, files in os.walk(path):
#     for f in files:
#         fname = os.path.join(dirpath, f)
#         print "fname=", fname
#         with open(fname) as pearl:
#             text = pearl.read()
#             token_dict[f] = text.lower().translate(None, string.punctuation)
token_dict['book'] = "".join(text).lower().replace('\n',' ').translate(None, string.punctuation)

tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
tfs = tfidf.fit_transform(token_dict.values())

# str = 'Harry Potter enters the tournament for Hogwarts with Ron and magic'
# # response = tfidf.transform([str])
# feature_names = tfidf.get_feature_names()
# # print(response)
# # for col in response.nonzero()[1]:
# #     print(feature_names[col], response[0, col])
