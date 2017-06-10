#linear regression on 10k features to predict date

#from sklearn.metrics import recall_score
#from application.selective_features import make_feature_list, dictionaries_of_features, make_genres_big_and_lavin
import sqlite3
from random import shuffle
import pickle
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression

#load 10k feature dicts and metadata
metadata = pickle.load( open( "pickled_data/metadata.p", "rb" ) )
feature_dicts = pickle.load( open( "pickled_data/feature_dicts_10k.p", "rb" ) )
#print(len(metadata), len(feature_dicts))

def predict_years(metadata, feature_dicts):

    all_years = [int(i[8]) for i in metadata]
    all_ids = [i[0] for i in metadata]
    myrange = list(range(0, len(metadata)))
    shuffle(myrange)

    randoms = myrange[:500]
    randoms.sort()

    #define train_years, test_years
    train_years = []
    test_years = []

    #define train_dicts, test_dicts
    train_dicts = []
    test_dicts = []

    train_ids = []
    test_ids = []

    for num in myrange:
        if num in randoms:
            train_years.append(all_years[num])
            train_dicts.append(feature_dicts[num])
            train_ids.append(all_ids[num])
        else:
            test_years.append(all_years[num])
            test_dicts.append(feature_dicts[num])
            test_ids.append(all_ids[num])

    #print(len(train_years) == len(train_dicts))
    #print(len(test_years) == len(test_dicts))
    train_ids_str = ", ".join(train_ids)
    test_ids_str = ", ".join(test_ids)

    #use scikit learn Pipeline functionality to vectorize from dictionaries, run tfidf, and perform linear regression
    text_clf = Pipeline([('vect', DictVectorizer()), ('tfidf', TfidfTransformer()),('clf', LinearRegression()),])
    text_clf = text_clf.fit(train_dicts, train_years)
    predicted = text_clf.predict(test_dicts)

    result_rows = []
    margin = []
    for i,j in enumerate(predicted):
        m = abs(j - test_years[i])
        margin.append(m)
        row = [test_ids[i], j, test_years[i], m]
        rows.append(row)

    mean = np.mean(margin)
    main_row = [test_ids_str, train_ids_str, mean]
    return (main_row, result_rows)

def store_results(main_row, result_rows):
    conn = sqlite3.connect('regression_scores.db')
    c = conn.cursor()
    make_main = """CREATE TABLE IF NOT EXISTS main (id INTEGER PRIMARY KEY, test_ids TEXT, train_ids TEXT, mean_margin REAL)"""
    c.execute(make_main)
    make_results = """CREATE TABLE IF NOT EXISTS results (id INTEGER PRIMARY KEY, main_id INTEGER, doc_id TEXT, predicted REAL, actual REAL, margin REAL, FOREIGN KEY(main_id) REFERENCES main(id))"""
    c.execute(make_results)

    insert_main = """INSERT INTO main (id, test_ids, train_ids, mean_margin) VALUES (null, ?, ?, ?)"""
    c.execute(insert_main, main_row)
    conn.commit()

    #get id for row you just inserted
    main_id = c.execute("""SELECT id FROM main ORDER BY id DESC""").fetchone()[0]
    insert_result = """INSERT INTO results (id, main_id, doc_id, predicted, actual, margin) VALUES (null, ?, ?, ?, ?, ?)"""
    for result_row in result_rows:
        new_row = [main_id]
        new_row.extend(result_row)
        c.execute(insert_result, new_row)
    conn.commit()

for z in range(300):
    if z % 10 == 0:
        print(z)
    result_tuple = predict_years(metadata, feature_dicts)
    store_results(result_tuple[0], result_tuple[1])

#this code represents how to predicts year values using a model that can't use the pipeline
# from sklearn.naive_bayes import GaussianNB
# dict_vect = DictVectorizer()
# X_train_values = dict_vect.fit_transform(train_dicts)
# clf = GaussianNB()
# tfidf_transformer = TfidfTransformer()
# X_train_tfidf = tfidf_transformer.fit_transform(X_train_values)
# clf.fit(X_train_tfidf.toarray(), train_years)
#
# X_test_values = dict_vect.fit_transform(test_dicts)
# X_test_tfidf = tfidf_transformer.fit_transform(X_test_values)
# predicted = clf.predict(X_test_tfidf.toarray())
#
# margin = []
# for i,j in enumerate(predicted):
#     #print(j, test_years[i], abs(j - test_years[i]))
#     m = abs(j - test_years[i])
#     margin.append(m)
#
# print(np.mean(margin))
