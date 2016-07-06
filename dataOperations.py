from nltk.tokenize import sent_tokenize
import dataReader
import nltk
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


hary_potter_sent = dataReader.read_hary_potter()
hary_potter_words = [nltk.word_tokenize(row) for row in hary_potter_sent]
hary_potter_post_tagged = [nltk.pos_tag(tokens) for tokens in hary_potter_words]