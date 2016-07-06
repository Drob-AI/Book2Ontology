from nltk.tokenize import sent_tokenize, word_tokenize
import dataReader

hary_potter_text = str(dataReader.read_hary_potter())
hary_potter_sent = sent_tokenize(hary_potter_text)
hary_potter_words = [word_tokenize(row) for row in hary_potter_sent]