
from fileSurfer import FileSurfer

def getLineFromFile(filePath):
    result = []
    with open(filePath, 'r') as fileHandle:
        fileSurfer = FileSurfer(fileHandle)
        fileEnd = not (fileSurfer.getLine())
        while(not fileEnd):
            result.append(fileSurfer.getLine().strip())
            fileEnd = not(fileSurfer.readNextLine())
    return result
