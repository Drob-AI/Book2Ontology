from nltk.tokenize import sent_tokenize
import dataReader
import nltk
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


hary_potter_sent = dataReader.read_hary_potter()
hary_potter_words = [nltk.word_tokenize(row) for row in hary_potter_sent]
hary_potter_post_tagged = [nltk.pos_tag(tokens) for tokens in hary_potter_words]
sentts = [nltk.ne_chunk(pos_taged, binary = False) for pos_taged in hary_potter_post_tagged]
person_list = []
person = []
name = ""
for sentt in sentts:
    for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
        for leaf in subtree.leaves():
            person.append(leaf[0])
        if len(person) > 1: #avoid grabbing lone surnames
            for part in person:
                name += part + ' '
            if name[:-1] not in person_list:
                person_list.append(name[:-1].replace('Mr.', '').replace('Miss', '').strip())
            name = ''
        person = []

