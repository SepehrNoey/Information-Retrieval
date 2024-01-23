from preprocess.normalizer import normalize
from preprocess.tokenizer import tokenize
from preprocess.lemmatizer import lemmatize

def preprocess(str: str):
    str = normalize(str)
    tokens = tokenize(str)
    for j in range(len(tokens)):
        tokens[j] = lemmatize(tokens[j])
    
    return tokens