import hazm

lem = hazm.Lemmatizer()
print(lem.lemmatize('رفته', 'V'))
stem = hazm.Stemmer()
print(stem.stem('زلزله‌زدگان'))