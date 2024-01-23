import sys
sys.path.append("D:/AUT/Term 7/Information Retrieval/Project/indexConstruction")
sys.path.append("D:/AUT/Term 7/Information Retrieval/Project/preprocess")
sys.path.append("D:/AUT/Term 7/Information Retrieval/Project/queryProcessing")
sys.path.append("D:/AUT/Term 7/Information Retrieval/Project")


from queryProcessing.queryProcessor import QueryProcessor
from indexConstruction.invertedIndex import InvertedIndex

ii = InvertedIndex.load("ii.pkl", "rb")
qp = QueryProcessor(ii)

res = qp.findKRelevant("اخبار", 50)
print(res)

# deleted = InvertedIndex.load("deleted-terms.pkl", "rb")
# print("deleted:", deleted)
