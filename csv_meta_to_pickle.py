#lavin csv_meta_to_pickle

import pickle
import csv

excluded = pickle.load( open( "pickled_data/excluded_ids.p", "rb" ) )

meta = []
with open ("meta/finalmeta.csv", "r") as myfile:
    for m_line in csv.reader(myfile):
        if m_line[0] != "docid":
            if m_line[0] not in excluded:
                meta.append(m_line)

pickle.dump(meta, open( "pickled_data/metadata.p", "wb" ))
