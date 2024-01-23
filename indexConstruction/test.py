import hazm

stem = hazm.Stemmer()
print(stem.stem('محمدحسین'))
tagger = hazm.POSTagger(model='C:/Users/Lenovo/Downloads/pos_tagger.model')
tokens = hazm.word_tokenize('محمدحسین')
print(tagger.tag(tokens[0]))
print("token is:", tokens[0])
print(hazm.Lemmatizer().lemmatize(tokens[0], 'V'))