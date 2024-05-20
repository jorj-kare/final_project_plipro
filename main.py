import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from numpy import asarray, exp
from numpy.random import randn, uniform
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Rastrigin objective function
def rastrigin(X):
    return 10 * len(X) + sum([(x**2 - 10 * np.cos(2 * np.pi * x)) for x in X])

def objective(X):
    return -rastrigin(X)

# Evolution Strategy (μ, λ) algorithm
def es_comma(objective, bounds, n_iter, step_size, mu, lam):
    n_var = bounds.shape[0]
    # initial population of random vectors
    pop = uniform(bounds[:, 0], bounds[:, 1], (lam, n_var))
    # evaluate the objective function
    scores = asarray([objective(d) for d in pop])
    # keep track of the best solution
    best = pop[np.argmax(scores)]
    best_eval = np.max(scores)
    # list to store the mean value of each generation
    mean_values = [np.mean(scores)]
    # run the algorithm
    for gen in range(n_iter):
        # select the top mu members
        selected = pop[np.argsort(scores)[-mu:]]
        # generate children
        children = list()
        for i in range(lam):
            # select parent
            ix = np.random.randint(mu)
            parent = selected[ix]
            # create a mutated version
            child = parent + step_size * randn(n_var)
            # store for next generation
            children.append(child)
        # replace population
        pop = asarray(children)
        # evaluate scores
        scores = asarray([objective(d) for d in pop])
        # keep track of the best solution
        best = pop[np.argmax(scores)]
        best_eval = np.max(scores)
        # store the mean value of this generation
        mean_values.append(np.mean(scores))
    return [best, best_eval, mean_values]

# Main application class

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Evolutionary Strategies with GUI")
        self.geometry("800x600")

        self.sidebar = ttk.Frame(self, width=200)
        self.sidebar.pack(side="left", fill="y")

        self.content = ttk.Frame(self)
        self.content.pack(side="right", fill="both", expand=True)

        self.create_sidebar()
        self.create_plot_area()

    def create_sidebar(self):
        self.sidebar.grid_propagate(False)
        self.sidebar.grid_rowconfigure(0, weight=1)

        labels_pos = {"sticky": "w", "padx": 5, "pady": 5}
        entries_pos = {"sticky": "ew", "padx": 5, "pady": 5}
        entries_opt = {"width": 10}

        label_1 = ttk.Label(self.sidebar, text="Μέγεθος Πληθυσμού", style="design.TLabel")
        label_1.grid(row=1, **labels_pos)
        self.entry_1 = ttk.Entry(self.sidebar, style="TEntry", **entries_opt)
        self.entry_1.grid(row=2, **entries_pos)

        label_2 = ttk.Label(self.sidebar, text="Αριθμός Καλύτερων Μελών", style="design.TLabel")
        label_2.grid(row=3, **labels_pos)
        self.entry_2 = ttk.Entry(self.sidebar, style="TEntry", **entries_opt)
        self.entry_2.grid(row=4, **entries_pos)

        label_3 = ttk.Label(self.sidebar, text="Αριθμός Γενιών", style="design.TLabel")
        label_3.grid(row=5, **labels_pos)
        self.entry_3 = ttk.Entry(self.sidebar, style="TEntry", **entries_opt)
        self.entry_3.grid(row=6, **entries_pos)

        label_4 = ttk.Label(self.sidebar, text="Αρχική Τιμή Διασποράς", style="design.TLabel")
        label_4.grid(row=7, **labels_pos)
        self.entry_4 = ttk.Entry(self.sidebar, style="TEntry", **entries_opt)
        self.entry_4.grid(row=8, **entries_pos)

        label_5 = ttk.Label(self.sidebar, text="Αρχική Τιμή Μέσης Τιμής", style="design.TLabel")
        label_5.grid(row=9, **labels_pos)
        self.entry_5 = ttk.Entry(self.sidebar, style="TEntry", **entries_opt)
        self.entry_5.grid(row=10, **entries_pos)

        label_6 = ttk.Label(self.sidebar, text="Εύρος Αρχικής Τιμής (0 αν σταθερή)", style="design.TLabel")
        label_6.grid(row=11, **labels_pos)
        self.entry_6 = ttk.Entry(self.sidebar, style="TEntry", **entries_opt)
        self.entry_6.grid(row=12, **entries_pos)

        label_7 = ttk.Label(self.sidebar, text="Διαστασιμότητα", style="design.TLabel")
        label_7.grid(row=13, **labels_pos)
        self.entry_7 = ttk.Entry(self.sidebar, style="TEntry", **entries_opt)
        self.entry_7.grid(row=14, **entries_pos)

        self.button = ttk.Button(self.sidebar, text="Υποβολή", command=self.submit_form)
        self.button.grid(row=15, **labels_pos)

    def create_plot_area(self):
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.content)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def createPlot(self, data):
        self.ax.clear()
        self.ax.plot(data["Generations"], data["Mean Value"])
        self.ax.set_xlabel("Generations")
        self.ax.set_ylabel("Mean Value of Objective Function")
        self.canvas.draw_idle()

    def submit_form(self):
        error = False
        msg = ""
        values = [0] * 7
        for i in range(0, 7):
            entry = getattr(self, "entry_" + str(i + 1))
            value = entry.get()
            try:
                values[i] = float(value)
            except ValueError:
                error = True
                msg = "Οι τιμές πρέπει να είναι αριθμοί"
                break

        if values[1] > values[0]:
            error = True
            msg = "Ο αριθμός των καλύτερων μελών πρέπει να είναι μικρότερος ή ίσος με το μέγεθος πληθυσμού"

        if error:
            messagebox.showwarning("Μη έγκυρες τιμές", msg)
        else:
            self.run_evolution_strategy(values)

    def run_evolution_strategy(self, values):
        lam = int(values[0])
        mu = int(values[1])
        generations = int(values[2])
        step_size = values[3]
        dimensions = int(values[6])
        bounds = asarray([[-step_size, step_size] for _ in range(dimensions)])
        initial_mean = [values[4] if values[5] == 0 else round(uniform(values[4], values[5]), 2)] * dimensions

        best, score, generation_means = es_comma(objective, bounds, generations, step_size, mu, lam)
        self.createPlot({"Generations": range(len(generation_means)), "Mean Value": generation_means})
        print(f'f({best}) = {-score}')

if __name__ == "__main__":
    app = App()
    app.mainloop()

