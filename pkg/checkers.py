import os

def cFile(name):
    return os.path.isfile(name)

def cFolder(path):
    if os.path.exists(path):
        return
    os.makedirs(path)

def cExtensions(name, vext):
    for ext in vext:
        if name.endswith(ext):
            return True
    return False

def cExclusions(path, excl):
    for ex in excl:
        if ex in path:
            return  True
    return False