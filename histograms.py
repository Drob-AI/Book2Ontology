from dataOperations import person_list, hary_potter_ne_and_pos_tagged, hary_potter_post_tagged
import nltk
from nltk.tree import Tree
from itertools import chain
from nltk.stem import WordNetLemmatizer
from nltk.corpus.reader import wordnet
lemmatizer = WordNetLemmatizer()


def countCharacterImportance(person_list, ne_and_pos_tagged_words):
    named_entities = []
    for s in ne_and_pos_tagged_words:
        for c in s.subtrees():
            if isinstance(c, Tree) and c.label() == 'PERSON':
                named_entities.append(c.leaves())
    named_entities_strings = map(lambda ne: " ".join(map(lambda t: t[0], ne)),  named_entities)

    person_histogram = {p: 0 for p in named_entities_strings}#person_list}
    for p in named_entities_strings:
        person_histogram[p] = (person_histogram[p] + 1) if p in person_histogram else 1
    return person_histogram


#h = countCharacterImportance(person_list, hary_potter_ne_and_pos_tagged)
#h_sorted = sorted(h.items(), key=lambda i: i[1], reverse=True)
#print(h_sorted)


def countWordsInBook(pos_tagged):
    pos_tagged_flattened = chain.from_iterable(pos_tagged)
    words = filter(
        lambda t: any(t[1].startswith(tag) for tag in ['NN','VB','JJ','RB']), 
        pos_tagged_flattened)

    words_histogram = dict()
    pos_lemma_dict = {'NN':wordnet.NOUN,'VB':wordnet.VERB,'JJ':wordnet.ADJ,'RB':wordnet.ADV}
    for w in words:
        lem_pos = pos_lemma_dict[w[1][:2]]
        lem = lemmatizer.lemmatize(w[0], pos=lem_pos)
        #print(w, lem, pos_lemma_dict[w[1][:2]])
        words_histogram[lem] = (words_histogram[lem] + 1) if lem in words_histogram else 1
    return words_histogram

hw = countWordsInBook(hary_potter_post_tagged)
hw_sorted = sorted(hw.items(), key=lambda i: i[1], reverse=True)
print(hw_sorted)
