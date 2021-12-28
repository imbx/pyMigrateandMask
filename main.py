import os, json, time
from datetime import datetime
from pkg import * 
from pkg.main_folder import MainFolder, MainFolderEncoder
from config import o_config as cfg
from config import p_dict as parseDict

currentTime = datetime.now().strftime("%d%m%Y%H%M%S")


print("\n----------------")
print("Creating folders")
print("----------------\n")

proj_path = cfg["projects_path"]
out_path = cfg["output_path"]
mask_path = cfg["masked_output"]

if cfg["write_date"]:
    out_path += currentTime + "/"
    mask_path += currentTime + "/"

checkers.cFolder(proj_path)
checkers.cFolder(out_path)

if cfg["maskdata"]:
    checkers.cFolder(mask_path)

folderDict = {}

print("\n----------------")
print("Reading paths...")
print("----------------\n")

for p in os.listdir(proj_path):
    if not checkers.cFile(p):
        folderDict[p] = MainFolder(p)

print("\n-----------------------")
print("Extracting config files")
print("-----------------------\n")


for key in folderDict:
    fa = str (folderDict[key])
    path = os.path.join(proj_path , str(fa))
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            if checkers.cExtensions(name, cfg["valid_ext"]) and not checkers.cExclusions(root, cfg["folder_exclusion"]) and checkers.cFile(os.path.join(root, name)):
                new_path = root.replace(proj_path, '')
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
        if cfg["maskdata"] or cfg["generatemaskfiles"]:
            utils.CopyFile(
                os.path.join(
                    proj_path,
                    val["path"]
                ) + "/"+ val["name"] +
                    val["ext"]
                ,
                os.path.join(
                    mask_path,
                    val["path"]
                )
            )
        utils.CopyAndRename(
            os.path.join(
                proj_path,
                val["path"]
            ) + "/",
            os.path.join(
                out_path,
                val["path"]
            ),
            val["name"],
            ".PROD",
            val["ext"]
        )
        utils.CopyAndRename(
            os.path.join(
                proj_path,
                val["path"]
            ) + "/",
            os.path.join(
                out_path,
                val["path"]
            ),
            val["name"],
            ".PREPROD",
            val["ext"]
        )
    
with open(out_path + currentTime + ".json", "w") as outfile:
    json.dump(folderDict, fp=outfile, cls=MainFolderEncoder)

print("\n--------------------------------")
print("Config files extracted correctly")
print("--------------------------------\n")

if cfg["maskdata"]:
    checkers.cFolder("./output/")

    keydb = []

    print("\n-------")
    print("MASKING")
    print("-------\n")

    for key in folderDict:
        for val in folderDict[key].paths:
            filepath = os.path.join(
                    mask_path,
                    val["path"]
                ) + "/" + val["name"] + val["ext"]
            if val["ext"] == ".xml" or val["ext"] == ".config":
                try:
                    val["masked"] = parser.ParseXML(filepath, parseDict["xml"], keydb)
                except:
                    print("Error trying to parse {}".format(filepath))
                finally: 
                    continue

    tocsv.SaveCSV(str(currentTime + ".csv"), keydb)

print("\n--------")
print("FINISHED")
print("--------\n")

input("Press Enter to exit")





