from tkinter import *
from functools import partial  # To prevent unwanted windows


class Converter:
    def __init__(self):

        self.base_frame = Frame(padx=10, pady=10)
        self.base_frame.grid()

        self.to_help_button = Button(self.base_frame,
                                     text="Help / Info",
                                     bg="#A32CC4",
                                     # fg determines the text colour
                                     fg="#FFFFFF",
                                     font=("Arial", "14", "bold"), width=12,
                                     command=self.to_help)
        self.to_help_button.grid(row=1, padx=5, pady=5)

    def to_help(self):
        """
        Opens help dialogue box and disables help button
        (so that users can't create multiple help boxes).
        """
        DisplayHelp(self)


class DisplayHelp:
    def __init__(self, partner):
        # setup dialogue box and background colour
        background = "#ffe6cc"
        self.help_box = Toplevel()

        # disable help button
        partner.to_help_button.config(state=DISABLED)

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
        partner.to_help_button.config(state=NORMAL)
        self.help_box.destroy()


if __name__ == "__main__":
    root = Tk()
    root.title("Currency Converter")
    Converter()
    root.mainloop()
