import os
from copy import deepcopy

# from AStarOptimizat import AStar
# from AStarOpt2 import AStar
from AStar import AStar
from AStarOpt2 import AStarOpt
from IDAStar import IDAStar
from State import isInRange
from UCS import UCS

heuristics = ['banala', 'admisibila1', 'admisibila2', 'neadmisibila']


def read(input_path):
    f = open(input_path)

    robinet_x, robinet_y = [int(x) for x in f.readline().split()]
    canal_x, canal_y = [int(x) for x in f.readline().split()]
    matrix = []

    while True:
        line = f.readline()

        if not line:
            break

        matrix.append([x for x in line[:(len(line) - 1)]])

    f.close()

    return robinet_x, robinet_y, canal_x, canal_y, matrix


def print_state(state, g):
    g.write('Sparg zidul de pe pozitia ' + str(state.current_x) + ' ' + str(state.current_y) + '\n')
    g.write('costul acestei mutari =' + str(state.cost) + '\n')
    g.write('cost total = ' + str(state.sum_cost) + '\n')
    g.write('nr ordine =' + str(state.id) + '\n')
    # g.write('best o dist =' + str(state.best_o_dist) + '\n')

    for j in range(len(state.matrix)):
        g.write(str(state.matrix[j]) + '\n')

    g.write('\n')


def print_solution(path, g):
    g.write('Lungimea drumului = ' + str(len(path)) + '\n\n\n')

    for i in range(0, len(path)):
        print_state(path[i], g)

    g.write('\n')

def print_paths(paths, g):
    for i in range(len(paths)):
        g.write('\n\n\n\n' + 'Solutia ' + str(i + 1) + '\n\n')
        g.write('Timp de executie = ' + str(paths[i][1]) + ' ms\n')
        g.write('Nr total de noduri calculate =' + str(paths[i][2]) + '\n')

        print_solution(paths[i][0], g)

    if len(paths) < solutions_number:
        g.write('Solutia' + str(len(paths) + 1) + '\n\nTimeout!!')


def call_AStarOpt(output_file):
    """
    ~ Deschid fisierul
    ~ Verific datele de intrare
    ~ Creez obiectul de tip AStarOptimal
    ~ Apelez functia Solve
    ~ Afisez solutia

    """

    g = open((output_folder + '/' + output_file), 'w')

    if not isInRange(matrix, robinet_x, robinet_y) or not isInRange(matrix, canal_x, canal_y):
        g.write('Datele de input sunt gresite. Problema nu are solutii')
    else:
        for heuristic in heuristics:
            g.write('\n\n\n' + heuristic + '\n\n')

            a = AStarOpt(heuristic, deepcopy(matrix), robinet_x, robinet_y, canal_x, canal_y, timeout)
            path = a.Solve()

            if path == 'Timeout':
                g.write(path)
            else:
                g.write('Timp de executie = ' + str(path[1]) + ' ms\n')
                g.write('Nr total de noduri calculate =' + str(path[2]) + '\n')

                print_solution(path[0], g)

            g.write('\n\n\n\n ______________________________________________________ \n\n\n\n')

    g.close()


def call_AStar(output_file):
    """
    AStar
    ~ Deschid fisierul
    ~ Verific datele de intrare
    ~ Creez obiectul de tip AStar
    ~ Apelez functia Solve
    ~ Afisez solutia

    """
    g = open((output_folder + '/' + output_file), 'w')

    if not isInRange(matrix, robinet_x, robinet_y) or not isInRange(matrix, canal_x, canal_y):
        g.write('Datele de input sunt gresite. Problema nu are solutii')
    else:
        g.write('AStar\n')

        for heuristic in heuristics:
            g.write('\n\n\n' + heuristic + '\n\n')

            a = AStar(heuristic, deepcopy(matrix), robinet_x, robinet_y, canal_x, canal_y, timeout)
            paths = a.Solve(solutions_number)

            print_paths(paths, g)

            g.write('\n\n\n\n ______________________________________________________ \n\n\n\n')

    g.close()


def call_UCS(output_file):
    """
    ~ Deschid fisierul
    ~ Verific datele de intrare
    ~ Creez obiectul de tip UCS
    ~ Apelez functia Solve
    ~ Afisez solutia

    """
    g = open((output_folder + '/' + output_file), 'w')

    if not isInRange(matrix, robinet_x, robinet_y) or not isInRange(matrix, canal_x, canal_y):
        g.write('Datele de input sunt gresite. Problema nu are solutii')
    else:
        a = UCS(deepcopy(matrix), robinet_x, robinet_y, canal_x, canal_y, timeout)
        paths = a.Solve(solutions_number)

        print_paths(paths, g)

        g.write('\n\n\n\n ______________________________________________________ \n\n\n\n')

    g.close()

def call_IDAStar(output_file):
    """
    ~ Deschid fisierul
    ~ Verific datele de intrare
    ~ Creez obiectul de tip IDAStar
    ~ Apelez functia Solve
    ~ Afisez solutia

    """

    g = open((output_folder + '/' + output_file), 'w')

    if not isInRange(matrix, robinet_x, robinet_y) or not isInRange(matrix, canal_x, canal_y):
        g.write('Datele de input sunt gresite. Problema nu are solutii')
    else:
        for heuristic in heuristics:
            g.write('\n\n\n' + heuristic + '\n\n')

            idaStar = IDAStar(heuristic, deepcopy(matrix), robinet_x, robinet_y, canal_x, canal_y, timeout)
            paths = idaStar.Solve(solutions_number)

            if paths == "Nu exista solutii!":
                print(paths)
            else:
                print_paths(paths, g)

                g.write('\n\n\n\n ______________________________________________________ \n\n\n\n')

    g.close()


if __name__ == '__main__':
    """
      ~ se cer in linia de comanda calea catre folderul ce contine fisierele de intrare
      si catre folderul ce va contine fisierele de iesire
      ~ daca folderul de iesire dat nu exista, atunci este creeat
      ~ se mai cere in linia de comanda si numarul de solutii dorite
      ~ Sunt apoi parcurse fisierele de intrare si pentru fiecare in parte se creeaza 4 fisiere de iesire 
      (cate unul pentru fiecare algoritm)
      
    """

    print("Type the path for the input folder")
    input_folder = input()

    print("Type the path for the output folder")
    output_folder = input()

    print("Type the number of solutions you wanna see")
    solutions_number = int(input())

    print("Timeout:")
    timeout = int(input())

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    for input_file in os.listdir(input_folder):
        """
            Citesc datele din fisierul curent
            Deschid fisierul de output corespunzator
            Si pentru fiecare algoritm in parte abordez fiecare euristica si aplic:
            ~ citire
            ~ rezolvare
            ~ afisare
        """
        output_AStar = input_file[:len(input_file) - 3] + '__AStar.out'
        output_AStarOpt = input_file[:len(input_file) - 3] + '__AStarOptimal.out'
        output_UCS = input_file[:len(input_file) - 3] + '__UCS.out'
        output_IDAStar = input_file[:len(input_file) - 3] + '__IDAStar.out'

        robinet_x, robinet_y, canal_x, canal_y, matrix = read(input_folder + "/" + input_file)

        call_AStar(output_AStar)
        call_AStarOpt(output_AStarOpt)
        call_UCS(output_UCS)
        call_IDAStar(output_IDAStar)
