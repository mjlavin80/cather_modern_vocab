import curses
import nltk
from nltk.corpus import cmudict
import spacy

d = cmudict.dict()

nlp = spacy.load('en')

def nsyl(word):
   return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]][0]

try:
    a = nsyl('struggle')
except:
    a = False
print(a)

doc = nlp(u'The tall man told us to duck quickly.')
for word in doc:
    print(word.text, word.lemma, word.lemma_, word.tag, word.tag_, word.pos, word.pos_)
