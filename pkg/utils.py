import shutil
import time
import os
from pkg import checkers

def CopyFile(filepath, destination):
    checkers.cFolder(destination)
    if not checkers.cFile(destination): 
        shutil.copy(filepath, destination)
    print("File copied from " + filepath + " to " + destination)

def CopyAndRename(filepath, destination, name, toadd, ext):
    checkers.cFolder(destination)
    if not checkers.cFile(destination): 
        shutil.copy(filepath + name + ext, destination)

        if not os.path.exists(os.path.join(destination, name + ext)):
            time.sleep(5)
        try:
            os.rename(os.path.join(destination, name + ext), os.path.join(destination, name + toadd + ext))
        except:
            print("Something went wrong with {}".format(os.path.join(destination, name + toadd + ext)))
    print("File copied from " + filepath + name + ext + " to " + os.path.join(destination, name + toadd + ext))

