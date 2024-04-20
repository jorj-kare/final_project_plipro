import tkinter as tk
from tkinter import ttk
import matplotlib as mpl


# -------- Global variables ------------

color_main_window = "#F5E1FD"


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        # ---------------
        self.geometry("1200x800")
        self.resizable(0, 0)
        self.title("Simple Evolutionary Strategies")
        self.config(background=color_main_window)


if __name__ == "__main__":

    app = App()
    app.mainloop()
