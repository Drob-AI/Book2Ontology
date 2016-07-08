from dataOperations import person_list, hary_potter_ne_and_pos_tagged, hary_potter_post_tagged
import string
#import Levenshtein as lev
import nltk
from nltk.tree import Tree
from itertools import chain
from nltk.stem import WordNetLemmatizer
from nltk.corpus.reader import wordnet
from nltk.corpus import wordnet as wn
lemmatizer = WordNetLemmatizer()


def findFullName(name, person_list):
    name = "".join(ch for ch in name if ch not in set(string.punctuation)).lower()
    names = name.split()
    #print(name, names)
    closest = None
    closest_score = 0
    for person in person_list:
        person_default = person
        person = "".join(ch for ch in person if ch not in set(string.punctuation)).lower()
        person_names = person.split()
        #print(person, person_names)
        inters = set(names).intersection(set(person_names))
        if(set(names) <= set(person_names) or set(names) >= set(person_names)):
            #print(person_names, len(inters))
            if closest_score < len(inters):
                closest = person_default
                closest_score = len(inters)
    return closest


def extractNamedEntities(ne_type, ne_and_pos_tagged_words):
    named_entities = []
    for s in ne_and_pos_tagged_words:
        for c in s.subtrees():
            if isinstance(c, Tree) and c.label() == ne_type:
                named_entities.append(c.leaves())
    named_entities_strings = map(lambda ne: " ".join(map(lambda t: t[0], ne)),  named_entities)
    return named_entities_strings

def extractPersons(ne_and_pos_tagged_words):
    return extractNamedEntities('PERSON', ne_and_pos_tagged_words)

def extractUniquePersons(ne_and_pos_tagged_words):
    persons = extractPersons(ne_and_pos_tagged_words)
    # now try to merge "Harry" with "Harry Potter" and such...
    persons_merged = list()
    for p in persons:
        full_name = findFullName(p, persons_merged)
        full_name = " ".join(full_name.split()[-2:]) if full_name else None # looks better because many names are prepended by another word
        p = " ".join(p.split()[-2:])
        if not full_name:
            persons_merged.append(p)
            #print("append " + p)
        elif len(full_name) < len(p):
            persons_merged.remove(full_name)
            persons_merged.append(p)
            #print("update " + full_name + " -> " + p)
        ##else full_name == p or full_name >= p: do nothing
        #else:
        #    print(p + " is " + full_name)
    return persons_merged

def extractLocations(ne_and_pos_tagged_words):
    return extractNamedEntities('LOCATION', ne_and_pos_tagged_words)


def countCharacterImportance(ne_and_pos_tagged_words):
    named_entities_strings = extractPersons(ne_and_pos_tagged_words)
    unique_named_entities_strings = extractUniquePersons(ne_and_pos_tagged_words)
    person_histogram = {p: 0 for p in unique_named_entities_strings}
    for p in named_entities_strings:
        p = findFullName(p, unique_named_entities_strings)
        person_histogram[p] = (person_histogram[p] + 1) if p in person_histogram else 1
    return person_histogram

#h = countCharacterImportance(hary_potter_ne_and_pos_tagged)
#h_sorted = sorted(h.items(), key=lambda i: i[1], reverse=True)
#print(h_sorted)


def getMainCharacters(threshold_ratio):
    char_histogram = countCharacterImportance(hary_potter_ne_and_pos_tagged)
    char_histogram = sorted(char_histogram.items(), key=lambda i: i[1], reverse=True)
    sum_occurrences = sum(map(lambda i: i[1], char_histogram))
    return filter(lambda i: i[1] >= threshold_ratio * sum_occurrences, char_histogram)

#print(getMainCharacters(0.01))


def countLocationImportance(ne_and_pos_tagged_words):
    named_entities_strings = extractLocations(ne_and_pos_tagged_words)
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
