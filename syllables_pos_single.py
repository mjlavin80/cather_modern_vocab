import spacy
import pickle
from random import shuffle
import csv
import re
from collections import Counter
import pandas as pd
import string
import curses
import sqlite3
import numpy as np
import nltk

from nltk.corpus import cmudict
print("Loading libraries")
nlp = spacy.load('en')
d = cmudict.dict()
nlp = spacy.load('en')

def store_results(result_row):
    conn = sqlite3.connect('syllables_pos.db')
    c = conn.cursor()
    make_results = """CREATE TABLE IF NOT EXISTS results (id INTEGER PRIMARY KEY, \
    lavin_id TEXT, tt_ratio REAL, adj_ratio REAL, adv_ratio REAL, avg_syllables REAL)"""
    #id, tt_ratio, adj_ratio, adv_ratio, avg_syllables (per recognized)
    c.execute(make_results)

    insert_result = """INSERT INTO results (id, lavin_id, tt_ratio, adj_ratio, adv_ratio, avg_syllables) VALUES (null, ?, ?, ?, ?, ?)"""
    c.execute(insert_result, result_row)
    conn.commit()

def nsyl(word):
   return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]][0]

dict_of_10k = {}
with open ("lexicon/new10k.csv", "r") as myfile:
    for m_line in csv.reader(myfile):
        if m_line[0] != "word":
            dict_of_10k[m_line[0]] = m_line[1]

df_meta = pd.read_csv("meta/finalmeta.csv", encoding="latin-1")
docids = list(df_meta['gutenberg_id'])
sources = list(df_meta['source'])

#dict of dictionaries with the structure of {id:{position: (term, pos)}}
full_feature_dicts_pos = {}

full_feature_dicts_syllables = {}
#dict of dictionaries with the structure of {id: {term: [count, syllables]}}
print("Finished loading libraries")

_id = "1300"
print(_id)
full_pos_dict = {}
full_syllable_dict = {}

with open("txts/gutenberg_full_text/%s.txt" % str(_id)) as f:
    #lowercase
    s = f.read().lower().replace("\n", " ").replace("\r", " ").replace("\t", " ")


#model against spacy for pos
doc = nlp(s)

#tokenize for syllables, add results to dicts
tokens = s.split(" ")
tokens = [s.translate(str.maketrans('','',string.punctuation)) for s in tokens]
tokens = [s.translate(str.maketrans('','','1234567890')) for s in tokens]

cells = Counter(tokens)
print(cells)
try:
    del cells['']
except:
    pass

#convert back to a list of terms and counts
c = list(cells.items())

#loop through to minimize syllable detection lag
for y in c:
    #syllables
    try:
        #syllable
        sylls = nsyl(y[0])
    except:
        pass
for v,w in enumerate(doc):
    try:
        full_pos_dict[v] = (w.text, w.pos_)
    except:
        pass

#calculate ratios and add to pos_syllables_db

shuffle(tokens)
norm_tokens = tokens[:2800]
norm_token_count = len(norm_tokens)
norm_types = list(Counter(norm_tokens).keys())
norm_type_count = len(norm_types)
type_token_ratio = 1.0*norm_type_count/norm_token_count

#pos
adj_ratio = len([i[1] for i in list(full_pos_dict.values()) if i[1] == 'ADJ'])/len([j[1] for j in list(full_pos_dict.values())])
adv_ratio = len([i[1] for i in list(full_pos_dict.values()) if i[1] == 'ADV'])/len([j[1] for j in list(full_pos_dict.values())])

#syllables
syllables = sum(np.array([i[1]*i[0] for i in list(full_syllable_dict.values())]).astype(np.float))
words =sum(np.array([i[0] for i in list(full_syllable_dict.values())]).astype(np.float))
avg_syllables = syllables/words

result_row = [_id, type_token_ratio, adj_ratio, adv_ratio, avg_syllables]

print("ID %s worked" % str(_id))
