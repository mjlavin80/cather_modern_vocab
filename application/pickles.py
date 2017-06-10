from application import db
from application.models import *
import pymysql
from collections import Counter
from config import USER, PWD
import pickle
import sys, os

#define pickle object
class pickledData():
    def __init__(self):
        self.set_data_variables()
    def set_data_variables(self):
        try:
            self.metadata = pickle.load( open( "pickled_data/metadata.p", "rb" ) )
            self._ids = [p[0] for p in self.metadata]
            self.dates = [q[1] for q in self.metadata]
            self.genres = [r[2] for r in self.metadata]
            self.authors = [s[3] for s in self.metadata]
            self.titles = [t[4] for t in self.metadata]
            self.big_genres = [u[5] for u in self.metadata]
            self.lavin_genres = [v[6] for v in self.metadata]
            self.processed_genres = [w[7] for w in self.metadata]
        except:
            # get ids, store order here
            self._ids_dates_authors_titles  = [[i.id, i.firstpub, i.author, i.title] for i in db.session.query(Metadata).all()]
            self.genres = []
            self._ids = [p[0] for p in self._ids_dates_authors_titles]
            self.dates = [q[1] for q in self._ids_dates_authors_titles]
            self.authors = [r[2] for r in self._ids_dates_authors_titles]
            self.titles = [s[3] for s in self._ids_dates_authors_titles]
            for _id in self._ids:
                #get genres
                genre_rows  = [i.genre for i in db.session.query(Genres).filter(Genres.work_id==_id).all()]
                #mush genres to string
                g = " | ".join(genre_rows)
                #append
                self.genres.append(g)
            #define big and lavin here
            from application.selective_features import make_genres_big_and_lavin
            self.processed_genres, self.big_genres, self.lavin_genres = make_genres_big_and_lavin(self.genres)

            self.metadata = list(zip(self._ids, self.dates, self.genres, self.authors, self.titles, self.big_genres, self.lavin_genres, self.processed_genres))
            pickle.dump(self.metadata, open( "pickled_data/metadata.p", "wb" ) )
        #load feature dict from pickle
        try:
            self.feature_dicts = pickle.load( open( "pickled_data/feature_dicts.p", "rb" ) )
            print("Loaded pickle data successfully.")

        except:
            #\print("Did not find feature data in pickle form. Creating pickle for future use.")
            self.feature_dicts = []

            for _id in self._ids:
                feature_dict = {}
                # get types and counts
                query = "".join(["SELECT type, type_count FROM counts WHERE work_id=", str(_id), " AND type REGEXP '^[A-Za-z]+$';"])
                #loop terms matching certain criteria (regex query)

                conn = pymysql.connect(host='localhost', port=3306, user=USER, passwd=PWD, db='horror')
                cur = conn.cursor()

                a = cur.execute(query)
                for row in cur:
                    #add to dict if ok to use
                    if row[0] in features:
                        feature_dict[row[0]] = row[1]
                self.feature_dicts.append(feature_dict)

            print("Finished making dictionaries")
            pickle.dump( feature_dicts, open( "pickled_data/feature_dicts.p", "wb" ) )
            cur.close()
            conn.close()
