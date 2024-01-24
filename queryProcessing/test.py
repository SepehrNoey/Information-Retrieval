import sys
sys.path.append("D:/AUT/Term 7/Information Retrieval/Project/indexConstruction")
sys.path.append("D:/AUT/Term 7/Information Retrieval/Project/preprocess")
sys.path.append("D:/AUT/Term 7/Information Retrieval/Project/queryProcessing")
sys.path.append("D:/AUT/Term 7/Information Retrieval/Project")
import time


from queryProcessing.queryProcessor import QueryProcessor
from queryProcessing.queryProcessor import PositionalQueryProcessor
from queryProcessing.queryProcessor import EfficientQueryProcessor
from indexConstruction.invertedIndex import InvertedIndex

ii = InvertedIndex.load("ii.pkl", "rb")
champII = InvertedIndex.load("champII.pkl", "rb")
qp = QueryProcessor(ii)
qp2 = PositionalQueryProcessor(ii)
qp3 = EfficientQueryProcessor(ii, champII)

start = time.time()
res = qp.search("رامین رضاییان", 50)
end = time.time()
print(f"normal cosine search spent {end - start}, result is: {res}")

start = time.time()
res2 = qp2.search("رامین رضاییان", 50)
end = time.time()
print(f"\npositional + normal cosine search spent {end - start}, result is: {res2}")
# deleted = InvertedIndex.load("deleted-terms.pkl", "rb")
# print("deleted:", deleted)

start = time.time()
res3 = qp3.search("رامین رضاییان", 50)
end = time.time()
print(f"\nchamp list + normal cosine search spent {end - start}, result is: {res3}")
