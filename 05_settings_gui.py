from tkinter import *
from tkinter import ttk
from functools import partial  # To prevent unwanted windows
import settings_list as s


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
                                   partial(self.close_help, partner))

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

        # List to store settings once they have been added to the GUI
        self.settings_input_list = []

        for item in s.settings.values():
            print(s.settings)
            print(item)
            print(item["name"])
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
            elif item["input_type"] == "checkbox":
                self.make_settings_input = Checkbutton(self.settings_input_frame,
                                                       onvalue = True,
                                                       offvalue = False,
                                                       bg=background)
                self.make_settings_input.grid(column=1, row=current_row)
            else:
                print("input_type for this setting is incorrect!")

            current_row += 1

        self.dismiss_button = Button(self.settings_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_help, partner))
        self.dismiss_button.grid(column=0, row=2, padx=10, pady=10)

        self.save_button = Button(self.settings_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_help, partner))
        self.save_button.grid(column=0, row=2, padx=10, pady=10)

        # List and loop to set background colour on
        # everything except the buttons.
        recolour_list = [self.settings_frame, self.settings_heading_label, self.settings_input_frame]

        for item in recolour_list:
            item.config(bg=background)

    def close_help(self, partner):
        partner.to_settings_button.config(state=NORMAL)
        self.settings_box.destroy()


if __name__ == "__main__":
    root = Tk()
    root.title("Currency Converter")
    Converter()
    root.mainloop()






