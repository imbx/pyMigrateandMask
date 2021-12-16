import json
from json import JSONEncoder

class MainFolder:
    def __init__(self, root):
        self.root = root
        self.paths = []

    def __str__(self):
        return self.root

class MainFolderEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__


    