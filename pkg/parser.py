import configparser
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

    for val in dict:
        for i in dict[val]:
            if val == "key":
                currentsearch = bsdata.find(key=i)
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
