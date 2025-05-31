"""Currency converter GUI."""

from tkinter import *
from tkinter import ttk
from functools import partial  # To prevent unwanted windows
import convert_round as cr
import settings_list as s
import settings_functions as sfunc
import api_functionality as api


class Converter:
    """Converter that also leads to other parts of program."""
    def __init__(self):
        """Main part of GUI."""

        self.base_frame = Frame(padx=10, pady=10)
        self.base_frame.grid()

        self.base_heading = Label(self.base_frame,
                                  text="Currency Converter",
                                  font=("Arial", "16", "bold")
                                  )
        self.base_heading.grid(row=0)

        self.convert_frame = Frame(self.base_frame)
        self.convert_frame.grid(row=1)

        self.error_label = Label(self.base_frame,
                                 text="Press the help button if unsure on how to use",
                                 fg="#004C99",
                                 font=("Arial", "14", "bold")
                                 )
        self.error_label.grid(row=2)

        # Conversion, help and history / export buttons
        self.button_frame = Frame(self.base_frame)
        self.button_frame.grid(row=3)

        # this is all stuff for convert_frame

        # input_frame and output_frame are within convert_frame and will have their own dropdowns etc
        self.input_frame = Frame(self.convert_frame)
        self.input_frame.grid(column=0, row=0, padx=10)

        self.output_frame = Frame(self.convert_frame)
        self.output_frame.grid(column=1, row=0, pady=10)

        # input_frame contents
        self.input_label = Label(self.input_frame,
                                 text="Currency to convert from",
                                 font=("Arial", "12")
                                 )
        self.input_label.grid(row=0)

        self.input_combo_box = ttk.Combobox(self.input_frame, state="readonly", values=list(api.currency_list.values()))
        self.input_combo_box.grid(row=1)

        self.input_entry = Entry(self.input_frame,
                                font=("Arial", "12"),
                                width=15
                                )

        self.input_entry.grid(row=2, padx=10, pady=10)

        # output_frame contents
        self.output_label = Label(self.output_frame,
                                  text="Currency to convert to",
                                  font=("Arial", "12")
                                  )
        self.output_label.grid(row=0)

        self.output_combo_box = ttk.Combobox(self.output_frame, state="readonly", values=list(api.currency_list.values()))
        self.output_combo_box.grid(row=1)

        self.output_entry = Entry(self.output_frame,
                                font=("Arial", "12"),
                                width=15, state="readonly"
                                )

        self.output_entry.grid(row=2, padx=10, pady=10)
        # convert_frame stuff ends here

        # button list (button text | bg colour | command | row | column)
        if sfunc.settings_read(s.json_name)["help_button_hide"]:
            button_details_list = [
                ["Convert", "#03AC13", self.input_checker, 0, 0],
                ["Swap", "#F96815", self.swap_inputs, 0, 1],
                ["Settings", "#0492C2", self.to_settings, 1, 0],
                # ["Help", "#A32CC4", self.to_help, 1, 1]
            ]
        else:
            button_details_list = [
                ["Convert", "#03AC13", self.input_checker, 0, 0],
                ["Swap", "#F96815", self.swap_inputs, 0, 1],
                ["Settings", "#0492C2", self.to_settings, 1, 0],
                ["Help", "#A32CC4", self.to_help, 1, 1]
            ]

        # List to hold buttons once they have been made
        self.button_ref_list = []

        for item in button_details_list:
            self.make_button = Button(self.button_frame,
                                      text=item[0], bg=item[1],
                                      fg="#FFFFFF", font=("Arial", "12", "bold"),
                                      width=12, command=item[2])
            self.make_button.grid(row=item[3], column=item[4], padx=5, pady=5)

            self.button_ref_list.append(self.make_button)

        if sfunc.settings_read(s.json_name)["style"] == "Dark":
            # List and loop for dark mode
            recolour_list = [self.base_frame, self.base_heading, self.convert_frame,
                             self.input_label, self.output_label, self.input_frame, self.output_frame,
                             self.error_label, self.button_frame]
            recolour_list_brighten = [self.base_heading, self.input_label, self.output_label]

            for item in recolour_list:
                item.config(bg="#222222")

            for item in recolour_list_brighten:
                item.config(fg="#FFFFFF")

    def convert(self, value):
        """Uses API to convert currency into other currency."""
        input_currency_ico = api.currency_name_to_ico(self.input_combo_box.get())
        output_currency_ico = api.currency_name_to_ico(self.output_combo_box.get())

        exchange_rate = api.exchange_rate_get(input_currency_ico, output_currency_ico)
        answer = cr.convert_round_4dp(value, exchange_rate)

        answer_statement = f"{value} {input_currency_ico} is {answer} in {output_currency_ico}"

        self.error_label.config(text=answer_statement, fg="#004C99", font=("Arial", "12", "bold"))
        self.input_entry.config(bg="#FFFFFF")

        self.output_entry.config(state="normal")
        self.output_entry.delete(0, END)
        self.output_entry.insert(0, answer)
        self.output_entry.config(state="readonly")


    def input_checker(self):
        """Checks inputs and makes sure they are valid."""
        # Before we do anything, check that the currency options are not the same.
        # If they are the same, trying to pass them to the API will result in an error and will mess everything up.
        if self.input_combo_box.get() == self.output_combo_box.get():
            error = "You cannot convert to the same currency!"
            has_errors = True

        # If they're not the same, we continue.
        else:

            try:
                value = int(self.input_entry.get())
                if value > 0:
                    # Add API stuff here later
                    self.convert(value)
                    return
                else:
                    error = "Input must be a number greater than 0!"
                    has_errors = True

            except ValueError:
                error = "Input must be a number greater than 0!"
                has_errors = True

        if has_errors:
            self.error_label.config(text=error, fg="#960019", font=("Arial", "10", "bold"))
            self.input_entry.config(bg="#F4CCCC")
            self.input_entry.delete(0, END)

    def swap_inputs(self):
        """Swaps current inputs to other side and vice versa."""
        # getting all the values from all the combo boxes and dropdowns so we can swap them later
        input_dropdown = self.input_combo_box.get()
        output_dropdown = self.output_combo_box.get()
        input_entry = self.input_entry.get()
        output_entry = self.output_entry.get()

        self.input_combo_box.set(output_dropdown)
        self.output_combo_box.set(input_dropdown)

        # the reason why we set the state from normal to readonly is because we can't modify the entry
        # while it is readonly, for some reason. we modify it back to readonly so that the user
        # cannot type in the answer area, as this would make no sense.
        self.output_entry.config(state="normal")
        self.input_entry.delete(0, END)
        self.input_entry.insert(0, output_entry)
        self.output_entry.config(state="readonly")

        self.output_entry.config(state="normal")
        self.output_entry.delete(0, END)
        self.output_entry.insert(0, input_entry)
        self.output_entry.config(state="readonly")

    def to_help(self):
        """
        Opens help dialogue box and disables help button
        (so that users can't create multiple help boxes).
        """
        DisplayHelp(self)

    def to_settings(self):
        """
        Opens settings dialogue box and disables settings button
        (so that users can't create multiple settings boxes).
        """
        DisplaySettings(self)

class DisplayHelp:
    """Help GUI."""
    def __init__(self, partner):
        """Main part of GUI."""
        # setup dialogue box and background colour
        background = "#ffe6cc"
        self.help_box = Toplevel()

        # disable help button
        partner.button_ref_list[3].config(state=DISABLED)

        self.help_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_help, partner))

        self.help_frame = Frame(self.help_box, width=300,
                                height=200)
        self.help_frame.grid()

        self.help_heading_label = Label(self.help_frame,
                                        text="Help / Info",
                                        font=("Arial", "14", "bold"))
        self.help_heading_label.grid(row=0)

        help_text = "To use the currency converter, set the desired currencies to convert to and from " \
                    "via the dropdowns.\n\n" \
                    "Then type the amount of currency that you want to convert on the left box.\n\n" \
                    "Press the convert button and the equivalent amount in the other currency " \
                    "will appear in the other box.\n\n" \
                    "You can also press the swap button to swap the currencies, " \
                    "and the settings button to change settings.\n\n" \
                    "You can press the help button to access this again."

        self.help_text_label = Label(self.help_frame,
                                     text=help_text, wraplength=350,
                                     justify="left")
        self.help_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.help_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_help, partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

        # List and loop to set background colour on
        # everything except the buttons.
        recolour_list = [self.help_frame, self.help_heading_label, self.help_text_label]

        for item in recolour_list:
            item.config(bg=background)

    def close_help(self, partner):
        """Closes GUI properly and allows for reopening later."""
        partner.button_ref_list[3].config(state=NORMAL)
        self.help_box.destroy()

class DisplaySettings:
    """Settings GUI."""
    def __init__(self, partner):
        """Main part of GUI."""
        # setup dialogue box and background colour
        background = "#ffe6cc"

        # this is for later, to create dropdowns and checkboxes for settings
        current_row = 0

        self.settings_box = Toplevel()

        # disable button
        partner.button_ref_list[2].config(state=DISABLED)

        self.settings_box.protocol('WM_DELETE_WINDOW',
                                   partial(self.close_settings, partner))

        self.settings_frame = Frame(self.settings_box, width=300,
                                    height=200)
        self.settings_frame.grid()

        self.settings_heading_label = Label(self.settings_frame,
                                            text="Settings",
                                            font=("Arial", "14", "bold"))
        self.settings_heading_label.grid(row=0)

        self.settings_input_frame = Frame(self.settings_frame, width=300,
                                          height=200)
        self.settings_input_frame.grid(row=1, padx=15)

        # Lists to store settings once they have been added to the GUI
        self.settings_ref_list = []
        # Second list for checkbutton variables
        self.checkbutton_ref_list = []

        for item in s.settings.values():

            # Accesses the settings.json file and gets the value of the current setting.
            # This is used for determining what dropdowns and checkboxes will be set to after creation.
            current_value = list(sfunc.settings_read(s.json_name).values())[current_row]

            self.make_settings_label = Label(self.settings_input_frame,
                                             text=item["name"],
                                             justify="left",
                                             bg=background)
            self.make_settings_label.grid(column=0, row=current_row)

            if item["input_type"] == "dropdown":
                self.make_settings_input = ttk.Combobox(self.settings_input_frame,
                                                        values=item["options"],
                                                        justify="left",
                                                        state="readonly",
                                                        width=15)
                self.make_settings_input.grid(column=1, row=current_row)

                self.settings_ref_list.append(self.make_settings_input)

                # Puts the current value into dropdown
                self.make_settings_input.set(current_value)


            elif item["input_type"] == "checkbox":
                state = BooleanVar()
                self.make_settings_input = Checkbutton(self.settings_input_frame,
                                                       variable = state,
                                                       onvalue="True",
                                                       offvalue="False",
                                                       bg=background)
                self.make_settings_input.grid(column=1, row=current_row)

                self.settings_ref_list.append(self.make_settings_input)
                self.checkbutton_ref_list.append(state)

                # Set the value when we create it
                if current_value:
                    self.make_settings_input.select()
                elif not current_value:
                    self.make_settings_input.deselect()
                else:
                    print("Value of checkbox incorrect.")

            else:
                print("input_type for this setting is incorrect!")

            current_row += 1
        self.button_frame = Frame(self.settings_frame)
        self.button_frame.grid(row=2)

        self.dismiss_button = Button(self.button_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_settings, partner))
        self.dismiss_button.grid(column=0, row=1, padx=10, pady=10, sticky="nsew")

        self.save_button = Button(self.button_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Save", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.save_settings,self.settings_ref_list,
                                                     self.checkbutton_ref_list))
        self.save_button.grid(column=1, row=1, padx=10, pady=10, sticky="nsew")

        # List and loop to set background colour on
        # everything except the buttons.
        recolour_list = [self.settings_frame, self.settings_heading_label, self.settings_input_frame, self.button_frame]

        for item in recolour_list:
            item.config(bg=background)

    @staticmethod
    def save_settings(settings_list, checkbutton_list):
        """Saves every setting input to file."""
        # this variable goes up every time the loop is finished, to get checkbox values properly
        current_setting = 0


        checkbutton_number = 0
        for item in settings_list:

            if isinstance(item, ttk.Combobox):
                prompt_value = item.get()
            elif isinstance(item, Checkbutton):
                prompt_value = checkbutton_list[checkbutton_number].get()
                checkbutton_number += 1
            else:
                print("Setting is neither combobox nor checkbutton!")
                prompt_value = None

            sfunc.settings_modify(s.json_name,
                                  list(sfunc.settings_read(s.json_name).keys())[current_setting],
                                  prompt_value)
            current_setting += 1


    def close_settings(self, partner):
        """Closes settings GUI properly and allows for reopening later."""
        partner.button_ref_list[2].config(state=NORMAL)
        self.settings_box.destroy()


# main routine

# this makes sure that all the settings are correct and should always be before making the gui
# otherwise, in the main code, problems will arise when trying to use settings such as style if the settings are wrong
sfunc.settings_validator(s.settings.items(), (sfunc.settings_read(s.json_name)), s.default_dict, s.json_name)
root = Tk()
root.title("Currency Converter")
Converter()
root.mainloop()
