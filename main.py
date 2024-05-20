import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from random import uniform
import matplotlib as mpl
import rastrigin_max as rm
from numpy import asarray

mpl.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# -------- Global variables ------------

color_main_window = "#FFFBDA"
color_sidebar = "#77B0AA"
color_header = "#F6D6D6"
color_text = "#322C2B"
color_error = "#FF0080"
data = {}


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        # ------------ Main window ------------
        self.geometry("1200x700")
        self.resizable(0, 0)
        self.title("Simple Evolutionary Strategies")
        self.config(background=color_main_window)

        # ------------ Header ------------

        self.header = tk.Frame(self, bg=color_main_window)
        self.header.place(relx=0.3, rely=0, relwidth=0.7, relheight=0.12)

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
        seperator_pos = {"ipadx": 250, "pady": 20}
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
            text="Αρχική τιμής της διασποράς της κατανομή ",
            style="design.TLabel",
        )
        label_4.grid(row=11, **labels_pos)
        label_5 = ttk.Label(
            self.sidebar,
            text="Αρχική τιμή της μέσης τιμή της κατανομής ",
            style="design.TLabel",
        )
        label_5.grid(row=14, **labels_pos)
        # label_6 = ttk.Label(
        #     self.sidebar,
        #     text="*Για τυχαία επιλογή ανάμεσα \n σε δυο τιμές συμπληρώστε \n και τα δυο πεδία .",
        #     style="design.TLabel",
        #     font="Italian 9 ",
        # )
        # label_6.grid(
        #     row=15,
        # )

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
        self.entry_5 = ttk.Entry(self.sidebar, style="TEntry", width=6)
        self.entry_5.grid(row=15, **entries_pos)
        # ------------ Checkbox -----------

        self.checked = tk.BooleanVar()
        self.checkbox = tk.Checkbutton(
            self.sidebar,
            text="Τυχαία επιλογή \n ανάμεσα σε ενα εύρος",
            variable=self.checked,
            background=color_sidebar,
            activebackground=color_sidebar,
            foreground=color_text,
            activeforeground=color_text,
            bg=color_sidebar,
            bd=0,
        )
        self.checkbox.grid(row=15, sticky="E")
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
        self.plt = self.fig.add_subplot()
        self.plt.set_title("Τίτλος γραφήματος", fontsize=16),
        self.plt.set_ylabel(
            "Mέση τιμή του πληθυσμού ανά γενιά",
            fontsize=12,
        )
        self.plt.set_xlabel(
            "Αριθμός γενεών",
            fontsize=12,
        )
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.place(relx=0.35, rely=0, relwidth=0.65, relheight=0.95)
        NavigationToolbar2Tk(self.canvas, self)

    def createPlot(self, data):
        self.plt.clear()
        self.plt.plot(data)
        self.canvas.draw_idle()

    def submit_form(self):
        entries_error = []
        error = False
        msg = ""

        values = [0] * 5
        print(self.checked.get())
        for i in range(0, 5):
            entry = getattr(self, "entry_" + str(i + 1))
            value = entry.get()

            try:
                if i == 3:
                    values[i] = float(value)
                else:
                    values[i] = int(value)
            except ValueError:
                error = True
                msg = (
                    "Παρακαλώ εισάγεται ακέραιο ή δεκαδικό αριθμό."
                    if i == 3
                    else "Παρακαλώ εισάγεται ακέραιο αριθμό."
                )
                entry.configure(style="error.TEntry")
                entries_error.append(entry)

        if error:
            data = {}
            messagebox.showwarning("Μη έγκυρες τιμές", msg)
            for e in entries_error:
                e.after(
                    100,
                    e.configure(style="TEntry"),
                )

        else:
            data = {
                "Μέγεθος_Πληθυσμού": int(values[0]),
                "Αριθμός_των_καλύτερων_μελών": int(values[1]),
                "Αριθμός_γενιών": int(values[2]),
                "Διασπορά_της_κατανομής": float(values[3]),
                "Μέσης_τιμή_κατανομής": int(values[4]),
            }

            # define range for input
            bounds = asarray(
                [
                    [-data["Διασπορά_της_κατανομής"], data["Διασπορά_της_κατανομής"]]
                    for _ in range(data["Μέσης_τιμή_κατανομής"])
                ]
            )

            # define the maximum step size
            step_size = 0.15

            # Αρχική τιμής της μέσης τιμής της κατανομής:
            # είτε τυχαία επιλογή ανάμεσα σε ένα εύρος είτε σε συγκεκριμένη τιμή.
            initial_mean = [-data["Διασπορά_της_κατανομής"]] * data[
                "Μέσης_τιμή_κατανομής"
            ]
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


if __name__ == "__main__":

    app = App()
    app.mainloop()
