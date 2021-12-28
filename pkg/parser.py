from bs4 import BeautifulSoup, Comment

def ParseXML(path, dict, db):
    haswritten = False
    with open(path, 'r') as f:
        data = f.read()
        bsdata = BeautifulSoup(data, "xml")

    if not bsdata:
        print("No file to read at {}".format(path))
        return False

    for val in dict:
        currentsearch = bsdata.find_all(attrs = { val["search-attr"] : val["search-val"] })
        
        if currentsearch == []:
            continue

        print(currentsearch)
        for result in currentsearch:
            if not haswritten : haswritten = True
            print("Masking {}".format(result))
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
    if haswritten : 
        f = open(path, "w")
        for element in bsdata(text=lambda text: isinstance(text, Comment)):
            element.extract()
        f.write(bsdata.prettify())
        print("MASKED! {}".format(path))
    else :
        print("Nothing to mask! {}".format(path))

    f.close()
    return haswritten