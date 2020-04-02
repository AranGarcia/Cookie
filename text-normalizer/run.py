#!/usr/bin/env python3
"""
Text normalizing script.

The input is any of the files stored in the Shepard repository, as they need to be preprocessed
before any information extraction or ETL processes can be performed upon them. This script will
do the following:

1) Stop-words filtering
    Removal of common words that are redundant and do not give much meaning to the text.
2) Lemmatization
    Since words can be derived into multiple conjugations, normalization to the lemma of each
    word will provide the main text data source for information retrieval.

Important resources:
https://www.analyticsvidhya.com/blog/2019/08/how-to-remove-stopwords-text-normalization-nltk-spacy-gensim-python/

"""

import sys

# Spacy
import spacy
from spacy.lang.es.stop_words import STOP_WORDS

# YAML
from yaml import Dumper, Loader, dump, load

if len(sys.argv) < 2:
    print("Usage\n\trun.py FILE [DEST]")
    exit(1)

# Unserialize data from YAML file
fname = sys.argv[1]
with open(fname) as f:
    data = load(f, Loader=Loader)

nlp = spacy.load("es_core_news_sm")


def iter_items(items):
    """Recursive legal file object text normalization."""
    for it in items:
        text = nlp(it["text"].lower())

        # Stop word removal
        token_list = [
            token.lemma_
            for token in text
            if not token.is_stop and not token.is_punct
        ]

        it["text"] = " ".join(token_list)

        children_items = it.get("content", {}).get("items")
        if children_items:
            iter_items(children_items)


# Remove stop words
iter_items(data["items"])

# Reserialize in another file
fname = "result.yaml"
with open(fname, "w") as f:
    dump(data, stream=f, encoding="utf-8", allow_unicode=True)
