import os
from copy import deepcopy
from queue import PriorityQueue
from State import State
import time


class UCS:

    def __init__(self, start_matrix, robinet_x, robinet_y, canal_x, canal_y, timeout):
        """
        Obiectul de tip AStar primeste ca parametrii:
        ~ datele de intrare ale problemei:
            ~ euristica dorita
            ~ matricea initiala
            ~ coordonatele punctului de start
            ~ coordonatele punctului de final
        """

        self.paths = []
        self.start_matrix = start_matrix
        self.robinet_x = robinet_x
        self.robinet_y = robinet_y
        self.canal_x = canal_x
        self.canal_y = canal_y
        self.open = PriorityQueue()
        self.timeout = timeout
        # self.nr_ordine = [0]

    def Solve(self, solutions_number):

        """
        ~ startState este starea initiala a problemei (radacina arborelui)
        ~ initializez open cu startState
        ~ open este un Priority Queue de tupluri de forma:
            (valoarea euristica, id-ul, starea/nodul)
        """

        t1 = time.time()

        startState = State(deepcopy(self.start_matrix), None, self.robinet_x, self.robinet_y,
                           self.canal_x, self.canal_y, 0)
        count = 0

        self.open.put((0, count, startState))

        while self.open.qsize():

            """
            Cat timp nu am gasit solutia si inca am elemente in coada:
             ~ closestChild este elementul extras din coada open
             ~ closestChild.createChildren o sa imi completeze lista closestChild.children cu toate nodurile copii 
             ale nodului closestChild 
             ~ Parcurg copiii si pentru fiecare nod verific daca nodul curent este stare finala:
                - daca da, atunci obtin solutia (calea de la radacina pana la el ) si o adaug la paths si scad 
                solutions_number. Daca solutions_number a ajuns la 0 opresc programul, altfel continua.
                - daca nodul nu este stare finala, il adaug in coada open cu suma adunata pana la ea (fara costul ei)
                si se continua programul
            """

            if round(1000*(time.time()-t1)) > self.timeout:
                break

            closestChild = self.open.get()[2]

            if closestChild.isFinalState:
                t2 = time.time()

                self.paths.append((closestChild.getPath(), round(1000 * (t2 - t1)), count))
                solutions_number -= 1

                if not solutions_number:
                    break

            closestChild.createChildren()

            for child in closestChild.children:
                count += 1
                child.id = count

                self.open.put((child.sum_cost, count, child))

        if not self.paths:
            print("Goal is not possible!")

        return self.paths
