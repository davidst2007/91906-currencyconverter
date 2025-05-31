from tkinter import *
from tkinter import ttk
from functools import partial  # To prevent unwanted windows
import settings_list as s
import settings_functions as sfunc


class Converter:
    def __init__(self):

        self.base_frame = Frame(padx=10, pady=10)
        self.base_frame.grid()

        self.to_settings_button = Button(self.base_frame,
                                         text="Settings",
                                         bg="#0492C2",
                                         # fg determines the text colour
                                         fg="#FFFFFF",
                                         font=("Arial", "14", "bold"), width=12,
                                         command=self.to_help)
        self.to_settings_button.grid(row=1, padx=5, pady=5)

    def to_help(self):
        """
        Opens help dialogue box and disables help button
        (so that users can't create multiple help boxes).
        """
        DisplaySettings(self)


class DisplaySettings:
    def __init__(self, partner):
        # setup dialogue box and background colour
        background = "#ffe6cc"

        # this is for later, to create dropdowns and checkboxes for settings
        current_row = 0

        self.settings_box = Toplevel()

        # disable button
        partner.to_settings_button.config(state=DISABLED)

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
        partner.to_settings_button.config(state=NORMAL)
        self.settings_box.destroy()

# main routine

# this makes sure that all the settings are correct and should always be before making the gui
# otherwise, in the main code, problems will arise when trying to use settings such as style if the settings are wrong
sfunc.settings_validator(s.settings.items(), (sfunc.settings_read(s.json_name)), s.default_dict, s.json_name)

if __name__ == "__main__":
    root = Tk()
    root.title("Currency Converter")
    Converter()
    root.mainloop()






