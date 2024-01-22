from hazm import Stemmer

def stem(word: str):
    stemmer = Stemmer()
    return stemmer.stem(word)