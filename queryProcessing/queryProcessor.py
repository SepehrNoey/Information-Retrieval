from indexConstruction.invertedIndex import InvertedIndex
from preprocess.preprocessor import preprocess
from math import log10, sqrt
import heapq

class QueryProcessor:
    def __init__(self, ii: InvertedIndex):
        self._ii = ii

    def search(self, query: str, k: int):
        return self._findKRelevant(self._ii, query, k)

    def _findKRelevant(self, ii: InvertedIndex, query: str, k: int):
        query = query.strip()
        tokens = preprocess(query)
        to_be_deleted = []
        for i in range(len(tokens)):
            pl = ii.getPostingList(tokens[i])
            if pl is None:
                to_be_deleted.append(i)
        
        to_be_deleted.sort(reverse=True)
        for i in to_be_deleted:
            tokens.pop(i)
        
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
        pl = self._ii.getPostingList(token)
        id_tf_pairs = pl.getDocIdTFPairs()
        df = pl.getDF()
        doc_scores = {}
        for (id, tf) in id_tf_pairs:
            doc_scores[id] = (1 + log10(tf)) * log10(self._ii.getDocCount() / df)
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

        score = 0.0
        for t in a_vector:
            if t in b_vector:
                score += (a_vector[t] / squared_sum_a) * (b_vector[t] / squared_sum_b)
        
        return score
    

class PositionalQueryProcessor(QueryProcessor):
    def __init__(self, ii: InvertedIndex):
        super().__init__(ii)

    def search(self, query: str, k: int):
        return self._findKRelevant(self._ii, query, k)

    def _findKRelevant(self, ii: InvertedIndex, query: str, k: int):
        query = query.strip()
        tokens = preprocess(query)
        to_be_deleted = []
        for i in range(len(tokens)):
            pl = ii.getPostingList(tokens[i])
            if pl is None:
                to_be_deleted.append(i)
        
        to_be_deleted.sort(reverse=True)
        for i in to_be_deleted:
            tokens.pop(i)

        found_docs = []

        for i in range(len(tokens), 1, -1): # phrase queries of length i
            subphrase_start = 0
            for j in range(len(tokens) - i + 1): # subphrase numbers
                postings_postingPtr_posPtr = {}
                for l in range(i):
                    ls = []
                    ls.append(ii.getPostingList(tokens[subphrase_start + l]).getPostings()) # postings of this token
                    ls.append(0) # index of last processed doc
                    ls.append(0) # index of last processed position in that doc
                    
                    postings_postingPtr_posPtr[subphrase_start + l] = ls

                first_token_things = postings_postingPtr_posPtr[subphrase_start]
                for p in range(len(first_token_things[0])): # at most we need to search len(first token postings list) 
                    curr_posting = first_token_things[0][p]
                    curr_posIndex = first_token_things[2]
                    doc_condition = True
                    
                    for l in range(1, len(postings_postingPtr_posPtr), 1):
                        if not doc_condition:
                            break

                        otherToken_postings = postings_postingPtr_posPtr[subphrase_start + l][0]
                        otherToken_docIndex = postings_postingPtr_posPtr[subphrase_start + l][1]
                        otherToken_posIndex = postings_postingPtr_posPtr[subphrase_start + l][2]
                        
                        otherDoc_condition = True

                        for m in range(otherToken_docIndex, len(otherToken_postings), 1):
                            if not otherDoc_condition:
                                break

                            if curr_posting.getDocID() < otherToken_postings[m].getDocID():
                                doc_condition = False
                                break
                            elif curr_posting.getDocID() > otherToken_postings[m].getDocID():
                                # postings_postingPtr_posPtr[subphrase_start + l][1] += 1
                                continue
                            else: # docID is same, search for successive postions
                                pos_condition = True

                                for n in range(curr_posIndex, len(curr_posting.getPositions()), 1):
                                    if not pos_condition:
                                        break
                                    
                                    curr_positions = curr_posting.getPositions()
                                    otherToken_positions = otherToken_postings[m].getPositions()

                                    for q in range(otherToken_posIndex, len(otherToken_positions), 1):
                                        if otherToken_positions[q] - curr_positions[n] == l:
                                            # found successive positions
                                            
                                            if l == len(postings_postingPtr_posPtr) - 1: # if we are processing the last token in subphrase
                                                if otherToken_postings[m].getDocID() not in found_docs:
                                                    found_docs.append(otherToken_postings[m].getDocID())
                                            otherDoc_condition = False
                                            pos_condition = False
                                            break
                                        elif otherToken_positions[q] - curr_positions[n] > l:
                                            break
                                        else:
                                            continue

                subphrase_start += 1
        
        if len(found_docs) < k:
            qp = QueryProcessor(self._ii)
            res = qp._findKRelevant(ii, query, 4 * k)
            for i in range(len(res)):
                if res[i][0] not in found_docs:
                    found_docs.append(res[i])
                if len(found_docs) == k:
                    break
        elif len(found_docs) > k:
            for i in range(len(found_docs) - k):
                found_docs.pop()
           
        return found_docs
    
class EfficientQueryProcessor(QueryProcessor):
    def __init__(self, ii: InvertedIndex, championII: InvertedIndex):
        super().__init__(ii)
        self.__championII = championII

    def search(self, query: str, k: int):
        cham_res = super()._findKRelevant(self.__championII, query, k)
        if len(cham_res) < k:
            normal_res = super()._findKRelevant(self._ii, query, 2 * k)
            for i in range(len(normal_res)):
                if normal_res[i] not in cham_res:
                    cham_res.append(normal_res[i])

        return cham_res