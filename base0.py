from tkinter import *
from tkinter import messagebox, ttk
import requests
import json
import pandas


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

        self.input_combo_box = ttk.Combobox(self.input_frame, state="readonly")
        self.input_combo_box.grid(row=1)

        # output_frame contents
        self.output_label = Label(self.output_frame,
                                  text="Currency to convert to",
                                  font=("Arial", "12")
                                  )
        self.output_label.grid(row=0)

        self.output_combo_box = ttk.Combobox(self.output_frame, state="readonly")
        self.output_combo_box.grid(row=1)

        # button list (button text | bg colour | command | row | column)
        button_details_list = [
            ["Convert", "#03AC13", "", 0, 0],
            ["Swap", "#F96815", "", 0, 1],
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


# main routine
root = Tk()
root.title("Currency Converter")
Converter()
root.mainloop()
