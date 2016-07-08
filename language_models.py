from nltk.collocations import BigramAssocMeasures
from nltk.collocations import BigramCollocationFinder
from speech import character_speech
from speech import all_speech
from nltk import word_tokenize
import nltk
from nltk.util import ngrams

bigram_measures = BigramAssocMeasures()

baseFreq = {}
def person_language_model(person_speech, speechy):
    token=nltk.word_tokenize(person_speech)
    bigrams=ngrams(token,2)
    finder = BigramCollocationFinder.from_words(bigrams)
    bgcnt = len(token) - 1
    print bgcnt
    if bgcnt == 0:
        return None
    baseFreq[speechy] = 1.0 / bgcnt
    finder.apply_freq_filter(3)
    finder.apply_ngram_filter(lambda w1, w2: w1 == '\n')
    return finder

person_models = {}

def person_language_models():
    for speechy in character_speech:
        char_text = character_speech[speechy]
        person_models[speechy] = person_language_model(char_text, speechy)

def bg_score(bg, model, a):
    score = model.score_ngram(bigram_measures.raw_freq, bg[0], bg[1])

    if score == None:
        return baseFreq[a]
    else:
        return score

def tag_all_speech():
    person_language_models()
    for a in all_speech:
        if a['speeker']:
            continue
        maxq = 0
        char = None
        for b in character_speech:
            model = person_models[b]
            if not model:
                continue
            spokes = [x["txt"] for x in a['speech_tokens'] if x["isChar"]]
            spokes = reduce(lambda a,b: a + ' ' + b, spokes)
            token = nltk.word_tokenize(spokes)
            bigrams = ngrams(token,2)
            m = map(lambda bg: bg_score(bg, model, b), bigrams)
            q = reduce(lambda a,b: a * b, m);
            if q > maxq:
                maxq = q
                char = b
        a['speeker'] = char

tag_all_speech()

for a in all_speech:
    print a