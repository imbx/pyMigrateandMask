import json

config = {}

try:
    with open("config.json") as json_data:
        config = json.load(json_data)
except:
    print("ERR")

o_config = config["output"]
p_dict = config["dict"]
