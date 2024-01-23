from indexConstruction.invertedIndex import InvertedIndex
from preprocess.preprocessor import preprocess
from math import log10, sqrt
import heapq

class QueryProcessor:
    def __init__(self, ii: InvertedIndex):
        self.__ii = ii

    def findKRelevant(self, query: str, k: int):
        query = query.strip()
        tokens = preprocess(query)
        for i in range(len(tokens)):
            pl = self.__ii.getPostingList(tokens[i])
            if pl is None:
                tokens.remove(tokens[i])

        query_term_scores = {}
        query_term_freq = {}
        for t in tokens:
            if t not in query_term_freq:
                query_term_freq[t] = 0
            query_term_freq[t] += 1
        for t in query_term_freq:
            query_term_scores[t] = 1 + log10(query_term_freq[t])


        doc_term_scores = {}
        for t in tokens:
            scores = self.getTfIdfList(t)
            for id in scores:
                if id not in doc_term_scores:
                    doc_term_scores[id] = {}
                doc_term_scores[id][t] = scores[id]

        top_k_heap = []
        for docID, doc_vector in doc_term_scores.items():
            doc_score = self.getSimilarity(query_term_scores, doc_vector)
            heapq.heappush(top_k_heap, (-doc_score, docID))
        
        if len(top_k_heap) < k:
            k = len(top_k_heap)
        
        result = []
        for _ in range(k):
            neg_score, id = heapq.heappop(top_k_heap)
            result.append((id, -neg_score))
        
        return result
        

    def getTfIdfList(self, token: str):
        pl = self.__ii.getPostingList(token)
        id_tf_pairs = pl.getDocIdTFPairs()
        df = pl.getDF()
        doc_scores = {}
        for (id, tf) in id_tf_pairs:
            doc_scores[id] = (1 + log10(tf)) * log10(self.__ii.getDocCount() / df)
        return doc_scores

    def getSimilarity(self, a_vector: dict, b_vector: dict):
        squared_sum_a = 0.0
        squared_sum_b = 0.0

        for t in a_vector:
            squared_sum_a += a_vector[t] ** 2
        for t in b_vector:
            squared_sum_b += b_vector[t] ** 2
        
        squared_sum_a = sqrt(squared_sum_a)
        squared_sum_b = sqrt(squared_sum_b)

        processed_terms = {}
        score = 0.0
        for t in a_vector:
            if t in b_vector:
                score += (a_vector[t] / squared_sum_a) * (b_vector[t] / squared_sum_b)
        
        return score