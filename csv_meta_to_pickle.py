#lavin csv_meta_to_pickle

import pickle
import csv

excluded = pickle.load( open( "pickled_data/excluded_ids.p", "rb" ) )

meta = []
with open ("meta/finalmeta.csv", "r", encoding="latin-1") as myfile:
    for h, m_line in enumerate(csv.reader(myfile)):
        if h > 0:
            if m_line[3] not in excluded:
                meta.append(m_line)

pickle.dump(meta, open( "pickled_data/metadata.p", "wb" ))
print(excluded)
