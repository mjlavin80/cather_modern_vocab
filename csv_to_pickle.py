import pickle
import csv
import re
from collections import Counter
import pandas as pd
import string

dict_of_10k = {}
with open ("lexicon/new10k.csv", "r") as myfile:
    for m_line in csv.reader(myfile):
        if m_line[0] != "word":
            dict_of_10k[m_line[0]] = m_line[1]

df_meta = pd.read_csv("meta/finalmeta.csv", encoding="latin-1")
docids = list(df_meta['gutenberg_id'])
sources = list(df_meta['source'])

full_feature_dicts = []
feature_dicts = []
excluded_ids = []


for count, _id in enumerate(docids):
    found = 0
    print(_id)
    #handle semicolon data
    _id_name = _id.replace(";", "_")

    #if it's in gutenberg_full_text
    if sources[count] == 'gutenberg':
        full_fdict = {}
        fdict = {}
        try:
            with open("txts/gutenberg_full_text/%s.txt" % str(_id_name)) as f:
                #lowercase
                s = f.read().lower().replace("\n", " ").replace("\r", " ").replace("\t", " ")

            #tokenize and convert to term frequency table, cells = list of term, count tuples
            tokens = s.split(" ")
            tokens = [s.translate(str.maketrans('','',string.punctuation)) for s in tokens]
            tokens = [s.translate(str.maketrans('','','1234567890')) for s in tokens]

            cells = Counter(tokens)
            try:
                del cells['']
            except:
                pass
            c = list(cells.items())

            #write tsv to folder
            df_cells = pd.DataFrame.from_records(c, columns=["term", "count"]).sort_values(by="count", ascending=False)

            #df_cells.to_csv("txts/gutenberg_tsv/"+str(_id_name)+".tsv", sep="\t", header=False, index=False)

            for y in c:
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
            full_feature_dicts.append(full_fdict)
            feature_dicts.append(fdict)
            found=1
        except:
            pass
    #try as if it's others_full_text
    if sources[count] == "lavin":
        full_fdict = {}
        fdict = {}

        with open("txts/other_full_text/%s.txt" % str(_id_name)) as f:
            #lowercase
            s = f.read().lower().replace("\n", " ").replace("\r", " ").replace("\t", " ")
        #tokenize and convert to term frequency table, cells = list of term, count tuples
        tokens = s.split(" ")

        tokens = [s.translate(str.maketrans('','',string.punctuation)) for s in tokens]
        tokens = [s.translate(str.maketrans('','','1234567890')) for s in tokens]

        cells = Counter(tokens)
        try:
            del cells['']
        except:
            pass
        c = list(cells.items())


        #write tsv to folder
        df_cells = pd.DataFrame.from_records(c, columns=["term", "count"]).sort_values(by="count", ascending=False)

        #df_cells.to_csv("txts/other_tsv/"+str(_id_name)+".tsv", sep="\t", header=False, index=False)

        for y in c:
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
        full_feature_dicts.append(full_fdict)
        feature_dicts.append(fdict)
        found = 2
    #process from genrescorpus
    if sources[count] == "genrescorpus":
        full_fdict = {}
        fdict = {}
        with open("txts/genrescorpus/%s.fic.tsv" % str(_id_name)) as f:
            s = f.read()
            s = s.replace("\n\"\t", "\n\\\"\t")
            row = s.split("\n")
            cells = [tuple(i.split("\t")) for i in row]
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
        full_feature_dicts.append(full_fdict)
        feature_dicts.append(fdict)
        found=3
    print(found)
    if found == 0:
        excluded_ids.append(_id)
    print(count+1, len(full_feature_dicts)+len(excluded_ids))

pickle.dump(feature_dicts, open( "pickled_data/feature_dicts_10k.p", "wb" ))
pickle.dump(full_feature_dicts, open( "pickled_data/full_feature_dicts.p", "wb" ))
pickle.dump(excluded_ids, open( "pickled_data/excluded_ids.p", "wb" ))

print(len(excluded_ids))
