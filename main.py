from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib as mpl
import rastrigin_max as rm
from numpy import asarray
from numpy import sqrt
from threading import *

mpl.use("TkAgg")

# -------- Global variables ------------

color_main_window = "#EEF7FF"
color_sidebar = "#6DA4AA"
color_text = "#322C2B"
color_error = "#FF0080"
data = {}
means_arr = []
bounds_arr = []

# μέγεθος πληθυσμού, αριθμός των καλύτερων μελών, αριθμός γενιών, διασπορά της κατανομής, αρχική μέση τιμή της κατανομής, κάτω όριο πεδίου ορισμού, άνω όριο πεδίου ορισμού
default_entries_values = [100, 20, 5000, 2, 1, -5.12, 5.12, 0]


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        # ----------- variables  ------------
        self.entries = {}
        self.labels = {}
        self.separators = {}
        self.entries_error = []
        self.error = False
        self.msg = ""
        self.index = 1

        # ------------ Main window ------------
        self.geometry("1400x950")
        self.title("Simple Evolutionary Strategies")
        self.config(background=color_main_window)
        self.option_add("*Dialog.msg.font", "Modern 12")

        # ------------ Sidebar ------------
        self.style.configure("sidebar.TFrame", background=color_sidebar)
        self.sidebar = ttk.Frame(self, style="sidebar.TFrame")
        self.sidebar.place(relx=0, rely=0, relwidth=0.35, relheight=1)
        self.sidebar["padding"] = (0, 20, 0, 0)
        self.sidebar.grid_columnconfigure(0, weight=1)
        for i in range(23):
            self.sidebar.grid_rowconfigure(i + 1, weight=1)

        # ------------ Separators ---------
        self.style.configure("TSeparator", background=color_text)
        row = 4
        for i in range(7):
            self.separators["separator_{0}".format(i + 1)] = ttk.Separator(
                self.sidebar, orient="horizontal", style="TSeparator"
            )
            self.separators["separator_" + str(i + 1)].grid(row=row, ipadx=300, pady=20)
            row += 3

        # ------------ Labels ------------
        self.style.configure(
            "design.TLabel",
            background=color_sidebar,
            foreground=color_text,
            font="Modern 12 ",
            padding=(10, 0, 0, 6),
        )

        labels_text = [
            "Μέγεθος Πληθυσμού",
            "Αριθμός των καλύτερων μελών",
            "Αριθμός γενιών",
            "Διαστασιμότητα",
            "Διασπορά της κατανομής",
            "Κάτω όριο πεδίου ορισμού",
            "Άνω όριο πεδίου ορισμού",
            "Αρχική μέση τιμή της κατανομής",
            "1η διάσταση",
        ]
        row = 2
        for i in range(9):
            self.labels["label_{0}".format(i + 1)] = ttk.Label(
                self.sidebar, text=labels_text[i], style="design.TLabel"
            )
            self.labels["label_" + str(i + 1)].grid(row=row, sticky="W")
            row += 3

        self.labels["label_7"].grid(row=17, sticky="E")
        self.labels["label_8"].grid(row=20)
        self.labels["label_9"].grid(row=20, sticky="E", padx=(0, 10))

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
        row = 3
        for i in range(8):
            self.entries["entry_{0}".format(i + 1)] = ttk.Entry(
                self.sidebar, style="TEntry", width=12, font="Modern 12"
            )
            self.entries["entry_" + str(i + 1)].grid(row=row, padx=10, sticky="W")
            row += 3

        self.entries["entry_7"].grid(row=18, padx=10, sticky="E")
        self.entries["entry_8"].grid(row=21)

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
            font="Modern 10 ",
            relief="groove",
            command=self.threading,
        )
        self.btn_submit.grid(row=23, padx=(0, 50), pady=(0, 50), sticky="E")

        self.btn_next_dim = tk.Button(
            self.sidebar,
            text="→",
            activebackground=color_sidebar,
            activeforeground=color_main_window,
            fg=color_text,
            bg=color_main_window,
            padx=1,
            pady=1,
            width=3,
            wraplength=20,
            font="Modern 15  ",
            relief="groove",
            command=self.next_dimension,
        )
        self.btn_next_dim.grid(row=21, padx=(0, 50), sticky="E")
        self.btn_reset_form = tk.Button(
            self.sidebar,
            text="Επαναφορά",
            activebackground=color_sidebar,
            activeforeground=color_main_window,
            fg=color_text,
            bg=color_main_window,
            padx=10,
            pady=10,
            width=10,
            wraplength=120,
            font="Modern 10 ",
            relief="groove",
            command=self.set_default_values,
        )
        self.btn_reset_form.grid(row=23, pady=(0, 50), padx=(50, 0), sticky="W")

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

        self.set_default_values()

    # ------------- Functions ----------------
    def threading(self):
        t1 = Thread(target=self.submit_form)
        t1.start()

    def set_default_values(self):
        means_arr = []
        bounds_arr = []
        self.index = 1
        self.labels["label_9"]["text"] = "1η διάσταση"
        self.btn_next_dim["state"] = "normal"
        self.entries["entry_4"]["state"] = "normal"
        for i in range(3):
            self.entries["entry_" + str(6 + i)]["state"] = "normal"
        for i in range(8):
            self.entries["entry_" + str(i + 1)].delete(0, tk.END)
            self.entries["entry_" + str(i + 1)].insert(0, default_entries_values[i])

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

    def next_dimension(self):
        dim = self.entries["entry_4"].get()
        self.entries["entry_4"]["state"] = "disable"
        bound = []
        mean = None
        # Αμυντικός μηχανισμός για τα πεδία των πεδίων ορισμού και της μέσης τιμής
        try:
            # Μετατρέπει τις τιμες σε δεκαδικούς αριθμους, αν η τιμή δεν είναι αριθμός βγάζει σφάλμα
            bound = [
                float(self.entries["entry_6"].get()),
                float(self.entries["entry_7"].get()),
            ]
            mean = float(self.entries["entry_8"].get())
            # Ελέγχει αν το κάτω οριο είναι μεγαλύτερο του πάνω
            if bound[0] >= bound[1]:
                raise ValueError("bounds_error")
            # Ελέγχει αν το η μεση τιμή ειναι εντος ορίων
            elif mean < bound[0] or mean > bound[1]:
                raise ValueError("mean_error")
        except ValueError as e:
            self.error = True
            if str(e) == "bounds_error":
                self.entries["entry_7"].configure(style="error.TEntry")
                self.entries_error.append("entry_7")
                self.msg = "Το άνω όριο πρέπει να είναι μεγαλύτερο απο το κάτω."
            elif str(e) == "mean_error":
                self.entries["entry_8"].configure(style="error.TEntry")
                self.entries_error.append("entry_8")
                self.msg = "Η αρχική μέση τιμη της κατανομής πρέπει να κυμαίνετε εντός των ορίων."
            else:
                self.msg = "Για κάθε διάσταση εισάγεται στα πεδία της μεσης τιμης και του πεδίου ορισμού ακέραιο ή δεκαδικό αριθμό."
                for i in range(3):
                    self.entries["entry_" + str(6 + i)].configure(style="error.TEntry")
                    self.entries_error.append("entry_" + str(6 + i))

        if self.error:
            messagebox.showwarning("Μη έγκυρες τιμές", self.msg)
            for key in self.entries_error:
                self.entries[key].after(
                    100, self.entries[key].configure(style="TEntry")
                )
        else:
            means_arr.append(mean)
            bounds_arr.append(bound)
            self.index += 1
            if self.index > int(dim):
                self.btn_next_dim["state"] = "disabled"
                self.labels["label_9"]["text"] = str(self.index - 1) + "η διάσταση"
                for i in range(3):
                    self.entries["entry_" + str(6 + i)]["state"] = "disabled"
            else:
                self.labels["label_9"]["text"] = str(self.index) + "η διάσταση"
                for i in range(3):
                    self.entries["entry_" + str(6 + i)].delete(0, tk.END)

        self.error = False
        print(bounds_arr[0][1])

    def submit_form(self):
        self.entries_error = []
        self.msg = ""
        values = [0] * 5
        i = 0
        # Αμυντικός μηχανισμός για: "Μέγεθος Πληθυσμού, Αριθμός των καλύτερων μελών, Αριθμός γενιών, Διαστασιμότητα, Διασπορά της κατανομής
        for key in self.entries:
            if key == "entry_6":
                break
            value = self.entries[key].get()
            try:
                # Για το πεδίο της διασπορας, μετατρεπει την είσοδο σε δεκαδικο αριθμο
                if key == "entry_5":
                    values[i] = float(value)
                # Μετατρέπει τις εισόδους σε ακεραιους αριθμους, αν η τιμή δεν είναι αριθμός βγάζει σφάλμα
                else:
                    values[i] = int(value)
                # Αμυντικός μηχανισμός για αρνητικους αριθμούς
                if values[i] < 0:
                    raise ValueError()
            except ValueError:
                self.error = True
                self.entries[key].configure(style="error.TEntry")
                self.entries_error.append(key)
                self.msg = "Παρακαλώ εισάγεται θετικό ακέραιο αριθμό."
            i += 1
        if not self.error:
            try:
                # Ελέγχει αν το υπολοιπο της διαιρεσης (Μεγεθος πληθυσμού / Αριθμός καλύτερων μελών) είναι μηδενικό
                if values[0] % values[1] != 0:
                    raise ValueError("modulo_error")
                # Ελέγχει αν έχουν συμπληρωθεί τα πεδία ορισμού και οι μέσες τιμές για όλες τις διαστάσεις
                elif len(means_arr) != values[3] or len(bounds_arr) != values[3]:
                    raise ValueError("dimension_error")
            except ValueError as e:

                self.error = True
                if str(e) == "modulo_error":
                    self.msg = "Το υπόλοιπο της διαίρεσης: Μεγεθος πληθυσμού / Αριθμός καλύτερων μελών πρέπει να είναι ίσο με μηδέν."
                    self.entries["entry_1"].configure(style="error.TEntry")
                    self.entries_error.append("entry_1")
                elif str(e) == "dimension_error":
                    self.msg = "Συμπληρώστε πρώτα τα πεδία ορισμού και αρχικής μέσης τιμής για κάθε διάσταση."
                    for i in range(3):
                        self.entries["entry_" + str(6 + i)].configure(
                            style="error.TEntry"
                        )
                        self.entries_error.append("entry_" + str(6 + i))

        if self.error:
            data = {}
            messagebox.showwarning("Μη έγκυρες τιμές", self.msg)
            for key in self.entries_error:
                self.entries[key].after(
                    100,
                    self.entries[key].configure(style="TEntry"),
                )
            self.error = False

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
                "Μέσης_τιμή_κατανομής": means_arr,
                "Πεδία_ορισμού": bounds_arr,
            }

            # !define range for input
            bounds = asarray(
                [
                    [data["Πεδία_ορισμού"][0][0], data["Πεδία_ορισμού"][0][1]]
                    for _ in range(data["Διαστασιμότητα"])
                ]
            )

            std_dev = sqrt(data["Διασπορά_της_κατανομής"])
            # Αρχική τιμής της μέσης τιμής της κατανομής:
            # είτε τυχαία επιλογή ανάμεσα σε ένα εύρος είτε σε συγκεκριμένη τιμή.
            initial_mean = [data["Μέσης_τιμή_κατανομής"]] * data["Διαστασιμότητα"]
            initial_mean_np = asarray(initial_mean)
            best, score, generation_means = rm.es_comma(
                rm.objective,
                bounds,
                data["Αριθμός_γενιών"],
                std_dev,
                data["Αριθμός_των_καλύτερων_μελών"],
                data["Μέγεθος_Πληθυσμού"],
                initial_mean_np,
            )
            self.createPlot(generation_means)
            self.progress_bar.stop()
            self.btn_submit["state"] = "normal"
            self.progress_bar.place_forget()
            self.label_results = tk.Label(
                self,
                text="f(%s) = %f" % (best, -score),
                background=color_main_window,
                font=("Modern", 16, "bold"),
                fg="#3572EF<",
            )
            self.label_results.place(x=680, y=50)
            self.label_results.lift()
            print("f(%s) = %f" % (best, -score))
            print(data)


if __name__ == "__main__":

    app = App()
    app.mainloop()
