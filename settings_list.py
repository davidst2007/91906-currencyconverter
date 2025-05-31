"""Constant file used as a dictionary for setting parameters."""

# This is a constant. It is a list of all settings, what they do, and what type they are.

# "input_type" refers to the type of input that it will use.
# "checkbox" indicates that the setting will be a simple checkbox.
# "dropdown" indicates that the setting will be a dropdown.

# "options" is a list of all options that the setting should have,
# to prevent the user from inputting something that should not be possible.
# This setting should always be ["True", "False"] on checkboxes.

# "name" is the name that will be visible in the settings GUI for the user.

settings = {

    "style": {
        # The "style" setting dictates how the program will look.
        "input_type": "dropdown",
        "options": ["Default", "Dark"],
        "name": "Style (requires restart)",
        "default_value": "Default"

    },

    "help_button_hide": {
        # The "help_button_hide" setting will hide the help box if checked.
        "input_type": "checkbox",
        "options": [True, False],
        "name": "Hide Help Button (requires restart)",
        "default_value": False
    }

}

# default_dict is used to recreate the settings.json file if it is invalid or missing.
default_dict = {
    "style": 1,
    "help_button_hide": "False"
}

# this is just for minimising having to type out the same thing constantly and should be used as
# a replacement for typing "settings.json" in the main routine. would save a lot of time if I
# ever chose to change what the .json is called, if I would ever want to do that for some reason.
json_name = "settings.json"