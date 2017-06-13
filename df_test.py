import pandas as pd
from collections import Counter
import string
import csv

dict_of_10k = {}
with open ("lexicon/new10k.csv", "r") as myfile:
    for m_line in csv.reader(myfile):
        if m_line[0] != "word":
            dict_of_10k[m_line[0]] = m_line[1]

df_meta = pd.read_csv("meta/finalmeta.csv", encoding="latin-1")
docids = list(df_meta['gutenberg_id'])

full_feature_dicts = []
feature_dicts = []
excluded_ids = []

found = False
for _id in docids:
    print(_id)
    if "processed" in _id:
        full_fdict = {}
        fdict = {}

        with open("txts/other_full_text/%s.txt" % str(_id)) as f:
            #lowercase
            s = f.read().lower().replace("\n", " ").replace("\r", " ").replace("\t", " ")

        #tokenize and convert to term frequency table, cells = list of term, count tuples
        tokens = s.split(" ")

        tokens = [s.translate(str.maketrans('','',string.punctuation)) for s in tokens]

        cells = Counter(tokens)
        del cells['']

        c = list(cells.items())


        #write tsv to folder
        df_cells = pd.DataFrame.from_records(c)

        df_cells.to_csv("txts/other_tsv/"+str(_id)+".csv", header=False, index=False)

        for y in cells:
            try:
                full_fdict[y[0]] = int(y[1])
            except:
                pass
            #check for top 10k terms
            try:
                test = dict_of_10k[y[0]]
                fdict[y[0]] = int(y[1])
            except:
                pass
