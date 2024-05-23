# main libs
from numpy import asarray
from numpy import exp
from numpy import sqrt
from numpy import square
from numpy import cos
from numpy import e
from numpy import pi
from numpy import argsort
from numpy.random import randn
from numpy.random import rand
from numpy.random import seed

# plot libs
import statistics
from numpy import arange
from numpy import meshgrid
from numpy import linspace
from matplotlib import pyplot
from matplotlib import cm

# for MyWindow
from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.animation as animation


class MyWindow:
    def __init__(self, win):

        # Ρύθμιση των παραθύρων εμφάνισης
        outputArea = Text(window, height=10, width=80)
        outputArea.place(x=90, y=400)
        graphArea = Text(window, height=31, width=80)
        graphArea.place(x=770, y=60)

        self.lbl1 = Label(win, text="a. Μέγεθος Πληθυσμού:")
        self.lbl2 = Label(
            win, text="b. Αριθμός των καλύτερων μελών για ανανέωση της κατανομής:"
        )
        self.lbl3 = Label(win, text="c. Αριθμός γενιών (generations):")
        self.lbl4 = Label(win, text="d. Αρχική τιμή της μέσης τιμής της κατανομής:")
        self.lbl5 = Label(win, text="   Τελική τιμή της μέσης τιμής της κατανομής:")
        self.lbl6 = Label(win, text="e. Αρχική τιμή της διασποράς της κατανομής:")
        self.t1 = Entry()
        self.t2 = Entry()
        self.t3 = Entry()
        self.t4 = Entry()
        self.t5 = Entry()
        self.t6 = Entry()

        self.b1 = Button(
            win,
            text="Simple Evolution Algorithm",
            command=lambda: self.control(outputArea, graphArea),
        )
        self.b2 = Button(win, text="Exit", command=window.destroy)

        self.lbl1.place(x=100, y=50)
        self.t1.place(x=110, y=70)
        self.lbl2.place(x=100, y=100)
        self.t2.place(x=110, y=120)
        self.lbl3.place(x=100, y=150)
        self.t3.place(x=110, y=170)
        self.lbl4.place(x=100, y=200)
        self.t4.place(x=110, y=220)
        self.lbl5.place(x=100, y=250)
        self.t5.place(x=110, y=270)
        self.lbl6.place(x=100, y=300)
        self.t6.place(x=110, y=320)
        self.b1.place(x=450, y=350)
        self.b2.place(x=650, y=350)

        # Τοποθέτηση αρχικών τιμών
        population_size = 100
        self.t1.insert(0, population_size)
        selected_parents = 20
        self.t2.insert(0, selected_parents)
        max_iterations = 5000
        self.t3.insert(0, max_iterations)
        r_min = -5.12
        self.t4.insert(0, r_min)
        r_max = 5.12
        self.t5.insert(0, r_max)
        step_size = 0.15
        self.t6.insert(0, step_size)

    # Function for Rastrigin plot
    def rastrigin_plot(self, x, y):
        self.x = x
        self.y = y
        return (x**2 - 10 * cos(2 * pi * x)) + (y**2 - 10 * cos(2 * pi * y)) + 20

    # Function for Gauss plot
    def gauss_plot(self, x, m, s):
        self.x = x
        self.m = m
        self.s = s
        return (1 / (s * sqrt(2 * pi))) * exp(-((x - m) ** 2) / (2 * s**2))

    # Fitness function via Gauss function
    def fitness(self, v):
        self.v = v
        x, m = v
        s = statistics.stdev(xaxis)
        return (1 / (s * sqrt(2 * pi))) * exp(-((x - m) ** 2) / (2 * s**2))

    # fitness function via Rastrigin function
    def fitnessR(self, v):
        self.v = v
        x, y = v
        return (x**2 - 10 * cos(2 * pi * x)) + (y**2 - 10 * cos(2 * pi * y)) + 20

    # fitness function via Ackley's multimodal function
    def fitnessA(self, v):
        self.v = v
        x, y = v
        return (
            -20.0 * exp(-0.2 * sqrt(0.5 * (x**2 + y**2)))
            - exp(0.5 * (cos(2 * pi * x) + cos(2 * pi * y)))
            + e
            + 20
        )

    # Ελέγχος, εάν ένας υποψήφιος γονέας ή παιδί είναι εντός ορίων
    def in_limits(self, candidate, limits):
        self.candidate = candidate
        self.limits = limits

        # LOOP στον πίνακα ορίων για έλεγχο υποψήφιου γονέα ή παιδιού
        for d in range(len(limits)):
            # Ελέγχος αν είναι εκτός ορίων
            if candidate[d] < limits[d, 0] or candidate[d] > limits[d, 1]:
                return False
        return True

    # Evolution Strategy αλγόριθμος με επιλογή για πρόσθεση επιλεγμένων γονέων
    def evolution_algorithm(
        self,
        graphArea,
        outputArea,
        limits,
        iteration_num,
        step_size,
        selected_parents,
        population_size,
    ):
        self.graphArea = graphArea
        self.outputArea = outputArea
        self.limits = limits
        self.iteration_num = iteration_num
        self.step_size = step_size
        self.selected_parents = selected_parents
        self.population_size = population_size

        best, best_eval = None, 1e10  # 1 X 10^10 = 10.000.000.000
        # Υπολογισμός παιδιών ανα γονείς
        n_children = int(population_size / selected_parents)
        # Αρχικοποίηση Πληθυσμού
        population = list()
        # Επανάληψη για πρόσθεση Υποψηφίων Γονέων βάσει μεγέθους δημιουργούμενου πληθυσμού
        for _ in range(population_size):
            candidate = None
            # Επανάληψη ενόσω ο υποψήφιος γονέας είναι εκτός ορίων
            while candidate is None or not self.in_limits(candidate, limits):
                # Δημιουργία υποψήφιου γονέα βάσει δεδομένων ορίων
                candidate = limits[:, 0] + rand(len(limits)) * (
                    limits[:, 1] - limits[:, 0]
                )
                population.append(candidate)

        child_per_gen = list()
        # Επανάληψη βάσει γενεών
        for generation in range(iteration_num):
            # Υπολογισμός βαθμολογιών (scores) και αποθήκευση σε ξεχωριστή παράλληλη λίστα
            scores = []
            for c in population:
                scores.append(self.fitness(c))
            # Κατάταξη βαθμολογιών (ranks) σε αύξουσα σειρά με διπλή κλήση ταξινόμησης
            ranks = argsort(argsort(scores))
            # Επιλογή δεικτών γονέων με την καλύτερη κατάταξη
            selected = []
            for x, _ in enumerate(ranks):  # Ανάγκη για δύο μεταβλητές οπότε x και _
                if ranks[x] < selected_parents:
                    selected.append(x)

            # Δημιουργία λίστας παιδιών
            children = list()
            # Επανάληψη στους επιλεγμένους γονείς
            for i in selected:
                # ΈΛεγχος αν αυτός ο γονέας είναι η βέλτιστη λύση και εκτύπωση δεδομένων
                if scores[i] < best_eval:
                    best, best_eval = population[i], scores[i]
                    gen_num = generation  # Αριθμός γενεών
                    pop_num = len(children)  # Πληθυσμός - (παιδιά) ανα γενιά
                    print("%4d, ΚΑΛΥΤΕΡΟ: f(%s) = %f" % (generation, best, best_eval))

                    # Εμφάνιση δεδομένων στο παραθυρικό περιβάλλον
                    buff = "%d, ΚΑΛΥΤΕΡΟ:f(%s)=%f" % (generation, best, best_eval)
                    outputArea.insert(END, buff + "\n")
                    outputArea.yview(END)

                    # Κλήση εμφάνισης διαγράμματος
                    if (
                        pop_num > 0 and gen_num > 0
                    ):  # Εμφάνιση γραφήματος όταν υπάρχουν Παιδιά - Γονείς
                        self.show_plot(graphArea, gen_num, pop_num)

                    if pop_num > population_size:
                        return [best, best_eval]

                # Loop βάσει παραμέτρου παιδιών
                for _ in range(n_children):  # Το _ για μη ανάγκη δείκτη
                    child = None
                    # Loop ενόσω το παιδί είναι εντός ή εκτός ορίων
                    while child is None or not self.in_limits(child, limits):
                        # Δημιουργία παιδιών
                        child = population[i] + randn(len(limits)) * step_size
                        children.append(child)

            # Πρόσθεση πληθυσμού απο παιδιά
            population = children

        return [best, best_eval]

    # Rastrigin plot
    def show_plot(self, graphArea, gen_num, pop_num):
        self.graphArea = graphArea
        self.gen_num = gen_num
        self.pop_num = pop_num

        # Εύρος εισόδου δειγμάτων ομοιόμορφα σε προσαυξήσεις step_size
        step_size = 0.15
        xaxis = arange(0, gen_num, step_size)
        yaxis = arange(0, pop_num, step_size)
        # Δημιουργία πλέγματος από τον άξονα
        x, y = meshgrid(xaxis, yaxis)
        # Υπολογισμός στόχων
        result = self.rastrigin_plot(x, y)
        # Δημιουργία διαγράμματος με σχήμα jet color
        fig = pyplot.figure()
        axis = fig.add_subplot(111, projection="3d")
        axis.plot_surface(x, y, result, cmap="jet")
        # Εμφάνιση διαγράμματος
        axis.set_xlabel("Αριθμός Γενεών")
        axis.set_ylabel("Πληθυσμός ανά Γενιά")
        plotname = "Rastrigin Graph - gen = " + str(gen_num)
        axis.set_title(plotname)

        # Εμφάνιση διαγράμματος στον καμβά
        # canvas = FigureCanvasTkAgg(fig, master = graphArea)
        # canvas.draw()
        # canvas.get_tk_widget().pack()

        # Αποθήκευση διαγράμματος
        pyplot.savefig(plotname)
        pyplot.show()

    def control(self, outputArea, graphArea):
        self.outputArea = outputArea
        self.graphArea = graphArea

        # Παράμετροι για την λειτουργία των εξελικτικών αλγορίθμων
        #
        # Σπόρος της γεννήτριας ψευδοτυχαίων αριθμών
        seed(1)
        # Oρισμός ελάχιστου και μέγιστου ορίου
        str_num = self.t4.get()
        if len(str_num) == 0:
            r_min = -5.12
        else:
            r_min = float(str_num)

        str_num = self.t5.get()
        if str_num == "":
            r_max = 5.12
        else:
            r_max = float(str_num)

        # Ορισμός για το μέγιστο μεγέθος βήματος
        str_num = self.t6.get()
        if len(str_num) == 0:
            step_size = 0.15
        else:
            step_size = float(str_num)

        # Ορισμός συνολικών επαναλλήψεων
        str_num = self.t3.get()
        if len(str_num) == 0:
            max_iterations = 5000
        else:
            max_iterations = int(str_num)

        # Αριθμός επιλεγμένων γονέων
        str_num = self.t2.get()
        if len(str_num) == 0:
            selected_parents = 20
        else:
            selected_parents = int(str_num)

        # Μέγεθος δημιουργούμενου πληθυσμού
        str_num = self.t1.get()
        if len(str_num) == 0:
            population_size = 100
        else:
            population_size = int(str_num)

        # Εμφάνιση λαθών παραμέτρων στο παραθυρικό περιβάλλον
        if population_size % selected_parents != 0 or selected_parents == 0:
            buff = "ΛΑΘΟΣ ΕΙΣΑΓΩΓΗΣ ΔΕΔΟΜΕΝΩΝ ΓΙΑ ΠΛΗΘΥΣΜΟ Ή ΓΟΝΕΙΣ"
            outputArea.insert(END, buff + "\n")
            buff = "Η ΔΙΑΙΡΕΣΗ ΠΛΗΘΥΣΜΟΥ ΠΡΟΣ ΓΟΝΕΙΣ ΠΡΕΠΕΙ ΝΑ ΕΧΕΙ ΥΠΟΛΟΙΠΟ 0"
            outputArea.insert(END, buff + "\n")
            outputArea.yview(END)
            return -1

        # Oρισμός πίνακα ορίων απο τις παραμέτρους ελάχιστου και μέγιστου
        # Τροποποίηση των ορισθέντων ορίων σε array
        limits = asarray([[r_min, r_max], [r_min, r_max]])

        # Εμφάνιση Διαγραμμάτος Gauss
        # Εύρος εισόδου βάσει παραμέτρων εισόδου ομοιόμορφα σε προσαυξήσεις 0,15
        global xaxis
        xaxis = arange(r_min, r_max, step_size)
        # Υπολογισμός στόχων βάσει εξίσωσης Gauss
        # result = self.gauss_plot(xaxis, mean, sd)
        mean = statistics.mean(xaxis)
        sd = statistics.stdev(xaxis)
        result = self.gauss_plot(xaxis, mean, sd)
        # Το figure περιέχει το plot
        fig = Figure(figsize=(6, 5), dpi=100)
        gaussplot = fig.add_subplot(111)
        # Εμφάνιση διαγράμματος στον καμβά
        gaussplot.plot(xaxis, result)
        gaussplot.set_title("Gaussian Normal Distribution")
        # Εμφάνιση διαγράμματος στον καμβά
        canvas = FigureCanvasTkAgg(fig, master=graphArea)
        canvas.draw()
        canvas.get_tk_widget().pack()
        # pyplot.show()

        # Κλήση του αλγορίθμου αξιολόγησης
        best, score = self.evolution_algorithm(
            graphArea,
            outputArea,
            limits,
            max_iterations,
            step_size,
            selected_parents,
            population_size,
        )
        print("\nΟΛΟΚΛΗΡΩΣΗ!")
        print("ΤΕΛΕΙΟ: f(%s) = %f" % (best, score))

        # Εμφάνιση δεδομένων στο παραθυρικό περιβάλλον
        buff = "ΟΛΟΚΛΗΡΩΣΗ!"
        outputArea.insert(END, buff + "\n")
        buff = "ΤΕΛΕΙΟ: f(%s) = %f" % (best, score)
        outputArea.insert(END, buff + "\n")
        outputArea.yview(END)


window = Tk()
mywin = MyWindow(window)
window.title("Παράμετροι και Εκτέλεση της Εξελικτικής Στρατηγικής")
window.geometry("1450x600+10+10")

window.mainloop()
