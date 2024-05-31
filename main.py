import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from random import uniform
import matplotlib as mpl
import rastrigin_max as rm
from numpy import asarray
from threading import *

mpl.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# -------- Global variables ------------

color_main_window = "#EEF7FF"
color_sidebar = "#6DA4AA"
color_text = "#322C2B"
color_error = "#FF0080"
data = {}


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        # ------------ Main window ------------
        self.geometry("1400x950")
        # self.resizable(0, 0)
        self.title("Simple Evolutionary Strategies")
        self.config(background=color_main_window)
        self.option_add("*Dialog.msg.font", "Modern 12")
        # ------------ Sidebar ------------
        self.style.configure("sidebar.TFrame", background=color_sidebar)
        self.sidebar = ttk.Frame(self, style="sidebar.TFrame")
        self.sidebar.place(relx=0, rely=0, relwidth=0.35, relheight=1)
        self.sidebar["padding"] = (0, 20, 0, 0)
        self.sidebar.grid_columnconfigure(0, weight=1)
        # ------------ Separators ---------
        self.style.configure(
            "TSeparator",
            background=color_text,
        )
        seperator_pos = {"ipadx": 300, "pady": 20}
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
        separator_5 = ttk.Separator(
            self.sidebar, orient="horizontal", style="TSeparator"
        )
        separator_5.grid(row=19, **seperator_pos)
        separator_6 = ttk.Separator(
            self.sidebar, orient="horizontal", style="TSeparator"
        )
        separator_6.grid(row=22, **seperator_pos)

        # ------------ Labels ------------
        self.style.configure(
            "design.TLabel",
            background=color_sidebar,
            foreground=color_text,
            font="Modern 12 ",
            padding=(10, 0, 0, 6),
        )
        labels_pos = {"sticky": "W"}
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
            text="Διαστασιμότητα",
            style="design.TLabel",
        )
        label_4.grid(row=11, **labels_pos)
        label_5 = ttk.Label(
            self.sidebar,
            text="Διασπορά της κατανομής ",
            style="design.TLabel",
        )
        label_5.grid(row=14, **labels_pos)
        label_6 = ttk.Label(
            self.sidebar,
            text="Αρχική μέση τιμή της κατανομής ",
            style="design.TLabel",
        )
        label_6.grid(row=17, **labels_pos)
        label_7 = ttk.Label(
            self.sidebar,
            text="Κάτω όριο πεδίου ορισμού ",
            style="design.TLabel",
        )
        label_7.grid(row=20, **labels_pos)
        label_8 = ttk.Label(
            self.sidebar,
            text="Άνω όριο πεδίου ορισμού",
            style="design.TLabel",
        )
        label_8.grid(row=20, padx=10, sticky="E")

        # ------------ Entries ------------
        self.style.configure(
            "TEntry",
            fieldbackground=color_main_window,
            foreground=color_text,
            relief="sunken",
            padding=(5, 5, 5, 0),
        )
        self.style.configure(
            "error.TEntry",
            fieldbackground=color_main_window,
            foreground=color_error,
            bordercolor=color_error,
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
        self.entry_5 = ttk.Entry(self.sidebar, style="TEntry", **entries_opt)
        self.entry_5.grid(row=15, **entries_pos)
        self.entry_6 = ttk.Entry(self.sidebar, style="TEntry", **entries_opt)
        self.entry_6.grid(row=18, **entries_pos)
        self.entry_7 = ttk.Entry(self.sidebar, style="TEntry", **entries_opt)
        self.entry_7.grid(row=21, **entries_pos)
        self.entry_8 = ttk.Entry(self.sidebar, style="TEntry", **entries_opt)
        self.entry_8.grid(row=21, padx=10, sticky="E")

        # ------------ Buttons ------------
        self.btn_submit = tk.Button(
            self.sidebar,
            text="Καταχώρηση",
            activebackground=color_sidebar,
            activeforeground=color_main_window,
            fg=color_text,
            bg=color_main_window,
            padx=10,
            pady=10,
            width=15,
            wraplength=120,
            font="Modern 12 ",
            relief="groove",
            command=self.threading,
        )
        self.btn_submit.grid(row=23)

        # ------------- ProgressBar --------------
        self.style.configure(
            "Horizontal.TProgressbar",
            background=color_main_window,
            troughcolor=color_sidebar,
            bordercolor=color_sidebar,
            lightcolor=color_main_window,
            darkcolor=color_sidebar,
        )
        self.progress_bar = ttk.Progressbar(
            self, orient="horizontal", mode="indeterminate", length=200
        )

        # ------------- Plot --------------
        self.fig = Figure(facecolor=color_main_window)
        self.plt = self.fig.add_subplot(facecolor=color_main_window)
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.place(relx=0.35, rely=0, relwidth=0.65, relheight=0.95)
        NavigationToolbar2Tk(self.canvas, self)

    def createPlot(self, data):
        self.plt.clear()
        # self.plt.set_title("Τίτλος γραφήματος", fontsize=16),
        self.plt.set_ylabel(
            "Mέση τιμή του πληθυσμού ανά γενιά",
            fontsize=12,
        )
        self.plt.set_xlabel(
            "Αριθμός γενεών",
            fontsize=12,
        )
        self.plt.plot(data)
        self.canvas.draw_idle()

    def threading(self):
        t1 = Thread(target=self.submit_form)
        t1.start()

    def submit_form(self):

        entries_error = []
        error = False
        msg = ""

        values = [0] * 8

        for i in range(0, 8):
            entry = getattr(self, "entry_" + str(i + 1))
            value = entry.get()

            try:
                if i >= 4:
                    values[i] = float(value)
                else:
                    values[i] = int(value)

            except ValueError:
                error = True
                msg = (
                    "Παρακαλώ εισάγεται ακέραιο ή δεκαδικό αριθμό."
                    if i >= 4
                    else "Παρακαλώ εισάγεται ακέραιο αριθμό."
                )
                entry.configure(style="error.TEntry")
                entries_error.append(entry)

        if not error:
            if values[0] % values[1] != 0:
                error = True
                entry = getattr(self, "entry_1")
                entry.configure(style="error.TEntry")
                entries_error.append(entry)
                msg = "Το υπόλοιπο της διαίρεσης: Μεγεθος πληθυσμού / Αριθμός καλύτερων μελών πρέπει να είναι ίσο με μηδέν."
            elif values[6] >= values[7]:
                error = True
                entry = getattr(self, "entry_8")
                entry.configure(style="error.TEntry")
                entries_error.append(entry)
                msg = "Το άνω όριο πρέπει να είναι μεγαλύτερο απο το κάτω."

        if error:
            data = {}
            messagebox.showwarning("Μη έγκυρες τιμές", msg)
            for e in entries_error:
                e.after(
                    100,
                    e.configure(style="TEntry"),
                )

        else:
            self.btn_submit["state"] = "disabled"
            self.progress_bar.place(x=920, y=365)
            self.progress_bar.lift()
            self.progress_bar.start()
            data = {
                "Μέγεθος_Πληθυσμού": values[0],
                "Αριθμός_των_καλύτερων_μελών": values[1],
                "Αριθμός_γενιών": values[2],
                "Διαστασιμότητα": values[3],
                "Διασπορά_της_κατανομής": values[4],
                "Μέσης_τιμή_κατανομής": values[5],
                "Κάτω_οριο": values[6],
                "Ανω_όριο": values[7],
            }

            # define range for input
            bounds = asarray(
                [
                    [data["Κάτω_οριο"], data["Ανω_όριο"]]
                    for _ in range(data["Διαστασιμότητα"])
                ]
            )

            step_size = data["Διασπορά_της_κατανομής"]
            # Αρχική τιμής της μέσης τιμής της κατανομής:
            # είτε τυχαία επιλογή ανάμεσα σε ένα εύρος είτε σε συγκεκριμένη τιμή.
            initial_mean = [data["Μέσης_τιμή_κατανομής"]] * data["Διαστασιμότητα"]
            initial_mean_np = asarray(initial_mean)
            best, score, generation_means = rm.es_comma(
                rm.objective,
                bounds,
                data["Αριθμός_γενιών"],
                step_size,
                data["Αριθμός_των_καλύτερων_μελών"],
                data["Μέγεθος_Πληθυσμού"],
                initial_mean_np,
                data["Διασπορά_της_κατανομής"],
            )
            self.createPlot(generation_means)
            self.progress_bar.stop()
            self.btn_submit["state"] = "normal"
            self.progress_bar.place_forget()
            self.label_results = tk.Label(
                self, text="f(%s) = %f" % (best, -score), background=color_main_window
            )
            self.label_results.place(x=680, y=50)
            self.label_results.lift()
            print("f(%s) = %f" % (best, -score))


if __name__ == "__main__":

    app = App()
    app.mainloop()
