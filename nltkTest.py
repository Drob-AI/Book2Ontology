import nltk
import genderRec
# nltk.download()
sentence = "At eight o'clock on Thursday morning"
tokens = nltk.word_tokenize(sentence)
print(tokens)
tagged = nltk.pos_tag(tokens)
print(tagged)

clf = genderRec.clf
genderRec.train_name_classifier(clf)
print(genderRec.test_classifier(clf))