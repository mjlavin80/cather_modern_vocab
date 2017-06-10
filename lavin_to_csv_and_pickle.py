#lavin texts to csv and pickle
import pickle
import csv
import glob
from collections import Counter

docids = []
with open ("meta/finalmeta.csv", "r") as myfile:
    for m_line in csv.reader(myfile):
        if m_line[0] != "docid":
            docids.append(m_line[0])

feature_dicts = pickle.load( open( "pickled_data/feature_dicts.p", "rb" ) )
metadata = pickle.load( open( "pickled_data/metadata.p", "rb" ) )
excluded = pickle.load( open( "pickled_data/excluded_ids.p", "rb" ) )

dict_of_10k = {}
with open ("lexicon/new10k.csv", "r") as myfile:
    for m_line in csv.reader(myfile):
        if m_line[0] != "word":
            dict_of_10k[m_line[0]] = m_line[1]

text = glob.glob('lavin_additional_texts/*.txt')
lavin_meta = {}

with open ("lavin_meta/lavin_meta.csv", "r") as myfile:
    for m_line in csv.reader(myfile):
        if m_line[0] != "docid":
            if m_line[0] not in excluded:
                lavin_meta[m_line[0]] = m_line

for filename in text:
    lavin_id = filename.replace("lavin_additional_texts/","").replace(".txt", "")
    #open and read()
    with open(filename) as f:
        md_text = f.read()
    #tokenize, lowercase, remove newlines and tabs, strip punctuation and numbers
    #convert newlines and tabs to spaces
    md_text = md_text.replace('\n', ' ').replace('\t', ' ')
    #remove no-alpha characters, convert all to lowercase
    md_no_punct = ''.join(char.lower() if char.isalpha() else ' ' for char in md_text )
    #tokenize and drop empty list items
    md_tokens = [i for i in md_no_punct.split(' ') if i != '']
    #convert to counter
    md_counts = Counter(md_tokens).items()
    processing_dict = {}
    for term, count in md_counts:
        try:
            test = dict_of_10k[term]
            processing_dict[term] = count
        except:
            pass
    feature_dicts.append(processing_dict)
    meta_tuple = lavin_meta[lavin_id]
    print(meta_tuple)
    metadata.append(meta_tuple)

pickle.dump(feature_dicts, open( "pickled_data/feature_dicts.p", "wb" ))
pickle.dump(metadata, open( "pickled_data/metadata.p", "wb" ))
