from utilitiesFunction import getLineFromFile
from textProcessing import removeDiacritics, removeEchoCharacters


#TODO: move to config file
PRODUCT_PATHFILE = '../sanbox/product_names.txt'

#singleton class
class ReverseIndex:
    __instance = None
    def __init__(self):
        if ReverseIndex.__instance == None:
            ReverseIndex.__instance = ReverseIndex.__ReverseIndex()
    def search(self, text):
        return ReverseIndex.__instance.search(text)

    class __ReverseIndex:
        def __init__(self):
            self.__wordTable = None
            self.__documents = None

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

        def search(self, text):
            docNumbers = set()
            result = []
            strInput = removeDiacritics(text)
            strInput = removeEchoCharacters(strInput)
            wordCollection = set(strInput.split())
            database = self.database
            documents = self.documents
            for word in wordCollection:
                if word in database:
                    docNumbers.update(database[word])
            for docNumber in docNumbers:
                result.append(documents[docNumber])
            return result
