
from math import log
from utilitiesFunction import getLineFromFile
from textProcessing import removeDiacritics, removeEchoCharacters
from bisect import bisect_left

#TODO: move to config file
NUMBER_OF_DOCUMENTS_RESULT = 20
PRODUCT_PATHFILE = '../sanbox/product_names.txt'
K1 = 1.2 #K1 in [1.2, 2.0]
B = 0.75

#singleton class
class BestMatch25:
    __instance = None
    def __init__(self):
        if BestMatch25.__instance == None:
            BestMatch25.__instance = BestMatch25.__BestMatch25()
    def search(self, text):
        return BestMatch25.__instance.search(text)

    @staticmethod
    def TF(term, document):
        result = 0
        doc_prc = removeDiacritics(document)
        doc_prc = removeEchoCharacters(doc_prc)
        term_prc = removeDiacritics(term)
        term_prc = removeEchoCharacters(term_prc)
        wordCollection = doc_prc.split()
        wordCollection.sort()
        lenOfCollection = len(wordCollection)
        index = bisect_left(wordCollection, term_prc)
        while(index < lenOfCollection and wordCollection[index] == term_prc):
            index += 1
            result += 1
        return result

    class __BestMatch25:
        def __init__(self):
            self.__wordTable = None
            self.__documents = None
            self.__avgdl = None

        def __buildDatabase(self):
            lenOfDocuments = len(self.documents)
            for index in range(lenOfDocuments):
                document = self.documents[index]
                document = removeDiacritics(document)
                document = removeEchoCharacters(document)
                self.__compileDocument(document, index)

        def __compileDocument(self, document, docNumber):
            wordCollection = set(document.split()) #remove duplicate word
            for word in wordCollection:
                if word not in self.__wordTable:
                    self.__wordTable[word] = []
                self.__wordTable[word].append(docNumber)

        @property
        def documents(self):
            if self.__documents == None:
                self.__documents = getLineFromFile(PRODUCT_PATHFILE)
            return self.__documents

        @property
        def database(self):
            if self.__wordTable == None:
                self.__wordTable = dict()
                self.__buildDatabase()
            return self.__wordTable
        
        @property
        def avgDocumentsLength(self):
            if self.__avgdl == None:
                self.__avgdl = float(sum([len(document) for document in self.documents])) / len(self.documents)
            return self.__avgdl

        def IDF(self, term):
            lenOfDocuments = len(self.documents)
            termFrequency = len(self.database[term]) if term in self.database else 0
            return log((lenOfDocuments - termFrequency + 0.5) / (termFrequency + 0.5) )

        def score(self, query, document):
            result = 0.0
            wordCollection = query.split()
            for word in wordCollection:
                freq = BestMatch25.TF(word, document)
                #IDF * (freq * (k1 + 1)) / (freq + k1 * (1 - b + b * (fieldLength / avgFieldLength)))
                score_word_i = self.IDF(word) * (freq * (K1 + 1)) / (freq + K1 * (1 - B + B * (len(document) / self.avgDocumentsLength)))
                if score_word_i > 0:
                    result += score_word_i
            return result
        def __getReleatedDocument(self, query):
            docNumbers = set()
            wordCollection = set(query.split())
            database = self.database
            for word in wordCollection:
                if word in database:
                    docNumbers.update(database[word])
            return docNumbers

        def rankings(self, query):
            result = []
            #because when frep = 0 then score is 0, so we should calculated for the related documents
            documents = self.documents
            indexReleatedDocuments = self.__getReleatedDocument(query)
            for index in indexReleatedDocuments:
                document = documents[index]
                score = self.score(query, document)
                if score > 0:
                    result.append((score, document))
            result.sort(key=lambda item: item[0], reverse = True)
            return result

        def search(self, query, numberDoc = NUMBER_OF_DOCUMENTS_RESULT):
            result = []
            strInput = removeDiacritics(query)
            strInput = removeEchoCharacters(strInput)
            rankings = self.rankings(strInput)
            result = [ranking[1] for ranking in rankings]
            result = result[:numberDoc]   #when numberDoc > len(rankings) then result equal rankings
            #result = rankings[:numberDoc]
            return result
