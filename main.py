import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from random import uniform
import matplotlib as mpl

mpl.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# -------- Global variables ------------

color_main_window = "#FFFBDA"
color_sidebar = "#77B0AA"
color_header = "#F6D6D6"
color_text = "#322C2B"
data = {}


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        style = ttk.Style(self)
        style.theme_use("clam")

        # ------------ Main window ------------
        self.geometry("1200x800")
        self.resizable(0, 0)
        self.title("Simple Evolutionary Strategies")
        self.config(background=color_main_window)

        # ------------ Header ------------

        self.header = tk.Frame(self, bg=color_main_window)
        self.header.place(relx=0.3, rely=0, relwidth=0.7, relheight=0.12)

        # ------------ Sidebar ------------
        style.configure("sidebar.TFrame", background=color_sidebar)
        self.sidebar = ttk.Frame(self, style="sidebar.TFrame")
        self.sidebar.place(relx=0, rely=0, relwidth=0.3, relheight=1)
        self.sidebar.grid_columnconfigure(0, weight=1)

        # ------------ Separators ---------
        style.configure(
            "TSeparator",
            background=color_text,
        )
        seperator_pos = {"ipadx": 250, "pady": 20}
        separator = ttk.Separator(self.sidebar, orient="horizontal", style="TSeparator")
        separator.grid(row=1, **seperator_pos)
        separator_1 = ttk.Separator(
            self.sidebar, orient="horizontal", style="TSeparator"
        )
        separator_1.grid(row=4, **seperator_pos)
        separator_2 = ttk.Separator(
            self.sidebar, orient="horizontal", style="TSeparator"
        )
        separator_2.grid(row=7, **seperator_pos)
        separator_3 = ttk.Separator(
            self.sidebar, orient="horizontal", style="TSeparator"
        )
        separator_3.grid(row=10, **seperator_pos)
        separator_4 = ttk.Separator(
            self.sidebar, orient="horizontal", style="TSeparator"
        )
        separator_4.grid(row=13, **seperator_pos)
        separator_5 = ttk.Separator(
            self.sidebar, orient="horizontal", style="TSeparator"
        )
        separator_5.grid(row=16, **seperator_pos)

        # ------------ Labels ------------
        style.configure(
            "design.TLabel",
            background=color_sidebar,
            foreground=color_text,
            font="Modern 12 ",
            padding=(10, 0, 0, 6),
        )
        style.configure(
            "titles.TLabel",
            background=color_sidebar,
            foreground=color_text,
            font="Modern 18 bold",
            padding=(0, 23, 0, 18),
        )
        labels_pos = {"sticky": "W"}
        label = ttk.Label(self.sidebar, text="Μεταβλητές", style="titles.TLabel")
        label.grid(row=0)
        label_1 = ttk.Label(
            self.sidebar, text="Μέγεθος Πληθυσμού", style="design.TLabel"
        )
        label_1.grid(row=2, **labels_pos)

        label_2 = ttk.Label(
            self.sidebar,
            text="Αριθμός των καλύτερων μελών",
            style="design.TLabel",
        )
        label_2.grid(row=5, **labels_pos)
        label_3 = ttk.Label(
            self.sidebar,
            text="Αριθμός γενιών ",
            style="design.TLabel",
        )
        label_3.grid(row=8, **labels_pos)
        label_4 = ttk.Label(
            self.sidebar,
            text="Διασπορά της κατανομή ",
            style="design.TLabel",
        )
        label_4.grid(row=11, **labels_pos)
        label_5 = ttk.Label(
            self.sidebar,
            text="Μέσης τιμή κατανομής ",
            style="design.TLabel",
        )
        label_5.grid(row=14, **labels_pos)
        label_6 = ttk.Label(
            self.sidebar,
            text="*Για τυχαία επιλογή ανάμεσα \n σε δυο τιμές συμπληρώστε \n και τα δυο πεδία .",
            style="design.TLabel",
            font="Italian 9 ",
        )
        label_6.grid(
            row=15,
        )

        # ------------ Entries ------------
        style.configure(
            "TEntry",
            background="#E3FEF7",
            foreground=color_text,
            relief="sunken",
            padding=(5, 5, 5, 0),
        )
        entries_opt = {
            "font": "Modern 12",
            "width": 12,
        }
        entries_pos = {"padx": 10, "sticky": "W"}

        self.entry_1 = ttk.Entry(self.sidebar, style="TEntry", **entries_opt)
        self.entry_1.grid(row=3, **entries_pos)

        self.entry_2 = ttk.Entry(self.sidebar, style="TEntry", **entries_opt)
        self.entry_2.grid(row=6, **entries_pos)
        self.entry_3 = ttk.Entry(self.sidebar, style="TEntry", **entries_opt)
        self.entry_3.grid(row=9, **entries_pos)
        self.entry_4 = ttk.Entry(self.sidebar, style="TEntry", **entries_opt)
        self.entry_4.grid(row=12, **entries_pos)
        self.entry_5 = ttk.Entry(self.sidebar, style="TEntry", width=6)
        self.entry_5.grid(row=15, **entries_pos)
        self.entry_6 = ttk.Entry(self.sidebar, style="TEntry", width=6)
        self.entry_6.grid(row=15, padx=10, sticky="E")

        # ------------ Buttons ------------
        btn_submit = tk.Button(
            self.sidebar,
            text="Καταχώρηση",
            activebackground=color_sidebar,
            activeforeground=color_main_window,
            fg=color_text,
            bg="white",
            padx=10,
            pady=15,
            width=15,
            wraplength=120,
            font="Modern 12 ",
            relief="groove",
            command=self.submit_form,
        )
        btn_submit.grid(row=17, pady=20)
        # ------------- Plot --------------
        self.fig = Figure()
        self.ax = self.fig.add_subplot()
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.place(relx=0.3, rely=0.25, relwidth=0.7, relheight=0.7)
        NavigationToolbar2Tk(self.canvas, self)

    def createPlot(self, data):

        self.ax.clear()
        keys = data.keys()
        values = data.values()
        self.ax.bar(keys, values)
        self.canvas.draw_idle()

    def submit_form(self):
        error = False
        msg = ""
        values = [0] * 6
        for i in range(0, 6):
            entry = getattr(self, "entry_" + str(i + 1))
            value = entry.get()
            if i == 5:
                if not value:
                    value = 0
                    break
                if int(value) < values[i - 1]:
                    error = True
                    msg = "Στην μέση τιμή κατανομής η τιμή στο δεύτερο πεδίο πρεπει να είναι μεγαλύτερη απο την τιμή στο πρώτο "

            if not value.isnumeric():
                error = True
                msg = "Οι τιμες πρεπει να είναι αριθμοί"
            else:
                values[i] = int(value)

        if error:
            data = {}
            messagebox.showwarning("Μη έγκυρες τιμές", msg)
        else:
            data = {
                "Μέγεθος_Πληθυσμού": values[0],
                "Αριθμός_των_καλύτερων_μελών": values[1],
                "Αριθμός_γενιών": values[2],
                "Διασπορά_της_κατανομή": values[3],
                "Μέσης_τιμή_κατανομής": (
                    values[4]
                    if values[5] == 0
                    else round(uniform(values[4], values[5]), 2)
                ),
            }
            self.createPlot(data)

        print(data)


if __name__ == "__main__":

    app = App()
    app.mainloop()
