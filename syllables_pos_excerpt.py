import curses
import nltk
from nltk.corpus import cmudict
d = cmudict.dict()

def nsyl(word):
   return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]][0]

passage = """IT is sixteen years since John Bergson died. His wife now lies
beside him, and the white shaft that marks their graves gleams
across the wheat-fields. Could he rise from beneath it, he would
not know the country under which he has been asleep. The shaggy coat
of the prairie, which they lifted to make him a bed, has vanished
forever. From the Norwegian graveyard one looks out over a vast
checker-board, marked off in squares of wheat and corn; light and
dark, dark and light. Telephone wires hum along the white roads,
which always run at right angles. From the graveyard gate one can
count a dozen gayly painted farmhouses; the gilded weather-vanes
on the big red barns wink at each other across the green and brown
and yellow fields. The light steel windmills tremble throughout
their frames and tug at their moorings, as they vibrate in the wind
that often blows from one week’s end to another across that high,
active, resolute stretch of country."""
tokens = passage.split(" ")
result = []
for i in tokens:
    try:
        tag = "<term syllable_count=\'%s\'>%s</term>" % (nsyl(i), i)"
        result.append(tag)
    except:
        tag = <"term syllable_count=\'%s\'>%s</term>" % ("", i)
        result.append(tag)
with open("tagged_excerpt.txt", "a") as out:
    for e in result:
        out.write(result, " ")
