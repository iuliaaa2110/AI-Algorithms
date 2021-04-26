import time
from copy import deepcopy

from State import State
# from main import print_solution


class IDAStar():
    def __init__(self, heuristic, start_matrix, robinet_x, robinet_y, canal_x, canal_y, timeout):
        """
        Obiectul de tip AStar primeste ca parametrii:
        ~ datele de intrare ale problemei:
            ~ euristica dorita
            ~ matricea initiala
            ~ coordonatele punctului de start (robinet_x, robinet_y)
            ~ coordonatele punctului de final (canal_x, canal_y)
        """

        self.paths = []
        self.heuristic = heuristic
        self.start_matrix = start_matrix
        self.robinet_x = robinet_x
        self.robinet_y = robinet_y
        self.canal_x = canal_x
        self.canal_y = canal_y
        self.timeout = timeout

    def calculate_F(self, state):
        """
        state.sum_cost == costul de pana la aceasta stare
        Adaug la state.sum_cost euristica dorita
        """
        if self.heuristic == "banala":
            return state.sum_cost

        if self.heuristic == "admisibila1":
            return state.sum_cost + state.one_step_forward_cost()

        if self.heuristic == "admisibila2":
            return state.sum_cost + state.next_o_cost()

        if self.heuristic == "neadmisibila":
            return state.sum_cost + state.best_o_dist * 5

    def Solve(self, solutions_number):

        t1 = time.time()
        count = 0

        startState = State(deepcopy(self.start_matrix), None, self.robinet_x, self.robinet_y,
                           self.canal_x, self.canal_y, 0)
        # print()
        threshold = self.calculate_F(startState)

        while True:
            solutions_number, result, count = self.reach(startState, threshold, solutions_number, t1, count)

            if result == 'done':
                return self.paths

            if result == float('inf'):
                return "Nu exista solutii!"

            threshold = result

    def reach(self, currentState, threshold, solutions_number, t1, count):

        f = self.calculate_F(currentState)

        if f > threshold:
            return solutions_number, f, count

        if round(1000 * (time.time() - t1)) > self.timeout:
            return 0, 'done', count

        if currentState.isFinalState and f == threshold:
            t2 = time.time()
            self.paths.append((currentState.getPath(),  round(1000 * (t2 - t1)), count))
            solutions_number -= 1

            if not solutions_number:
                return 0, 'done', count

        currentState.createChildren()
        minim = float('inf')

        for child in currentState.children:
            count += 1
            child.id = count
            solutions_number, result, count = self.reach(child, threshold, solutions_number, t1, count)

            """
            daca result == 'done', inseamna ca a intrat pe if ul de la linia 78 si avem un rezultat
            """
            if result == 'done':
                return 0, 'done', count

            if result < minim:
                minim = result

        return solutions_number, minim, count

