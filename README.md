# Text files

Method:

I begin with Ted Underwood and Jordan Sellers corpus of 3,724 texts. Isolate fiction more than 3,000 words long. Especially focusing on post-1850 texts, match as many as you can to specific Gutenberg IDs. Using author-title fuzzy match, I identify candidates and hand correct. Files will be named some_id.txt and a Gutenberg_ID field is added to metadata.csv for joining. Some Gutenberg texts are anthologies that include a particular text. If so, add \_excerpt to the filename. If the text is split across multiple IDs (multivolume), separate relevant Gutenberg IDs with a semicolon, and constructed a super text with the filename structured like this: ID_ID_ID.txt. If the Underwood version is multivolume, but Gutenberg isn't I'll put the relevant ID data in the cell for volume 1 only. (At this point, I derived 138 texts.)

I add other Gutenberg novels to the corpus by repeating this process for texts pre-1850. (This brings me from 138 to 265.)

To combine all this with Underwood's Genre corpus (important for bringing in more diversity of texts, and more date coverage) I've chosen to skip the Gutenberg join process and rely on term frequency (bag of words) data only. The purpose here is to have a base of texts for certain measures that depend on word order (like POS tagging) and use the secondary corpus to fill out date prediction models and such. To make sure I don't produce unnecessary duplication (some texts in one corpus are also in the other), I've used fuzzy matching to find the Underwood-Sellers-3724 title that most closely matches each Underwood-genres title. I have also removed one non-English source from Underwood-genres corpus (incorrectly designated as English language in HathiTrust metadata) and hand-corrected several dates of first publication that came up as suspicious after running this analysis: http://thedatahumanist/neologophobia. The full list of changes is in excluded_or_corrected.csv.

Finally, I add some texts of interests by hand. I plan to add more as I prepare this for publication. Some texts are hard to find or are out of copyright and thus I would have to digitize them, transform ebooks to term frequency tables, or find in a non-consumptive term frequency corpus like HTRC.

Add as much as possible without computational assistance:

- Cather novels
- More works by specific authors
- Texts by authors with known connection to Cather (Canfield, Jewett, Wharton, James, Conrad, Tarkington, etc.)
- Other women writers: Ferber, Gilman, Chopin, Larsen, Stein, Woolf, Kathleen Norris, Edith M. Hull, Pearl Buck, Viña Delmar, Mary Roberts Rinehart, Anne Douglas Sedgwick (The Little French Girl), Eleanor Abbott, Margaret Deland, Eleanor H. Porter,
- African American writers
- Native American writers
- Pulp and popular (consult genres list and match Gutenberg)
- Irish novelists
- 1920s: Faulkner, Fitzgerald, Hemingway, Steinbeck, Stein, Woolf, etc.

# Load Text Files into Test Code

Things to remember ...
Gutenberg folder: ignore \_excerpt files; strip header and footer, join multivolume, eventually convert to list of dictionaries
Other folder: should be all single volume .txt files ... needs a metadata csv. check for dupes by hand.
Underwood_genres ... Use script for semi-automated de-duping. Ignores rows with 'exclude' in the first cell. Only use these data for regression tests?
Need to revise test function or run_tests to skip bootstrapping on basic measures
Need to add in syllables per word analysis and add to output db


# Metadata

# Generating Pickle files

### Best Order of pickle scripts
csv_to_pickle.py ... pulls from meta/finalmeta.csv, converts full text to tsvs and slices gutenberg headers and footers

check these:
csv_meta_to_pickle.py ...
original genres ... only runs on underwood_genres texts, bit essential but might use this later

# Tests

- Lexical richness (can be done from dictionaries)
- Latinate-Germanic divide (dictionaries)


- Parts-of-speech ... adjectives and adverbs ... use spacy, run on gutenberg and other
- Average syllables-per-word ... run on gutenberg and other

# Other Tests (If Time)
- Sentence length?
- I, he, she, etc.
- Sentiment
- Non-standard English words
