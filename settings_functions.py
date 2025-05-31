import json
import settings_list as s

# This file is intended to be imported into other files.

def settings_read(target_json):
    try:
        with open(target_json, "r") as j:
            return json.load(j)
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        print("No JSON file detected.")
        return

def settings_validator(settings_format, settings, default_settings, target_json):

    # This function is meant for checking that the settings.json file is valid,
    # to not cause issues later down the line.

    try:

    # First accesses the specified dictionary. Should be in .items() form.
    # key is the name of the setting. value is the value of the setting (which is the properties of that setting)

        for key, value in settings_format:

            # Prints value.
            print(f"Setting: {key}")

            # Checks if value is a dictionary. Otherwise, do nothing.
            # Without this, the next loop can try to access a dictionary that doesn't exist and cause an error.
            if isinstance(value, dict):
                print("Value matches dict")

                # Checks if the parameter for the corresponding setting in settings.json
                # isn't a possible value listed in the settings_list constant.
                # If it isn't, then we modify the settings dictionary.
                if settings[key] not in value["options"]:
                    print(f"Value incorrect for {key}, changing to default...")
                    settings[key] = value["default_value"]
                    continue
                else:
                    print("Settings value is valid")
                    continue

            # If value isn't a dictionary (indicating no double dictionary),
            # don't try to access items within the value.
            else:
                print("This isn't a double dictionary.")

        # Once we are done, recreate the settings.json file with the new settings dictionary.
        settings_recreate(target_json, settings)


    # A KeyError will trigger if the setting cannot be found.
    # A TypeError will trigger if the file is missing.
    # If either of these happen, the entire settings.json file will be rewritten to default.
    except (KeyError, TypeError):
        print("JSON file invalid! Recreating file...")
        settings_recreate(target_json, default_settings)
        # Since the file is completely recreated here, we can stop checking if the settings are valid
        # because we know they will be valid. So we return here instead of rerunning everything.
        return


def settings_recreate(target_json, new_contents):
    with open(target_json, "w") as j:
        j.write(json.dumps(new_contents, indent=4))
    with open(target_json, "r") as j:
        print(f"{target_json} contents are now {json.load(j)}")

def settings_modify(target_json, target_setting, new_value):
    json_dict = settings_read(target_json)

    json_dict[target_setting] = new_value

    # This code can set settings to things that should not be allowed for that setting.
    # However, this is OK because in the real program, this will be used with dropdowns and checkboxes
    # and therefore there will be no way to input something incorrect.
    with open(target_json, "w") as j:
        j.write(json.dumps(json_dict, indent=4))
