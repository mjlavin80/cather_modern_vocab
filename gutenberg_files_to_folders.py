import pandas as pd
import re

#anchor to approximate start and end using keyphrase
def strip_hf(gutenberg_text):
    m = re.sub( r'start.+?project gutenberg ebook.+?\*\*\*', '<begin>', gutenberg_text.lower())
    m= re.sub( r'end.+?project gutenberg ebook', '<end>', m)
    m = re.sub(r'\r', ' ', m)
    m = re.sub(r'\n', ' ', m)
    m = re.sub(r'\t', ' ', m)
    #tokenize and clip on tokens
    m_tokens = m.split(" ")
    # remove key phrases "project gutenberg ebook",
    # "project gutenberg", "gutenberg ebook", and "ebook"
    m_tokens_culled = []
    start = False
    for i in m_tokens:
        if i == "<end>":
            break
        if start == True:
            m_tokens_culled.append(i)
        if i == "<begin>":
            start = True
    #m_tokens_culled[:100], m_tokens_culled[-100:-1]
    return m_tokens_culled

#load guteneberg IDs I want
df = pd.read_csv("meta/finalmeta.csv")
df = df.loc[df['source'] == 'gutenberg']

ids = list(df['gutenberg_id'])

for _id in ids:
    _id = _id.replace(" ", "").split(";")
    all_text = []
    for i in _id:
        #remember to ignore \_excerpt files;
        if "_excerpt" not in i:
            location = "../gutenberg/files/"+str(i)+".txt"
            try:
                #find corresponding txt folder, open file
                with open(location) as f:
                    txt = f.read()
                all_text.append(txt)
                full_text = " ".join(all_text)
                #copy the file to repo with the same name, join multivolume

                #remove headers and footers before you join
                _id = [strip_hf(z) for z in _id]
                joined = "_".join(" ".join([e for e in _id])
                new_location = "txts/gutenberg_full_text/"+joined+".txt"
                with open(new_location, 'a') as fn:
                    fn.write(txt)
                fn.close()
            except:
                pass
