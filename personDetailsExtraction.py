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

connected = {}
histogram = {}
for i,sentence in enumerate(dataOperations.hary_potter_post_tagged):
    first_nnp = []
    for word in sentence:

        for nnp in first_nnp:
            if histogram.get(nnp) == None:
                histogram[nnp] = {}

            if histogram[nnp].get(word[0]) == None:
                histogram[nnp][word[0]] = 1
            else:
                histogram[nnp][word[0]] += 1

        if word[1] == 'NNP':
            for con_key in first_nnp:
                if(connected.get(con_key) == None):
                    connected[con_key] = []

                connected[con_key].append(word[0])


            first_nnp.append(word[0])



names = [single_name for n in dataOperations.person_list for single_name in n.split(' ')]
for key in connected.keys():
    if key not in names:
        del connected[key]
    else:
        connected[key] = list(set(connected[key]))

# print(histogram["Snape"])
# histogram and top not stop words used as connected words
