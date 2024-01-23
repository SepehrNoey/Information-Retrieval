from hazm import Lemmatizer
from hazm import Stemmer

lem = Lemmatizer()
stem = Stemmer()

def lemmatize(word: str):
    word = stem.stem(word)
    return lem.lemmatize(word, 'V')