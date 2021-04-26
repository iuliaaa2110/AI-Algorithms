from copy import deepcopy
from queue import Queue, PriorityQueue

vx = [-1, 0, 0, 1]
vy = [0, -1, 1, 0]

vcx = [-1, -1, -1, 0, 1, 1,  1,  0]
vcy = [-1,  0,  1, 1, 1, 0, -1, -1]


def isInRange(matrix, x, y):
    """
    Atunci cand ma deplasez in matrice, am grija sa nu depasesc marginile acesteia
    :param x, :param y: coordonatele punctului in care vreau sa ajung
    :return: True daca pozitia e valida, False altfel
    """
    if 0 <= x < len(matrix) and 0 <= y < len(matrix[0]):
        return True
    return False


def calculate_cost(matrix, x, y):
    """
    Calculez cat costa sa distrug zidul curent.
    :return:
    """
    if matrix[x][y] != '#':
        return 0

    s = 1
    for i in range(0, 8):
        neighbour_x = x + vcx[i]
        neighbour_y = y + vcy[i]

        if isInRange(matrix, neighbour_x, neighbour_y):
            if matrix[neighbour_x][neighbour_y] == '#':
                s += 1
    # self.cost = s
    return s


class State(object):

    def __init__(self, matrix, parent, current_x, current_y, final_x, final_y, id=0):

        """
        :param matrix: matricea problemei
        :param parent: nodul tata
        :param current_x, :param current_y:  coordonatele zidului daramat in aceasta stare
        :param final_x:, :param final_y: coordonatele punctului in care trebuie sa ajunga apa
        :param id: numarul de ordine al nodului
        sum_cost: costul adunat de la starea initiala pana la cea curenta
        cost: costul individual al mutarii curente (cel descris in cerinta problemei)
        neighbours_coord: coordonatele urmatoarelor mutari (deplasarea in matrice) (copiilor)
        best_o_dist: e doar initializat aici. Dar isi poate modifica valoarea dupa ce apa se imprastie in toate
        pozitiile vecine 'o' la daramarea zidului, best_o_dist
        reprezinta distanta cea mai mica de la unul din 'o' urile unde a ajuns apa si pana la punctul final
        (unde trebuie sa ajunga)
        """

        self.final_x = final_x
        self.final_y = final_y
        self.current_x = current_x
        self.current_y = current_y
        self.parent = parent
        self.matrix = matrix
        self.cost = calculate_cost(matrix, current_x, current_y)
        self.best_o_dist = self.getDistance(current_x, current_y)

        if not self.parent:
            self.sum_cost = self.cost
            self.neighbours_coord = []
            self.isFinalState = False
        else:
            self.neighbours_coord = [s for s in self.parent.neighbours_coord if s != (
                current_x, current_y)]  # deepcopy(self.parent.neighbours_coord.remove((current_x, current_y)))
            self.sum_cost = self.parent.sum_cost + self.cost
            self.isFinalState = self.parent.isFinalState

        self.id = id
        self.children = []

        self.fill(self.current_x, self.current_y, deepcopy(self.neighbours_coord))

    def getDistance(self, x, y):
        """
        :return: nr ul minim de pasi din locul curent la destinatie
        """
        return abs(self.final_x - x) + abs(self.final_y - y)

    def fill(self, x, y, neighbours):

        """
        Functie care are rolul de a raspandi apa prin toate pozitiile vecine de tip 'o'
        :param x, :param y: coordonatele pozitiei unde tocmai a ajuns apa
        :param neighbours: coordonatele vecine valide ale intregii balti, dupa ce e umpluta
        """

        self.matrix[x][y] = 'i'

        if x == self.final_x and y == self.final_y:
            self.isFinalState = True

        d = self.getDistance(x, y)

        if d < self.best_o_dist:
            self.best_o_dist = d

        for i in range(0, 4):

            neighbour_x = x + vx[i]
            neighbour_y = y + vy[i]

            if isInRange(self.matrix, neighbour_x, neighbour_y):
                if self.matrix[neighbour_x][neighbour_y] == 'o':
                    self.fill(neighbour_x, neighbour_y, neighbours)

                elif self.matrix[neighbour_x][neighbour_y] == '#':
                    if (neighbour_x, neighbour_y) not in neighbours:
                        neighbours.append((neighbour_x, neighbour_y))

        self.neighbours_coord = neighbours

        # return neighbours

    def createChildren(self):
        """
        :param nr_ordine:
        :return: copiii nodului
        """

        if not self.children:

            for x, y in self.neighbours_coord:
                new_matrix = deepcopy(self.matrix)
                child = State(new_matrix, self, x, y, self.final_x, self.final_y)

                self.children.append(child)

        return self.children

    def one_step_forward_cost(self):
        best = None

        for neighbour_x, neighbour_y in self.neighbours_coord:

            cost = calculate_cost(self.matrix, neighbour_x, neighbour_y)

            if best is None:
                best = cost

            if cost < best:
                best = cost

        return best

    def next_o_cost(self):
        """
        O funcie foarte asemanatoare cu AStar care ca imi gaseste costul minim pana la o casuta "o",
        """
        neighbours = deepcopy(self.neighbours_coord)
        matrix = deepcopy(self.matrix)

        queue = PriorityQueue()

        for x, y in neighbours:
            queue.put((0, x, y))

        while True and not queue.empty():
            cost, x, y = queue.get()

            if matrix[x][y] == 'o':
                return cost
            else:
                # nu are cum sa fie decat "#", nu ajunge niciodata cu "i" aici
                for i in range(4):
                    neighbour_x = x + vx[i]
                    neighbour_y = y + vy[i]

                    if isInRange(matrix, neighbour_x, neighbour_y):
                        if matrix[neighbour_x][neighbour_y] != 'i':
                            current_cost = calculate_cost(matrix, neighbour_x, neighbour_y)
                            new_cost = cost + current_cost
                            queue.put((new_cost, neighbour_x, neighbour_y))

            matrix[x][y] = 'i'

        return 0

    def getPath(self):
        l = []
        nod = self
        while nod is not None:
            l.insert(0, nod)
            nod = nod.parent
        return l
