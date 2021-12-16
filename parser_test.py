import json, os
from bs4 import BeautifulSoup

def ParseXML(path, dict, db):
    with open(path, 'r') as f:
        data = f.read()

    bsdata = BeautifulSoup(data, "xml")

    for val in dict:
        for i in dict[val]:
            if val == "name":
                currentsearch = bsdata.find(name=i["attr"])
                for result in currentsearch:
                    db.append(
                        {
                            i, 
                            result.value
                        }
                    )
                pass
            elif val == "":
                pass

fulldict = json.load(
    open('xmldb.json')
    )

keydb = []

print(fulldict)

for i in fulldict:
    print(i)
    for k in fulldict[i]:
        print("\t", k["attr"], " | target attr: ", k["target"],)

ParseXML("./template.xml", fulldict, keydb)

print(json.dumps(keydb))
