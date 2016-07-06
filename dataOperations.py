from nltk.tokenize import sent_tokenize
import dataReader
import nltk
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import json

person_list = []
with open('person_list.json') as data_file:
    person_list = json.load(data_file)

organizations = []
with open('organizations.json') as data_file:
    organizations = json.load(data_file)

hary_potter_sent = dataReader.read_hary_potter()
hary_potter_words = [nltk.word_tokenize(row) for row in hary_potter_sent]
hary_potter_post_tagged = [nltk.pos_tag(tokens) for tokens in hary_potter_words]
# sentts = [nltk.ne_chunk(pos_taged, binary = False) for pos_taged in hary_potter_post_tagged]
# person_list = []
# person = []
# org = []
# organizations = []
# name = ""
# for sentt in sentts:
#     for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
#         for leaf in subtree.leaves():
#             person.append(leaf[0])
#         if len(person) > 1: #avoid grabbing lone surnames
#             for part in person:
#                 name += part + ' '
#             if name[:-1] not in person_list:
#                 person_list.append(name[:-1])
#             name = ''
#         person = []

#     for subtree in sentt.subtrees(filter=lambda t: t.label() == 'ORGANIZATION'):
#         for leaf in subtree.leaves():
#             org.append(leaf[0])
#         if len(org) > 1: #avoid grabbing lone surnames
#             for part in org:
#                 name += part + ' '
#             if name[:-1] not in organizations:
#                 organizations.append(name[:-1])
#             name = ''
#         org = []

# print(person_list, organizations)
# with open('person_list.json', 'w') as outfile:
#     json.dump(person_list, outfile)

# with open('organizations.json', 'w') as outfile:
#     json.dump(organizations, outfile)