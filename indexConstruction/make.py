import sys
sys.path.append("D:/AUT/Term 7/Information Retrieval/Project/indexConstruction")
sys.path.append("D:/AUT/Term 7/Information Retrieval/Project/preprocess")
sys.path.append("D:/AUT/Term 7/Information Retrieval/Project")

import json
from preprocess.preprocessor import preprocess
from indexConstruction.invertedIndex import InvertedIndex, InvertedIndexType


file_path = "C:/Users/Lenovo/Downloads/Telegram Desktop/IR_data_news_12k.json"

with open(file_path, 'r') as file:
    data = json.load(file)

ii = InvertedIndex(InvertedIndexType.POSITIONAL, len(data))
champII = InvertedIndex(InvertedIndexType.POSITIONAL, len(data))

for i in range(len(data)):
    content = data[str(i)]['content']
    tokens = preprocess(content)
    
    doc_terms = {}
    for j in range(len(tokens)):
        if tokens[j] not in doc_terms:
            doc_terms[tokens[j]] = [0, []]
        
        doc_terms[tokens[j]][0] += 1
        doc_terms[tokens[j]][1].append(j + 1)
    
    for key in doc_terms:
        ii.addPosting(key, i + 1, doc_terms[key][0], doc_terms[key][1])
        # if tf >= 3, so it's a good doc to be in champion list
        if doc_terms[key][0] >= 3:
            champII.addPosting(key, i + 1, doc_terms[key][0], doc_terms[key][1])
    

    if (i + 1) % 500 == 0:
        print("done processing doc: ", i + 1)

ii_deleted = ii.deleteMostRepeated(50)
champII_deleted = champII.deleteMostRepeated(50)
InvertedIndex.save(ii_deleted, "ii-deleted-terms.pkl", "wb")
InvertedIndex.save(ii, "ii.pkl", "wb")
InvertedIndex.save(champII_deleted, "champII-deleted-terms.pkl", "wb")
InvertedIndex.save(champII, "champII.pkl", "wb")