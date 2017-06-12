from collections import Counter
from random import shuffle
from ratio_functions import *
from sklearn.utils import resample
import sqlite3
from nltk.corpus import stopwords
import numpy
import json
import pickle

#dictionary_com
dictcom_dictionary = pickle.load( open( "pickled_data/dictcom_dict.p", "rb" ) )
oed_dictionary = pickle.load( open( "pickled_data/oed_dict.p", "rb" ) )

conn_w = sqlite3.connect('walker_datastore.db')
cw = conn_w.cursor()

walker_query = """SELECT term FROM counts LEFT JOIN terms ON counts.term_id=terms.id"""
walker_terms = [i[0] for i in cw.execute(walker_query).fetchall()]

#walker dictionary
walker_dictionary = Counter(walker_terms)
stops = stopwords.words('English')


#create results_db here
conn = sqlite3.connect('all_measures_fiction_sliced.db')
c = conn.cursor()
create = """CREATE TABLE IF NOT EXISTS results (id INTEGER PRIMARY KEY, is_resample INTEGER, test_train INTEGER, doc_id TEXT, tt_ratio REAL,
oed_ratio_no_set REAL, oed_matched_no_set REAL, oed_passed_no_set REAL, oed_neo BLOB, oed_ratio_set REAL,
oed_matched_set REAL, oed_passed_set REAL, oed_neo_set BLOB, gl_ratio_no_set REAL, matched_no_set REAL, passed_no_set REAL,
neo BLOB, gl_ratio_set REAL, matched_set REAL, passed_set REAL, neo_set BLOB, walker_ratio_no_set REAL, walker_matched_no_set REAL,
walker_passed_no_set REAL, walker_ratio_set REAL, walker_matched_set REAL, walker_passed_set REAL)"""
c.execute(create)
insert = """INSERT INTO results (id, is_resample, test_train, doc_id, tt_ratio, oed_ratio_no_set, oed_matched_no_set, oed_passed_no_set,
oed_neo, oed_ratio_set, oed_matched_set, oed_passed_set, oed_neo_set, gl_ratio_no_set, matched_no_set, passed_no_set,
neo, gl_ratio_set, matched_set, passed_set, neo_set, walker_ratio_no_set, walker_matched_no_set, walker_passed_no_set,
walker_ratio_set, walker_matched_set, walker_passed_set) VALUES (null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

full_feature_dicts = pickle.load( open( "pickled_data/full_feature_dicts.p", "rb" ) )

# function to remove stopwords from a dictionary
def remove_stops_from_dicts(mydict, stoplist):
    for i in stoplist:
        try:
            del mydict[i]
        except:
            pass

    return mydict

# remove stops from full_feature_dicts
feature_dicts_no_stops = []
for i in full_feature_dicts:
    result = remove_stops_from_dicts(i, stops)
    feature_dicts_no_stops.append(result)

#load metadata for db output
metadata = pickle.load( open( "pickled_data/metadata.p", "rb" ) )

print(len(metadata), len(full_feature_dicts))

for i, _dict in enumerate(feature_dicts_no_stops):
    is_resample = 0
    _tuples = _dict.items()
    doc_id = metadata[i][3]
    expanded = counts_to_shuffled(_tuples)

    if len(expanded) > 2800:
        expanded_sliced = expanded[:2800]

        #to analyze as set, run same functions on as_set
        #as_set = [f[0] for f in _tuples]
        as_set = [f[0] for f in list(Counter(expanded_sliced).items())]

        test_train = None
        tt_ratio = float(len(as_set))/len(expanded_sliced)

        #calculate walker, oed, and dictcom ratios, plus to neologism scores for all, cluster_train, cluster_test
        results = run_all_ratios(expanded_sliced, as_set, oed_dictionary, dictcom_dictionary, walker_dictionary)
        row = [is_resample, test_train, doc_id, tt_ratio]
        row.extend(results)
        #store in db ... make each a row, all the same
        c.execute(insert, row)
        conn.commit()
        #expanded = numpy.asarray(expanded)
