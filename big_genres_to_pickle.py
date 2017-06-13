#add big genres to metadata pickle
import pickle
metadata = pickle.load( open( "pickled_data/metadata.p", "rb" ) )

print(metadata[0])

# piped_genres = [i[14] for i in metadata]
# #define big and lavin here
# from application.selective_features import make_genres_big_and_lavin
# processed_genres, big_genres, lavin_genres = make_genres_big_and_lavin(piped_genres)
# print(big_genres)
