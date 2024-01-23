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

ii = InvertedIndex(InvertedIndexType.POSITIONAL)

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
    
    ii.incrementDocCount(1)

    if (i + 1) % 500 == 0:
        print("done processing doc: ", i + 1)

deleted = ii.deleteMostRepeated(50)
ii.save(deleted, "deleted-terms.pkl", "wb")
ii.save(ii, "ii.pkl", "wb")