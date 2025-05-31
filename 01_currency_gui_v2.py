from tkinter import *
from tkinter import ttk
from functools import partial  # To prevent unwanted windows
import convert_round as cr
import settings_list as s
import settings_functions as sfunc
import api_functionality as api


class Converter:
    def __init__(self):

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
                                 text="error",
                                 fg="#960019",
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
        # self.input_frame.config(highlightbackground="red", highlightthickness=1)

        self.output_frame = Frame(self.convert_frame)
        self.output_frame.grid(column=1, row=0, pady=10)
        # self.output_frame.config(highlightbackground="blue", highlightthickness=1)

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
        button_details_list = [
            ["Convert", "#03AC13", self.input_checker, 0, 0],
            ["Swap", "#F96815", self.swap_inputs, 0, 1],
            ["Settings", "#0492C2", "", 1, 0],
            ["Help", "#A32CC4", "", 1, 1]
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

    def convert(self, value):
        input_currency_ico = api.currency_name_to_ico(self.input_combo_box.get())
        output_currency_ico = api.currency_name_to_ico(self.output_combo_box.get())

        exchange_rate = api.exchange_rate_get(input_currency_ico, output_currency_ico)
        answer = cr.convert_round_4dp(value, exchange_rate)

        answer_statement = f"{value} {input_currency_ico} is {answer} in {output_currency_ico}"

        self.error_label.config(text=answer_statement, fg="#960019", font=("Arial", "12", "bold"))
        self.output_entry.insert(0, answer)


    def input_checker(self):
        has_errors = False
        error = ""

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

        # getting all the values from all the comboboxes and dropdowns so we can swap them later
        input_dropdown = self.input_combo_box.get()
        output_dropdown = self.output_combo_box.get()
        input_entry = self.input_entry.get()
        output_entry = self.output_entry.get()

        self.input_combo_box.set(output_dropdown)
        self.output_combo_box.set(input_dropdown)
        self.input_entry.insert(0, output_entry)
        self.output_entry.insert(0, input_entry)



# main routine

# this makes sure that all the settings are correct and should always be before making the gui
# otherwise, in the main code, problems will arise when trying to use settings such as style if the settings are wrong
sfunc.settings_validator(s.settings.items(), (sfunc.settings_read(s.json_name)), s.default_dict, s.json_name)
root = Tk()
root.title("Currency Converter")
Converter()
root.mainloop()
