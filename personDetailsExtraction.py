import nltk
import genderRec
import dataReader
import dataOperations
import json


# nltk.download()
# sentence = "At eight o'clock on Thursday morning"
# tokens = nltk.word_tokenize(sentence)
# print(tokens)
# tagged = nltk.pos_tag(tokens)
# print(tagged)

clf = genderRec.clf
genderRec.train_name_classifier(clf)
# print(genderRec.test_classifier(clf))

translated_names = [genderRec.translators.translate_name_in_array(name.split(' ')[0]) for name in dataOperations.person_list]

translated_genders = [genderRec.translate_byte_to_name(byte_name) for byte_name in clf.predict(translated_names)]

person_list_with_names = zip(dataOperations.person_list, translated_genders)
