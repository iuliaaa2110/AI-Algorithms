import os
import time
from copy import deepcopy
from queue import PriorityQueue
from State import State


class AStarOpt:

    def __init__(self, heuristic, start_matrix, robinet_x, robinet_y, canal_x, canal_y, timeout):
        """
        Obiectul de tip AStar primeste ca parametrii:
        ~ datele de intrare ale problemei:
            ~ euristica dorita
            ~ matricea initiala
            ~ coordonatele punctului de start (robinet_x, robinet_y)
            ~ coordonatele punctului de final (canal_x, canal_y)
        """

        self.timeout = timeout
        self.path = []
        self.heuristic = heuristic
        self.start_matrix = start_matrix
        self.robinet_x = robinet_x
        self.robinet_y = robinet_y
        self.canal_x = canal_x
        self.canal_y = canal_y
        self.closed = []
        self.open = PriorityQueue()
        self.path = []
        self.last_cost = 0
        # self.nr_ordine = [0]

    def calculate_F(self, state):
        """
        state.sum_cost == g == costul de pana in prezent
        Adaug la state.sum_cost euristica dorita

        •	Euristica admisibila1: calculeaza costul minim pana intr o stare care se afla fix la un pas
        distanta.
        •	Euristica admisibila2:  gaseste costul minim catre urmatorul “o” aflat in matrice.
        •	Euristica neadmisibila: costul maxim posibil de unde a ajuns apa pana la canal.
        Costum maxim al unui zid e 5, iar distanta minima ipotetica de la apa pana la canal e distanta euclidiana
        dintre cel mai apropiat "o" de canal si canal
        """
        if self.heuristic == "banala":
            return state.sum_cost

        if self.heuristic == "admisibila1":
            return state.sum_cost + state.one_step_forward_cost()

        if self.heuristic == "admisibila2":
            return state.sum_cost + state.next_o_cost()

        if self.heuristic == "neadmisibila":
            return state.sum_cost + state.best_o_dist * 5
        #
        # if self.heuristic == "neadmisibila":
        #     return state.sum_cost + state.getDistance()

    def Solve(self):

        """
        ~ startState este starea initiala a problemei (radacina arborelui)
        ~ initializez open cu startState
        ~ open este un Priority Queue cu tupluri de forma:
            (valoarea lui f = g + h, id-ul, starea/nodul)
        """
        t1 = time.time()

        startState = State(deepcopy(self.start_matrix), None, self.robinet_x, self.robinet_y,
                           self.canal_x, self.canal_y, 0)
        count = 0

        self.open.put((0, count, startState))

        while not self.path and self.open.qsize():

            """
            Cat timp nu am gasit solutia si inca am elemente in coada:
             ~ closestChild este elementul extras din coada open
             ~ closestChild.createChildren o sa imi completeze lista closestChild.children cu toate nodurile copii 
             ale nodului closestChild 
             ~ Parcurg copiii si pentru fiecare nod care nu are matricea intr o forma deja prezenta in lista closed, 
             verific daca nodul curent este stare finala:
                - daca da, atunci obtin solutia (calea de la radacina pana la el ) si opresc programul.
                - daca nodul nu este stare finala, ii calculez functia f si id ul si il adaug in coada open si 
                se continua programul
            """

            if round(1000*(time.time()-t1)) > self.timeout:
                return 'Timeout'

            closestChild = self.open.get()[2]

            if closestChild.isFinalState:
                t2 = time.time()
                self.path = (closestChild.getPath(), round(1000*(t2-t1)), count)
                break

            closestChild.createChildren()
            self.closed.append(closestChild.matrix)

            for child in closestChild.children:
                if child.matrix not in self.closed:
                    count += 1
                    child.id = count

                    self.open.put((self.calculate_F(child), count, child))

        if not self.path:
            print("Goal is not possible!")

        return self.path
