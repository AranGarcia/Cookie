import spacy

# Delete this
import pickle

LEMMA_FILE = "lemmatization-es.txt"


def get_lemmas():
    lemmas = set()
    with open(LEMMA_FILE, encoding="utf8") as f:
        for line in f:
            lemma, word = line.split()
            lemmas.add(lemma)

    return sorted(lemmas)


print("loading Spacy...")
nlp = spacy.load("es_core_news_md")

print("Getting lemmas...")
lemma_list = get_lemmas()

print("Calculating vetors...")
vectors = []
for i, lem in enumerate(lemma_list, 1):
    print(f"{i}/{len(lemma_list)}")
    vectors.append(nlp(lem).vector)

print("Saving to vectors.bin")
with open("vectors.bin", "wb") as f:
    pickle.dump(vectors, f)
