import configparser
import json, os
from bs4 import BeautifulSoup, Comment

def ParseConfig(path, dict, db):
    config = configparser.ConfigParser()
    config.read(path)

    for val in dict:
        for i in dict[val]:
            if val == "tag":
                db.append(
                    {
                        path,
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


def OLD_ParseXML(path, dict, db):
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
                        path,
                        i["attr-value"], 
                        result["default-value"]
                    ]
                )
                result["default-value"] = "XXX"
    f = open(path, "w")
    f.write(bsdata.prettify())
    print("MASKED!")


def ParseXML(path, dict, db):
    with open(path, 'r') as f:
        data = f.read()
        bsdata = BeautifulSoup(data, "xml")

    if not bsdata:
        return
    for val in dict:
        currentsearch = bsdata.find_all(attrs = { val["search-attr"] : val["search-val"] })
        for result in currentsearch:
            if val["target-attr"] != "":
                db.append(
                    [
                        path,
                        val["search-val"], 
                        result[val["target-attr"]]
                    ]
                )
                result[val["target-attr"]] = "XXX"
            else:
                for alter in result.select(val["target-tag"]):
                    db.append(
                        [
                            path,
                            val["search-val"], 
                            alter.text
                        ]
                        )
                    alter.clear()
                    alter.insert(0, "XXX")
    f = open(path, "w")
    for element in bsdata(text=lambda text: isinstance(text, Comment)):
        element.extract()
    f.write(bsdata.prettify())
    print("MASKED! {}".format(path))