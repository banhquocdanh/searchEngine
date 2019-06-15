from mmap import mmap, ACCESS_READ
from os import linesep, remove, SEEK_CUR
import re

class FilePosition(object):
    __lineIndex = None  #position start line
    __line = None
    __position = None   #position end of line

    def __init__(self, lineIndex, line, position):
        '''
        Constructor
        '''
        self.__lineIndex = lineIndex
        self.__line = line
        self.__position = position

    @property
    def position(self):
        return self.__position

    @property
    def line(self):
        return self.__line

    @property
    def lineIndex(self):
        return self.__lineIndex

class FileSurfer(object):
    __fileHandle = None
    __position = None
    __positionStack = None

    def __init__(self, fileHandle):
        '''
        Constructor
        '''
        #self.__fileHandle = fileHandle
        self.__fileHandle = mmap(fileHandle.fileno(), 0, access=ACCESS_READ)
        self.__fileHandle.seek(0)
        lineIndex = self.__fileHandle.tell()
        line = self.readline()
        self.__position = FilePosition(lineIndex, line, self.__fileHandle.tell())
        self.__positionStack = []

    def readNextLine(self):
        lineIndex = self.__fileHandle.tell()
        line = self.readline()
        self.__position = FilePosition(lineIndex, line, self.__fileHandle.tell())
        return self.__position.line

    def readPreviousLine(self):
        lineIndex = self.__fileHandle.tell()
        self.__fileHandle.seek(self.__position.lineIndex-2)
        while ((self.__fileHandle.tell() > 0) and ( self.__fileHandle.read(1) != b'\n')):
            self.__fileHandle.seek(-2, SEEK_CUR)
        lineIndex = self.__fileHandle.tell()
        line = self.readline()
        self.__position = FilePosition(lineIndex, line, self.__fileHandle.tell())
        return self.__position.line, lineIndex

    def goToEmptyLine(self, startFromNextLine = True):
        fileEnd = False
        if startFromNextLine:
            fileEnd = not (self.readNextLine())
        while(( linesep != self.getLine()) and (not fileEnd)):
            fileEnd = not (self.readNextLine())
        return self.getPosition() if not fileEnd else None

    def goToLineThatBeginsWith(self, pattern, startFromNextLine = True):
        fileEnd = False
        if startFromNextLine:
            fileEnd = not (self.readNextLine())
        while(( pattern != self.getLine()[:len(pattern)]) and (not fileEnd)):
            fileEnd = not (self.readNextLine())
        return self.getPosition() if not fileEnd else None

    def goToMatchingLine(self, pattern, startFromNextLine = True, indexEnd = -1):
        fileEnd = False
        if startFromNextLine:
            fileEnd = not (self.readNextLine())
        while(not fileEnd and not pattern.match(self.getLine()) and (indexEnd == -1 or self.getPosition() <= indexEnd)):
            fileEnd = not (self.readNextLine())
        return self.getPosition() if not fileEnd else None

    def backToMatchingLine(self, pattern, startFromPreviousLine = True):
        line = self.getLine()
        lineIndex = self.getPosition()
        if startFromPreviousLine:
            line, lineIndex = self.readPreviousLine()
        while(( not pattern.match(line)) and (lineIndex > 0)):
            line, lineIndex = self.readPreviousLine()
        return self.getPosition() if pattern.match(line) else None

    def getPosition(self):
        return self.__position.lineIndex

    def getLine(self):
        return self.__position.line

    def close(self):
        self.__fileHandle.close()

    def tell(self):
        return self.__fileHandle.tell()

    def seek(self,position):
        self.__fileHandle.seek(position)
        self.readNextLine()

    def seekNoUpdate(self,position):
        try:
            self.__fileHandle.seek(position)
        except ValueError:
            print("ValueError at position: " + str(position))
            raise

    def read(self,count = -1):
        return self.__fileHandle.read(count).decode("utf-8")

    def readline(self):
        return self.__fileHandle.readline().decode("utf-8")

    def getFileHandle(self):
        return self.__fileHandle

    def pushPosition(self):
        self.__positionStack.append(self.__position)

    def popPosition(self):
        self.__position = self.__positionStack.pop()
        self.__fileHandle.seek(self.__position.position)

    def __enter__(self):
        return self.__fileHandle

    def __exit__(self, exctype, value, traceback):
        self.close()

    @staticmethod
    def getGroupFromLine(line, pattern, groupNo=1):
        result = None
        if line:
            searchResult = pattern.search(line)
            if searchResult:
                if groupNo <= pattern.groups:
                    result = searchResult.group(groupNo)
                else:
                    result = searchResult.group(0)
        return result