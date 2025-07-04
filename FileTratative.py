import os
from time import sleep, time

DOWNLOADPATH = r"C:\Users\Cliente\Documents\EletroTrash"

def renameFile(oldName, newName, downloadPath = DOWNLOADPATH):
    oldPath = downloadPath + '\\' + oldName
    format = str.split(oldName, '.')
    format[1] = '.' + format[1]
    newPath = downloadPath + '\\' + newName + format[1]
    os.rename(oldPath, newPath)
    return newPath
    
def waitDownload(NameFile, downloadPath = DOWNLOADPATH, timeout=60):
    pathFile = os.path.join(downloadPath, NameFile)
    
    inicialTime = time()
    
    while not os.path.exists(pathFile):
        if time() - inicialTime  > timeout:
            print("Tempo de espera esgotado. O arquivo não foi encontrado.")
            return False
        sleep(1)
        
    while pathFile.endswith('.crdownload') or pathFile.endswith('.part'):
        sleep(1)

    return True