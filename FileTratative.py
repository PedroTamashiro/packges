import os
from time import sleep, time

DOWNLOADPATH = r"C:\Users\Cliente\Documents\EletroTrash"

def renameFile(oldName, newName):
    oldPath = DOWNLOADPATH + '\\' + oldName
    format = str.split(oldName, '.')
    format[1] = '.' + format[1]
    newPath = DOWNLOADPATH + '\\' + newName + format[1]
    os.rename(oldPath, newPath)
    return newPath
    
def waitDownload(NameFile, timeout=60):
    pathFile = os.path.join(DOWNLOADPATH, NameFile)
    
    inicialTime = time()
    
    while not os.path.exists(pathFile):
        if time() - inicialTime  > timeout:
            print("Tempo de espera esgotado. O arquivo não foi encontrado.")
            return False
        sleep(1)
        
    while pathFile.endswith('.crdownload') or pathFile.endswith('.part'):
        sleep(1)

    return True