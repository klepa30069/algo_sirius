"""
Задача 8:
Реализовать венгерский алгоритм для решения задач комбинаторной оптимизации через графы.

Задача венгерского алгоритма решается на матрицах и на графах смысла не имеет,
так как задача самого алгоритма сопоставить один параметр с другим.
То есть на графах - это получается не связные между собой компоненты,
которые имеют по две связные вершины между собой.

Функция reduce_matrix по времени получилась примерно O(n^2) по памяти O(1).
Функция find_zeros по времени получилась примерно O(n^2) по памяти O(n^2).
Функция find_min_uncovered по времени получилась примерно O(n^2) по памяти O(1).
Функция hungarian по времени получилась примерно O(n^3) по памяти O(n^2).
Функция in_out по времени получилась примерно O(n) по памяти O(n^2).

Итого: вся программа по времени получилось примерно O(n^3) по памяти примерно O(n^2).
"""


def reduce_matrix(graf):
    for i in range(len(graf)):
        min_val = min(graf[i])
        for j in range(len(graf[i])):
            graf[i][j] -= min_val
    for j in range(len(graf[0])):
        min_val = graf[0][j]
        for i in range(1, len(graf)):
            min_val = min(min_val, graf[i][j])
        for i in range(len(graf)):
            graf[i][j] -= min_val
    return graf


def find_zeros(graf):
    marked = [[0 for _ in range(len(graf[0]))] for _ in range(len(graf))]
    row_covered = [False] * len(graf)
    col_covered = [False] * len(graf[0])
    for i in range(len(graf)):
        for j in range(len(graf[0])):
            if graf[i][j] == 0 and not row_covered[i] and not col_covered[j]:
                marked[i][j] = 1
                row_covered[i] = True
                col_covered[j] = True
    return marked, row_covered, col_covered


def find_min_uncovered(graf, row_covered, col_covered):
    min_val = None
    for i in range(len(graf)):
        for j in range(len(graf[0])):
            if not row_covered[i] and not col_covered[j]:
                if min_val is None:
                    min_val = graf[i][j]
                else:
                    min_val = min(min_val, graf[i][j])
    return min_val


def hungarian(graf):
    matrix = [row[:] for row in graf]
    n = len(matrix)
    matrix = reduce_matrix(matrix)
    marked, row_covered, col_covered = find_zeros(matrix)
    assignment_count = sum(sum(row) for row in marked)
    while assignment_count != n:
        min_uncovered = find_min_uncovered(matrix, row_covered, col_covered)
        for i in range(n):
            for j in range(n):
                if not row_covered[i] and not col_covered[j]:
                    matrix[i][j] -= min_uncovered
                elif row_covered[i] and col_covered[j]:
                    matrix[i][j] += min_uncovered
        matrix = reduce_matrix(matrix)
        marked, row_covered, col_covered = find_zeros(matrix)
        assignment_count = sum(sum(row) for row in marked)
    assignments = []
    for i in range(n):
        for j in range(n):
            if marked[i][j] == 1:
                assignments.append((i, j, graf[i][j]))
    return assignments


def in_out():
    v = int(input('Введи количество параметров: '))
    graf = []
    for i in range(v):
        graf.append(list(map(int, input(f'Введи {i + 1} строчку матрицы стоимости (через \', \'): ').split(', '))))
    distances = hungarian(graf)
    total = 0
    for i in distances:
        print(f'Параметр {i[1] + 1} связан с человеком {i[0] + 1} по стоимости {i[2]}')
        total += i[2]
    print('Общая стоимость:', total)


if __name__ == "__main__":
    in_out()

"""
Вывод:

Введи количество параметров: 3
Введи 1 строчку матрицы стоимости (через ', '): 250, 400, 350
Введи 2 строчку матрицы стоимости (через ', '): 400, 600, 350
Введи 3 строчку матрицы стоимости (через ', '): 200, 400, 250
Параметр 2 связан с человеком 1 по стоимости 400
Параметр 3 связан с человеком 2 по стоимости 350
Параметр 1 связан с человеком 3 по стоимости 200
Общая стоимость: 950
"""
