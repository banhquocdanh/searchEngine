
from fileSurfer import FileSurfer

def getLineFromFile(filePath):
    result = []
    with open(filePath, 'r') as fileHandle:
        fileSf = FileSurfer(fileHandle)
        fileEnd = not (fileSf.getLine())
        while(not fileEnd):
            result.append(fileSf.getLine())
            fileEnd = not(fileSf.readNextLine())
    return result
