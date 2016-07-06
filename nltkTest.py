import nltk
# nltk.download()
sentence = "At eight o'clock on Thursday morning"
tokens = nltk.word_tokenize(sentence)
print(tokens)
tagged = nltk.pos_tag(tokens)
print(tagged)