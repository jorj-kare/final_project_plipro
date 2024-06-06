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

# Tkinter and plot libs
from tkinter import *
from tkinter.scrolledtext import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class MyWindow:
    def __init__(self, win):

        # Ρύθμιση των παραθύρων εμφάνισης
        # Περιοχή για εμφάνιση αποτελεσμάτων
        outputArea = ScrolledText(window, height="10", width="80", wrap=WORD)
        outputArea.place(x=90, y=410)

        # Περιοχή για εμφάνιση γραφημάτων
        graphArea = Canvas(win, bg="white", height=530, width=600)
        graphArea.place(x=770, y=45)

        self.lbl1 = Label(win, text="a. Μέγεθος Πληθυσμού:")
        self.lbl2 = Label(
            win, text="b. Αριθμός των καλύτερων μελών για ανανέωση της κατανομής:"
        )
        self.lbl3 = Label(win, text="c. Αριθμός γενιών (generations):")
        self.lbl4 = Label(win, text="d. Αρχική τιμή της μέσης τιμής της κατανομής:")
        self.lbl5 = Label(win, text="   Τελική τιμή της μέσης τιμής της κατανομής:")
        self.lbl6 = Label(win, text="e. Αρχική τιμή της διασποράς της κατανομής:")
        self.lbl7 = Label(
            win,
            text="   Επιλογή Fitness function, (G) Gauss, (R) Rastrigin, (A) Ackley:",
        )

        self.t1 = Entry()
        self.t2 = Entry()
        self.t3 = Entry()
        self.t4 = Entry()
        self.t5 = Entry()
        self.t6 = Entry()
        self.t7 = Entry()

        self.b1 = Button(
            win,
            text="Simple Evolution Algorithm",
            command=lambda: self.control(outputArea, graphArea),
        )
        self.b2 = Button(win, text="Έξοδος", command=win.destroy)
        self.b3 = Button(
            win, text="Προηγούμενο", command=lambda: self.step_in_graph(-1)
        )
        self.b4 = Button(win, text="Επόμενο", command=lambda: self.step_in_graph(1))

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
        self.lbl7.place(x=100, y=350)
        self.t7.place(x=110, y=370)
        self.b1.place(x=500, y=370)
        self.b2.place(x=680, y=370)
        self.b3.place(x=1000, y=15)
        self.b4.place(x=1100, y=15)

        # Τοποθέτηση αρχικών τιμών
        population_size = 100
        self.t1.insert(0, population_size)
        best_members = 20
        self.t2.insert(0, best_members)
        max_generations = 5000
        self.t3.insert(0, max_generations)
        r_min = -5.12
        self.t4.insert(0, r_min)
        r_max = 5.12
        self.t5.insert(0, r_max)
        dispersion = 0.11
        self.t6.insert(0, dispersion)
        fitness_var = "G"
        self.t7.insert(0, fitness_var)

    # Βηματισμός, επόμενο - προηγούμενο στα διαγράμματα
    def step_in_graph(self, change_by=0):
        self.change_by = change_by

        first_key = 1
        # Αριθμός γραφημάτων
        global cnt_graph
        last_key = cnt_graph + 1
        global key

        # Μετακίνηση στο επόμενο
        if change_by == 1 and key < last_key:
            key = key + change_by

        # Εμφάνιση στην περιοχή  Πρώτου - Τελευταίου γραφήματος
        if key > first_key and key < last_key:
            graph = FigureCanvasTkAgg(globals()[f"fig{key}"], master=self.graphArea)
            graph.draw()
            graph.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=False)
            print("Γράφημα %d Εμφανίστηκε", key)

        # Μετακίνηση στο προηγούμενο
        if change_by == -1 and key > first_key:
            key = key + change_by

        return

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
        return 1 / (sqrt(2 * pi * (s**2))) * exp(-((x - m) ** 2) / (2 * (s**2)))

    # Fitness using Gauss function
    def fitnessG(self, v):
        self.v = v
        x, m = v
        s = statistics.stdev(Gxaxis)
        return 1 / (sqrt(2 * pi * (s**2))) * exp(-((x - m) ** 2) / (2 * (s**2)))

    # fitness using Rastrigin function
    def fitnessR(self, v):
        self.v = v
        x, y = v
        return (x**2 - 10 * cos(2 * pi * x)) + (y**2 - 10 * cos(2 * pi * y)) + 20

    # fitness using Ackley's function
    def fitnessA(self, v):
        self.v = v
        x, y = v
        return (
            -20.0 * exp(-0.2 * sqrt(0.5 * (x**2 + y**2)))
            - exp(0.5 * (cos(2 * pi * x) + cos(2 * pi * y)))
            + e
            + 20
        )

    # Ρουτίνα ελέγχου, εάν ένας υποψήφιος γονέας ή παιδί είναι εντός ορίων
    def in_limits(self, candidate, limits):
        self.candidate = candidate
        self.limits = limits

        # Επανάληψη για έλεγχο υποψήφιου γονέα ή παιδιού αν είναι εντός ορίων
        for i in range(len(limits)):
            # Αν ο υποψήφιος είναι εκτός ορίων επιστρέφει λάθος
            if candidate[i] < limits[i, 0] or candidate[i] > limits[i, 1]:
                return False
        return True

    # Evolution Strategy αλγόριθμος με επιλογή για πρόσθεση επιλεγμένων γονέων
    def evolution(
        self,
        graphArea,
        outputArea,
        fitness_var,
        limits,
        generations_num,
        dispersion,
        best_members,
        population_size,
    ):
        self.graphArea = graphArea
        self.outputArea = outputArea
        self.limits = limits
        self.generations_num = generations_num
        self.dispersion = dispersion
        self.best_members = best_members
        self.population_size = population_size

        best = None
        best_evaluation = 10000000000
        # Υπολογισμός αιθμού παιδιών
        children_num = int(population_size / best_members)
        # Αρχικοποίηση δημιουργούμενου Πληθυσμού
        created_population = list()

        # Επανάληψη για πρόσθεση Υποψηφίων Γονέων στον αρχικό πληθυσμό
        for _ in range(population_size):  # Το _ για μη ανάγκη δείκτη
            candidate_parent = None
            # Επανάληψη ενόσω ο υποψήφιος γονέας είναι εντός ή εκτός ορίων
            while candidate_parent is None or not self.in_limits(
                candidate_parent, limits
            ):
                # Αν δεν βρέθηκε, δημιουργία υποψήφιου γονέα μέσα στο όρια
                candidate_parent = limits[:, 0] + rand(len(limits)) * (
                    limits[:, 1] - limits[:, 0]
                )
                # Πρόσθεση στον πλυθυσμό
                created_population.append(candidate_parent)

        # Επανάληψη βάσει αριθμού γενεών
        for generation in range(generations_num):

            # Δημιουργία λίστας με τους υποψήφιους βάσει επιλεγμένου μοντέλου fitness
            success_list = []
            if fitness_var == "G":  # Gauss
                for c in created_population:
                    success_list.append(self.fitnessG(c))
            elif fitness_var == "R":  # Rastrigin
                for c in created_population:
                    success_list.append(self.fitnessR(c))
            else:  # Ackley
                for c in created_population:
                    success_list.append(self.fitnessA(c))

            # Κατάταξη βαθμολογιών σε αύξουσα σειρά με διπλή κλήση ταξινόμησης
            ordered_list = argsort(argsort(success_list))

            # Δημιουργία λίστας γονέων για την καλύτερη κατάταξη
            selected_parents = []
            # Επανάλληψη μέσω (enumerate) για επιστροφή απαρίθμησης της ταξινομιμένης λίστας
            for x, _ in enumerate(
                ordered_list
            ):  # Ανάγκη για δύο μεταβλητές οπότε x και _
                if ordered_list[x] < best_members:
                    selected_parents.append(x)  # Πρόσθεση επιλεγμένων γονέων

            # Δημιουργία λίστας παιδιών
            created_children = list()
            # Επανάληψη στους επιλεγμένους γονείς
            for i in selected_parents:

                # ΈΛεγχος αν αυτός ο γονέας είναι λύση και εκτύπωση δεδομένων
                if success_list[i] < best_evaluation:
                    best_population = created_population[i]
                    best_evaluation = success_list[i]

                    # Ορισμός παραμέτρων εκτύπωσης
                    generation_num = generation  # Αριθμός γενεών
                    parent_num_num = len(selected_parents)  # Γονείς
                    child_num = len(created_children)  # Πληθυσμός - (παιδιά) ανα γενιά
                    best_evaluation_num = max(success_list)  # Καλύτερη Αξιολόγηση

                    # Εκτύπωση
                    print(
                        "Γενιά: %d, Παιδιά: %d, f(%s), ΑΞΙΟΛΟΓΗΣΗ %f"
                        % (generation_num, child_num, best_population, best_evaluation)
                    )
                    # Εμφάνιση δεδομένων στο παραθυρικό περιβάλλον
                    buff = "Γενιά: %d, Παιδιά: %d, f(%s), ΑΞΙΟΛΟΓΗΣΗ %f" % (
                        generation_num,
                        child_num,
                        best_population,
                        best_evaluation,
                    )
                    outputArea.insert(END, buff + "\n")
                    outputArea.yview(END)

                    # Κλήση εμφάνισης διαγράμματος Rastrigin
                    if (
                        child_num > 0 and generation_num > 0
                    ):  # Εμφάνιση γραφήματος όταν υπάρχουν Παιδιά - Γονείς
                        self.show_plot(graphArea, generation_num, child_num, dispersion)

                    # Τερματισμός αν ο δημιουργούμενος πλυθυσμός είναι μεγαλύτερος απο τον ζητούμενο
                    if child_num > population_size:
                        created_population = created_children
                        return [best_population, best_evaluation]

                # Επανάληψη βάσει υπολογισμένου αριθμού παιδιών
                for _ in range(children_num):  # Το _ για μη ανάγκη δείκτη
                    new_child = None
                    # Επανάληψη ενόσω το δημιουργούμενο παιδί είναι εντός ή εκτός ορίων
                    while new_child is None or not self.in_limits(new_child, limits):
                        # Αν δεν βρέθηκε, δημιουργία παιδιού μέσα στα όρια
                        new_child = (
                            created_population[i] + randn(len(limits)) * dispersion
                        )
                        # Πρόσθεση στην λίστα παιδιών
                        created_children.append(new_child)

            # Αντικατάσταση πληθυσμού απο παιδιά
            created_population = created_children

        return [best_population, best_evaluation]

    # Gauss plot
    def Gauss_plot(self, graphArea):
        self.graphArea = graphArea

        # Μεταβλητή αρίθμησης για την δημιουργία Gauss γραφήματος
        global key
        key = 1

        # Υπολογισμός όρων της εξίσωσης Gauss
        mean = statistics.mean(Gxaxis)
        sd = statistics.stdev(Gxaxis)
        result = self.gauss_plot(Gxaxis, mean, sd)
        # Δημιουργία γραφήματος
        # Μέσω της globals αρίθμηση στο fig προσθέτωντας το key
        globals()[f"fig{key}"] = Figure(figsize=(6, 6), dpi=100)
        axis = globals()[f"fig{key}"].add_subplot(111)
        # axis = fig.add_subplot(111)
        # Δημιουργία plot
        axis.plot(Gxaxis, result)
        # Εμφάνιση τίτλων διαγράμματος
        axis.set_title("Gaussian Normal Distribution")

        return

    # Rastrigin plot
    def show_plot(self, graphArea, gen_num, child_num, dispersion):
        self.graphArea = graphArea
        self.gen_num = gen_num
        self.child_num = child_num
        self.dispersion = dispersion

        # Μεταβλητές αρίθμησης για την δημιουργία Rastrigin γραφημάτων
        global key
        key = key + 1
        # Υπολογισμός αριθμού γραφημάτων
        global cnt_graph
        cnt_graph = key

        # Εύρος εισόδου δειγμάτων ομοιόμορφα σε προσαυξήσεις dispersion
        Rxaxis = arange(0, gen_num, dispersion)
        Ryaxis = arange(0, child_num, dispersion)
        # Δημιουργία πλέγματος από τον άξονα
        x, y = meshgrid(Rxaxis, Ryaxis)
        # Υπολογισμός στόχων
        result = self.rastrigin_plot(x, y)
        # Δημιουργία γραφήματος με σχήμα jet color
        # Μέσω της globals αρίθμηση στο fig προσθέτωντας το key
        globals()[f"fig{key}"] = Figure(figsize=(6, 6), dpi=100)
        axis = globals()[f"fig{key}"].add_subplot(111, projection="3d")
        axis.plot_surface(x, y, result, cmap="jet")
        # Εμφάνιση τίτλων διαγράμματος
        axis.set_xlabel("Αριθμός Γενεών")
        axis.set_ylabel("Πληθυσμός ανά Γενιά")
        axis.set_zlabel("Διασπορά")
        axis.set_title("Rastrigin Graph - gen = " + str(gen_num))

        return

    def control(self, outputArea, graphArea):
        self.outputArea = outputArea
        self.graphArea = graphArea

        # Παράμετροι για την λειτουργία του εξελικτικού αλγόριθμου
        #
        # Σπόρος της γεννήτριας ψευδοτυχαίων αριθμών
        seed(1)

        # Μέγεθος δημιουργούμενου πληθυσμού - παιδιά
        str_num = self.t1.get()
        if len(str_num) == 0:
            population_size = 100
        else:
            population_size = int(str_num)

        # Αριθμός επιλεγμένων γονέων
        str_num = self.t2.get()
        if len(str_num) == 0:
            best_members = 20
        else:
            best_members = int(str_num)

        # Ορισμός συνολικών γενεών
        str_num = self.t3.get()
        if len(str_num) == 0:
            max_generations = 5000
        else:
            max_generations = int(str_num)

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

        # Ορισμός για την αρχική τιμή διασποράς κατανομής
        str_num = self.t6.get()
        if len(str_num) == 0:
            dispersion = 0.11
        else:
            dispersion = float(str_num)

        # Ορισμός για επιλογή του μοντέλου fitness
        fitness_var = self.t7.get()

        # Εμφάνιση λαθών ή ελάχιστων παραμέτρων στο παραθυρικό περιβάλλον
        if population_size == 0:
            buff = "ΤΟ ΜΕΓΕΘΟΣ ΔΗΜΙΟΥΡΓΟΥΜΕΝΟΥ ΠΛΗΘΥΣΜΟΥ ΠΡΕΠΕΙ ΝΑ ΕΧΕΙ ΤΙΜΗ > 0"
            outputArea.insert(END, buff + "\n")
            outputArea.yview(END)
            return -1

        if best_members == 0:
            buff = "O ΑΡΙΘΜΟΣ ΤΩΝ ΕΠΙΛΕΓΜΕΝΩΝ ΓΟΝΕΩΝ ΠΡΕΠΕΙ ΝΑ ΕΧΕΙ ΤΙΜΗ > 0"
            outputArea.insert(END, buff + "\n")
            outputArea.yview(END)
            return -1

        if max_generations == 0:
            buff = "O ΑΡΙΘΜΟΣ ΤΩΝ ΓΕΝΕΩΝ ΠΡΕΠΕΙ ΝΑ ΕΧΕΙ ΤΙΜΗ > 0"
            outputArea.insert(END, buff + "\n")
            outputArea.yview(END)
            return -1

        if r_min > -5.0:
            buff = "ΜΗ ΕΠΙΤΡΕΠΤΗ ΤΙΜΗ ΓΙΑ ΤΟ ΚΑΤΩ ΟΡΙΟ"
            outputArea.insert(END, buff + "\n")
            outputArea.yview(END)
            return -1

        if r_max < 5.0:
            buff = "ΜΗ ΕΠΙΤΡΕΠΤΗ ΤΙΜΗ ΓΙΑ ΤΟ ΑΝΩ ΟΡΙΟ"
            outputArea.insert(END, buff + "\n")
            outputArea.yview(END)
            return -1

        if dispersion <= 0.1:
            buff = "ΜΗ ΕΠΙΤΡΕΠΤΗ ΤΙΜΗ ΓΙΑ ΤΗΝ ΑΡΧΙΚΗ ΤΙΜΗ ΔΙΑΣΠΟΡΑΣ"
            outputArea.insert(END, buff + "\n")
            outputArea.yview(END)
            return -1

        if population_size % best_members != 0:
            buff = "Η ΔΙΑΙΡΕΣΗ ΠΛΗΘΥΣΜΟΥ ΠΡΟΣ ΓΟΝΕΙΣ ΠΡΕΠΕΙ ΝΑ ΕΧΕΙ ΥΠΟΛΟΙΠΟ 0"
            outputArea.insert(END, buff + "\n")
            outputArea.yview(END)
            return -1

        # Oρισμός πίνακα απο τις παραμέτρους ελάχιστου και μέγιστου ορίου
        limits = asarray([[r_min, r_max], [r_min, r_max]])

        global Gxaxis  # Μεταβλητή κοινής χρήσης για την εμφάνιση και την συνάρτηση fitness του Gauss
        Gxaxis = arange(r_min, r_max, dispersion)

        # Κλήση δημιουργίας Διαγραμμάτος Gauss για την εμφάνιση εισαγμένων ορίων
        self.Gauss_plot(graphArea)

        # Κλήση του αλγορίθμου αξιολόγησης
        best_pop, best_eval = self.evolution(
            graphArea,
            outputArea,
            fitness_var,
            limits,
            max_generations,
            dispersion,
            best_members,
            population_size,
        )
        print("\nΟΛΟΚΛΗΡΩΣΗ!")
        print("ΤΕΛΕΙΟ: f(%s) = %f" % (best_pop, best_eval))

        # Εισαγωγή όλων των δημιουργημένων διαγραμμάτων στόν καμβά
        # με σειρά απο το τελευταίο ως το πρώτο ώστε τελικά να εμφανιστούν
        # με την σειρά δημιουργίας τους.
        global cnt_graph
        k = cnt_graph
        first_graph = 1
        while k >= first_graph:
            graph = FigureCanvasTkAgg(globals()[f"fig{k}"], master=self.graphArea)
            graph.draw()
            graph.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=False)
            k = k - 1
        global key
        key = first_graph

        # Εμφάνιση δεδομένων στο παραθυρικό περιβάλλον
        buff = "ΟΛΟΚΛΗΡΩΣΗ!"
        outputArea.insert(END, buff + "\n")
        buff = "ΤΕΛΕΙΟ: f(%s) = %f" % (best_pop, best_eval)
        outputArea.insert(END, buff + "\n")
        outputArea.yview(END)

        return


window = Tk()
mywin = MyWindow(window)
window.title("Παράμετροι και Εκτέλεση της Εξελικτικής Στρατηγικής")
window.geometry("1450x670+10+10")

window.mainloop()
