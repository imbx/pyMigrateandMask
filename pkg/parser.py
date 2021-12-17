import configparser
import json, os
from bs4 import BeautifulSoup

def ParseConfig(path, dict, db):
    config = configparser.ConfigParser()
    config.read(path)

    for val in dict:
        for i in dict[val]:
            if val == "tag":
                db.append(
                    {
                        i, 
                        config[i]
                    }
                )
                pass
            elif val == "":
                pass

    with open(path, 'w') as cfile:
        config.write(cfile)
    
    print("File at " + path + " was masked!")


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