import sys
sys.path.append("D:/AUT/Term 7/Information Retrieval/Project/indexConstruction")
sys.path.append("D:/AUT/Term 7/Information Retrieval/Project/preprocess")
sys.path.append("D:/AUT/Term 7/Information Retrieval/Project/queryProcessing")
sys.path.append("D:/AUT/Term 7/Information Retrieval/Project")
import time
import json

file_path = "C:/Users/Lenovo/Downloads/Telegram Desktop/IR_data_news_12k.json"

with open(file_path, 'r') as file:
    data = json.load(file)

from queryProcessing.queryProcessor import QueryProcessor
from queryProcessing.queryProcessor import PositionalQueryProcessor
from queryProcessing.queryProcessor import EfficientQueryProcessor
from indexConstruction.invertedIndex import InvertedIndex

def print_results(result):
    for i in range(len(result)):
        if isinstance(result[i], tuple):
            json_id_str = str(result[i][0] - 1)
            print(f"DocID in json: {json_id_str}, Score: {result[i][1]}, Title: {data[json_id_str]['title']}, URL: {data[json_id_str]['url']}")
        else:
            json_id_str = str(result[i] - 1)
            print(f"DocID in json: {json_id_str}, Score: PHRASE-QUERY-RESULT, Title: {data[json_id_str]['title']}, URL: {data[json_id_str]['url']}")
        
        print("**** ****\n")
            
def print_in_red(str):
    print(f"\033[91m{str}\033[0m")

ii = InvertedIndex.load("ii.pkl", "rb")
champII = InvertedIndex.load("champII.pkl", "rb")
qp = QueryProcessor(ii)
qp2 = PositionalQueryProcessor(ii)
qp3 = EfficientQueryProcessor(ii, champII)

start = time.time()
res = qp.search("رامین رضاییان", 10)
end = time.time()
print_in_red(f"normal cosine search spent time: {end - start}, result is:")
print_results(res)

start = time.time()
res2 = qp2.search("رامین رضاییان", 10)
end = time.time()
print_in_red(f"\npositional + normal cosine search spent time: {end - start}, result is:")
print_results(res2)
# deleted = InvertedIndex.load("deleted-terms.pkl", "rb")
# print("deleted:", deleted)

start = time.time()
res3 = qp3.search("رامین رضاییان", 10)
end = time.time()
print_in_red(f"\nchamp list + normal cosine search spent time: {end - start}, result is:")
print_results(res3)
