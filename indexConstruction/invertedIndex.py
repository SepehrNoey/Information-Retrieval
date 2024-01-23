from enum import Enum
import heapq
import pickle

class Posting:
    def __init__(self, docID: int, tf: int):
        self.__docID = docID
        self.__tf = tf

    def getTF(self):
        return self.__tf
    
    def getDocID(self):
        return self.__docID
    
class PositionalPosting(Posting):
    def __init__(self, docID, tf, positions):
        super().__init__(docID, tf)
        self.__positions = positions

class PostingsList:
    def __init__(self):
        self.__df = 0
        self.__list = []
        self.__tf_whole = 0

    def addPosting(self, p: Posting):
        self.__list.append(p)

    def incrementDF(self):
        self.__df += 1

    def countAllOccurrences(self):
        frequency = 0
        for posting in self.__list:
            frequency += posting.getTF()
        
        self.__tf_whole = frequency
        return frequency
    
    def getDF(self):
        return self.__df
    
    def getDocIdTFPairs(self):
        ls = []
        for p in self.__list:
            ls.append((p.getDocID(), p.getTF()))
        
        return ls

class InvertedIndexType(Enum):
    BASIC = 0
    POSITIONAL = 1
    

class InvertedIndex:
    def __init__(self, type : InvertedIndexType.POSITIONAL):
        self.__dictionary = {}
        self.__docCount = 0

        if type in [InvertedIndexType.POSITIONAL, InvertedIndexType.BASIC]:
            self.__type = type
        else:
            raise ValueError(f"inverted index of type {type} is not supported")
        
    def addPosting(self, term: str, docID: int, tf: int, positions = None):
        if term not in self.__dictionary:
            self.__dictionary[term] = PostingsList()
        
        self.__dictionary[term].incrementDF()
        if self.__type == InvertedIndexType.BASIC:
            self.__dictionary[term].addPosting(Posting(docID, tf))
        elif self.__type == InvertedIndexType.POSITIONAL:
            self.__dictionary[term].addPosting(PositionalPosting(docID, tf, positions))

    def deleteMostRepeated(self, k: int):
        term_freq_heap = [] # using a max heap for deleting top k repeated
        for key in self.__dictionary:
            heapq.heappush(term_freq_heap, (-self.__dictionary[key].countAllOccurrences(), key))

        to_be_deleted = []
        for _ in range(k):
            item = heapq.heappop(term_freq_heap)
            self.__deleteTerm(item[1])
            to_be_deleted.append(item)
        
        return [(-key, value) for key, value in to_be_deleted]

    def __deleteTerm(self, term):
        self.__dictionary.pop(term)

    def getPostingList(self, term: str) -> PostingsList:
        if term not in self.__dictionary:
            return None
        
        return self.__dictionary[term]

    def save(self, obj, path, mode):
        with open(path, mode) as file:
            pickle.dump(obj, file)
        print(f"{obj} saved.")

    
    def load(self, path, mode):
        with open(path, mode) as file:
            obj = pickle.load(file)
        
        return obj

    def incrementDocCount(self, num):
        self.__docCount += num

    def getDocCount(self):
        return self.__docCount

