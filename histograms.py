from dataOperations import person_list, hary_potter_ne_and_pos_tagged, hary_potter_post_tagged
import nltk
from nltk.tree import Tree
from itertools import chain
from nltk.stem import WordNetLemmatizer
from nltk.corpus.reader import wordnet
from nltk.corpus import wordnet as wn
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


def getMainCharacters(threshold_ratio):
    char_histogram = countCharacterImportance(person_list, hary_potter_ne_and_pos_tagged)
    char_histogram = sorted(char_histogram.items(), key=lambda i: i[1], reverse=True)
    sum_occurrences = sum(map(lambda i: i[1], char_histogram))
    return filter(lambda i: i[1] >= threshold_ratio * sum_occurrences, char_histogram)

print(getMainCharacters(0.01))


def countLocationImportance(ne_and_pos_tagged_words):
    named_entities = []
    for s in ne_and_pos_tagged_words:
        for loc in s.subtrees():
            if isinstance(loc, Tree) and loc.label() == 'LOCATION':
                named_entities.append(loc.leaves())
    named_entities_strings = map(lambda ne: " ".join(map(lambda t: t[0], ne)),  named_entities)

    loc_histogram = {loc: 0 for loc in named_entities_strings}
    for loc in named_entities_strings:
        loc_histogram[loc] = (loc_histogram[loc] + 1) if loc in loc_histogram else 1
    return loc_histogram

#hloc = countLocationImportance(hary_potter_ne_and_pos_tagged)
#hloc_sorted = sorted(hloc.items(), key=lambda i: i[1], reverse=True)
#print(hloc_sorted)


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

#hw = countWordsInBook(hary_potter_post_tagged)
#hw_sorted = sorted(hw.items(), key=lambda i: i[1], reverse=True)
#print(hw_sorted)


def countEventsInBook(pos_tagged, threshold):
    pos_tagged_flattened = chain.from_iterable(pos_tagged)
    nouns = filter(lambda t: t[1].startswith('NN'), pos_tagged_flattened)

    event_sim = dict()
    event_synset = wn.synsets('event', pos=wordnet.NOUN)[0]
    for n in nouns:
        lem = lemmatizer.lemmatize(n[0], pos=wordnet.NOUN)
        if lem not in event_sim:
            lem_synsets = wn.synsets(lem, pos=wordnet.NOUN)
            if len(lem_synsets) > 0:
                lem_synset = lem_synsets[0]
                event_sim[lem] = wn.path_similarity(lem_synset, event_synset)
    return filter(lambda i: i[1] >= threshold, event_sim)

#he = countEventsInBook(hary_potter_post_tagged, 0.2)
#he_sorted = sorted(he.items(), key=lambda i: i[1], reverse=True)
#print(he_sorted)
