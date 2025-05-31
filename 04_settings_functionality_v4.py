import json
import settings_list as s

json_settings = {}

while True:
    try:
        with open("settings.json", "r") as json_file:
            json_settings = json.load(json_file)
        break
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        print("No JSON file detected. Creating JSON file...")
        with open("settings.json", "w") as json_file:
            json_file.write(json.dumps(s.default_dict, indent=4))
        continue

def settings_validator(settings_format, settings, default_settings, target_json):

    # This function is meant for checking that the settings.json file is valid,
    # to not cause issues later down the line.
    #
    # First accesses the specified dictionary.
    # key is the name of the setting. value is the value of the setting (which is the properties of that setting)

    for key, value in settings_format:

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
            # isn't a possible option listed in options.
            while True:
                print("Entering while true loop")
                try:
                    # Checks if the parameter for the corresponding setting in settings.json
                    # isn't a possible value listed in the settings_list constant.
                    # If it isn't, then we modify the settings dictionary.
                    if settings[key] not in value["options"]:
                        settings[key] = value["default_value"]
                        break
                    else:
                        print("Settings value is valid")
                        break

                # A KeyError will trigger if the setting cannot be found.
                # If this happens, the entire settings.json file will be rewritten to default.
                except KeyError:
                    print("JSON file invalid! Recreating file...")
                    settings_recreate(target_json, default_settings)
                    # Since the file is completely recreated here, we can stop checking if the settings are valid
                    # because we know they will be valid. So we return here instead of rerunning everything.
                    return

        # If value isn't a dictionary (indicating no double dictionary), don't try to access items within the value.
        else:
            print(f"This isn't a double dictionary.")

    # Once we are done, recreate the settings.json file with the new settings dictionary.
    settings_recreate(target_json, settings)

def settings_recreate(target_json, new_contents):
    with open(target_json, "w") as j:
        j.write(json.dumps(new_contents, indent=4))
    with open(target_json, "r") as j:
        print(f"{target_json} contents are now {json.load(j)}")


settings_validator(s.settings.items(), json_settings, s.default_dict, "settings.json")

print(json_settings)

# with open("settings.json", "w") as json_file:
#     json_file.write(json.dumps(json_settings, indent=4))




