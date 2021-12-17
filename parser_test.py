import json, os
from bs4 import BeautifulSoup


def ParseXML(path, dict, db):
    with open(path, 'r') as f:
        data = f.read()
        bsdata = BeautifulSoup(data, "xml")

    if not bsdata:
        return
    for val in dict:
        for i in dict[val]:
            currentsearch = bsdata.find_all(attrs = { val : i["attr-value"] })
            for result in currentsearch:
                db.append(
                    [
                        i["attr-value"], 
                        result["default-value"]
                    ]
                )
                result["default-value"] = "XXX"
    f = open(path, "w")
    f.write(bsdata.prettify())
    print("MASKED!")


fulldict = json.load(
    open('xmldb.json')
    )

keydb = []

#print(fulldict)

for i in fulldict:
    print(i)
    for k in fulldict[i]:
        print("\t", k["attr-value"], " | target attr: ", k["target"],)

ParseXML("./template.xml", fulldict, keydb)
print("RESULT")
print(keydb)
