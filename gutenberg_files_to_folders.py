import pandas as pd
#load guteneberg IDs I want
df = pd.DataFrame("meta/finalmeta.csv")
df = df.loc[df['source']== 'gutenberg']

ids = list(df['gutenberg_id'])

for _id in ids:
    _id = _id.split(";")
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
                joined = "_".join(_id)
                new_location = "txts/gutenberg_full_text/"+joined+".txt"
                with open(new_location, 'a') as fn:
                    fn.write(txt)
                fn.close()
            except:
                pass
