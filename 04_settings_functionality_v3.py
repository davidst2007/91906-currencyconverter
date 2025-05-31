import json
import settings_list as s

test_dict = {"style": 1,
             "help_button_hide": "False"}

json_settings = {}

while True:
    try:
        with open("settings.json", "r") as json_file:
            json_settings = json.load(json_file)
        break
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        print("No JSON file detected. Creating JSON file...")
        with open("settings.json", "w") as json_file:
            json_file.write(json.dumps(test_dict, indent=4))
        continue

# First accesses the specified dictionary.
# key is the name of the setting. value is the value of the setting (which is the properties of that setting)
#
# The way how settings are organised in settings_list is that each setting is listed,
# and the value of each setting is a dictionary containing its parameters.

for key, value in s.settings.items():

    # Prints value.
    print(f"Setting: {key}")

    # Checks if value is a dictionary. Otherwise, do nothing.
    # Without this, the next loop can try to access a dictionary that doesn't exist and cause an error.
    if isinstance(value, dict):
        print("Value matches dict")

        # There is a "while True" block here in order to prevent any KeyError.
        # A KeyError will trigger if the setting cannot be found.
        # If this happens, the entire settings.json file will be rewritten to default.

        # Then, it checks if the parameter for the corresponding setting in settings.json
        # isn't a possible option listed in options. If it isn't,
        # then change the value to default.
        while True:
            print("Entering while true loop")
            try:
                if json_settings[key] not in value["options"]:
                    print(json_settings[key])
                    print(value["options"])
                    print(value["default_value"])
                    json_settings[key] = value["default_value"]
                    print(value["default_value"])
                    print(json_settings)
                    break
                else:
                    print("Settings value is valid")
                    break

            except KeyError:
                print("JSON file invalid! Recreating file...")
                with open("settings.json", "w") as json_file:
                    json_file.write(json.dumps(test_dict, indent=4))
                print(test_dict)
                with open("settings.json", "r") as json_file:
                    print(json.load(json_file))
                break

    # If value isn't a dictionary (indicating no double dictionary), don't try to access items within the value.
    else:
        print(f"This isn't a double dictionary.")


print(json_settings)

with open("settings.json", "w") as json_file:
    json_file.write(json.dumps(json_settings, indent=4))




