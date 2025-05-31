import json

default_settings = {
    "a": 1,
    "b": 2,
    "c": 3
}

with open("settings.json", "w") as json_file:
    json_file.write(json.dumps(default_settings, indent=4))

with open("settings.json", "r") as json_file:
    json_object = json.load(json_file)

print(json_object)
