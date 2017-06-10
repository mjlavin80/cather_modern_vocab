import curses 
import nltk
from nltk.corpus import cmudict 
d = cmudict.dict() 

def nsyl(word): 
   return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]][0] 

#load pickles
#loop feature_dicts
#loop tokens
#compute ratios
#scale each to number of occurrences
#store results
print(nsyl('lazy'))
