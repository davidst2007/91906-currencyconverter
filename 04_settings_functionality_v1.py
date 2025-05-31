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
    except json.decoder.JSONDecodeError:
        print("Oh ok")
        # with open("settings.json", "w") as json_file:
        #     json_file.write(json.dumps(test_dict, indent=4))
        break




# First accesses the specified dictionary.
# key is the name of the setting. value is the value of the setting (which is the properties of that setting)
#
# The way how settings are organised in settings_list is that each setting is listed,
# and the value of each setting is a dictionary containing its parameters.

for key1, value1 in s.settings.items():

    # Prints value.
    print(f"Setting: {key1}")

    # Checks if value is a dictionary. Otherwise, do nothing.
    # Without this, the next loop can try to access a dictionary that doesn't exist and cause an error.
    if isinstance(value1, dict):

        # Accesses the dictionary (the parameters of a setting).
        # key2 is the name of the parameter
        for key2, value2 in value1.items():
            print(f"  {key2}: {value2}")

            # This bit of code first checks that the parameter is options.
            if key2 == "options":

                # There is a "while True" block here in order to prevent any KeyError.
                # A KeyError will trigger if the setting cannot be found.
                # If this happens, the entire settings.json file will be rewritten to default.

                # Then, it checks if the parameter for the corresponding setting in settings.json
                # isn't a possible option listed in options. If it isn't,
                # then change the value to default.
                while True:
                    try:
                        if json_settings[key1] not in value2:
                            json_settings[key1] = value1["default_value"]
                            print(value1["default_value"])
                            print("s")



                    except KeyError:
                        print("JSON file invalid! Recreating file...")
                        with open("settings.json", "w") as json_file:
                            json_file.write(json.dumps(test_dict, indent=4))
                        break






    # If value isn't a dictionary (indicating no double dictionary), don't try to access items within the value.
    else:
        print(f"This isn't a double dictionary.")


print(json_settings)





