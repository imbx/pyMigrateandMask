import os
import json
from datetime import datetime
from pkg.main_folder import MainFolder, MainFolderEncoder
from pkg import * 

currentTime = datetime.now().strftime("%d%m%Y%H%M%S")

projects_path = "./projects/"
maskedconfig_path = "./config/masked_" + currentTime + "/"
config_path = "./config/config_" + currentTime + "/"

valid_extensions = ['.config', '.xml', '.appsettings']

print("\n----------------")
print("Creating folders")
print("----------------\n")

checkers.cFolder(projects_path)
checkers.cFolder(maskedconfig_path)
checkers.cFolder(config_path)

folderDict = {}

print("\n----------------")
print("Reading paths...")
print("----------------\n")

for p in os.listdir(projects_path):
    if not checkers.cFile(p):
        folderDict[p] = MainFolder(p)

print("\n-----------------------")
print("Extracting config files")
print("-----------------------\n")

for key in folderDict:
    fa = str (folderDict[key])
    path = os.path.join(projects_path , str(fa))
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            if checkers.cExtensions(name, valid_extensions) and checkers.cFile(os.path.join(root, name)):
                new_path = root.replace(projects_path, '')
                fname, extension = os.path.splitext(name)
                folderDict[key].paths.append(
                    {
                        "name" : fname,
                        "ext" : extension,
                        "path" : new_path,
                        "masked" : False
                    }
                )
    for val in folderDict[key].paths:
        utils.CopyFile(
            os.path.join(
                projects_path,
                val["path"]
            ) + "/"+ val["name"] +
                val["ext"]
            ,
            os.path.join(
                maskedconfig_path,
                val["path"]
            )
        )
        utils.CopyAndRename(
            os.path.join(
                projects_path,
                val["path"]
            ) + "/",
            os.path.join(
                config_path,
                val["path"]
            ),
            val["name"],
            ".PROD",
            val["ext"]
        )
        utils.CopyAndRename(
            os.path.join(
                projects_path,
                val["path"]
            ) + "/",
            os.path.join(
                config_path,
                val["path"]
            ),
            val["name"],
            ".PREPROD",
            val["ext"]
        )
    
with open(maskedconfig_path + currentTime + ".json", "w") as outfile:
    json.dump(folderDict, fp=outfile, cls=MainFolderEncoder)

print("\n--------------------------------")
print("Config files extracted correctly")
print("--------------------------------\n")

checkers.cFolder("./output/")

keydb = []
fulldict = json.load(
    open('xmldb.json')
    )


for key in folderDict:
    for val in folderDict[key].paths:
        filepath = os.path.join(
                maskedconfig_path,
                val["path"]
            ) + "/" + val["name"] + val["ext"]
        parser.ParseXML(filepath, fulldict, keydb)

#parser.ParseXML("./template.xml", fulldict, keydb)

tocsv.SaveCSV(str(currentTime + ".csv"), keydb)

#checkers.cFolder(os.path.join(maskedconfig_path, new_path))
#checkers.cFolder(os.path.join(config_path, new_path))

#if not checkers.cFile(os.path.join(maskedconfig_path, new_path + name)): 
#    shutil.copy(os.path.join(root, name), os.path.join(maskedconfig_path, new_path))
#print("config file: " + name)





