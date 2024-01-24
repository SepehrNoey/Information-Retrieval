import sys
sys.path.append("D:/AUT/Term 7/Information Retrieval/Project/indexConstruction")
sys.path.append("D:/AUT/Term 7/Information Retrieval/Project/preprocess")
sys.path.append("D:/AUT/Term 7/Information Retrieval/Project/queryProcessing")
sys.path.append("D:/AUT/Term 7/Information Retrieval/Project")


from queryProcessing.queryProcessor import QueryProcessor
from queryProcessing.queryProcessor import PositionalQueryProcessor
from indexConstruction.invertedIndex import InvertedIndex

ii = InvertedIndex.load("ii.pkl", "rb")
qp = QueryProcessor(ii)

res = qp.findKRelevant("خبرگزاری فارس", 50)
print("normal:", res)

qp2 = PositionalQueryProcessor(ii)
res2 = qp2.findKRelevant("رامین رضاییان", 50)
print("\npositional:", res2)
# deleted = InvertedIndex.load("deleted-terms.pkl", "rb")
# print("deleted:", deleted)
