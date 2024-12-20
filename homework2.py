"""
Задача 2:
Будем использовать упрощенную версию формулы релевантности - линейную комбинацию
признаков. Формула релевантности задается n параметрами (a_1, а_2, ..., а_n), а каждый
объект описывается n числовыми признаками (f_1, f_2, ..., f_n). Таким образом, релевантность
определяется по формуле:
relevance = сумма (a_i * f_i) по i = 1 ... n
У некоторых объектов будут меняться некоторые признаки. Необходимо находить самые
релевантные объекты (с наибольшим значением формулы релевантности).

Формат ввода
В первой строке входных данных записано одно целое число n (1 <= n <= 100) - количество
параметров в формуле ранжирования.
Вторая строка содержит n целых чисел а_i (0 <= a_i <= 10^8).
В третьей строке входных данных записано одно целое число d (10 <= d <= 100 000,
n * d <= 100 000) - количество объектов для ранжирования. Далее в d строках записано по n
целых чисел f_{i, j} (0 <= f_{i, j} <= 10^8) - числовые признаки i-гo объекта.
Следующая строка содержит одно целое число q (1 <= q <= 100 000) - количество запросов к
системе ранжирования. Следующие q строк описывают запросы. Запрос на выдачу самых
релевантных объектов задается парой 1 k (1 <= k <= 10). Запрос на изменение значения
признака объекта задается четверкой 2 i j v (1 <= i <= d, 1 <= j <= n, 0 <= v <= 10^8) и
означает, что j-й признак у i-го объекта становится равным v.

Формат вывода
После каждого запроса первого типа выведите в одну строку порядковые номера k самых
релевантных документов в порядке убывания релевантности (числа следует разделять
одиночными пробелами). Гарантируется, что все документы в любой момент времени имеют
различные значения релевантности

Пример:
Входные данные
n = 2
a = 1 100
d = 10
1 2
2 1
3 1
4 1
5 1
6 1
7 1
8 1
9 1
10 1
q = 4
1 2
1 10
2 4 1 1000
1 10
Результат
1 10
1 10 9 8 7 6 5 4 3 2
4 1 10 9 8 7 6 5 3 2

Функция quick_sort получилась по времени примерно O(d * log d) по памяти примерно O(log d).
Функция binary_search получилась по времени примерно O(log d) по памяти примерно O(log d).
Функция in_out получилась по времени примерно O(n * (d + q)) по памяти примерно O(n * d + 3 * d + n + 4).
Итого: вся программа по времени получилось примерно O(n * (d + q) + d * log d + log d) по памяти примерно O(n * d + 3 * d + n + 2 * log d + 4).
"""
from random import randint


def binary_search(arr, low, high, data):
    mid = -1
    while low <= high:
        mid = low + (high - low) // 2
        if arr[mid] == data:
            return mid
        elif arr[mid] > data:
            low = mid + 1
        else:
            high = mid - 1
    return mid


def quick_sort(array, index, left, right):
    if right - left > 1:
        i_pivot = randint(left, right)
        pivot = array[i_pivot]
        array[right], array[i_pivot] = array[i_pivot], array[right]
        index[right], index[i_pivot] = index[i_pivot], index[right]
        i_pivot = right
        right = right - 1
        while right - left != -1:
            while array[left] >= pivot and right - left != -1:
                left += 1
            while array[right] <= pivot and right - left != -1:
                right += -1
            if right < left:
                array[i_pivot], array[left] = array[left], array[i_pivot]
                index[i_pivot], index[left] = index[left], index[i_pivot]
            else:
                array[left], array[right] = array[right], array[left]
                index[left], index[right] = index[right], index[left]
        quick_sort(array, index, 0, right)
        quick_sort(array, index, left, i_pivot)
    return (array, index)


def in_out():
    n = int(input('Введите количество параметров ранжирования: '))
    a = list(map(int, input('Введите ' + str(n) + ' целых чисел через пробел: ').split(' ')))
    d = int(input('Введите количество объектов для ранжирования: '))
    f = list()
    relevance_data = list()
    relevance_index = list()
    for i in range(d):
        f.append(list(map(int, input('Введите ' + str(n) + ' целых чисел через пробел: ').split(' '))))
        relevance_data.append(0)
        for j in range(n):
            relevance_data[i] += a[j] * f[i][j]
        relevance_index.append(i + 1)
    relevance_data, relevance_index = quick_sort(relevance_data, relevance_index, 0, len(relevance_data) - 1)
    q_n = int(input('Введите количество запросов к системе ранжирования: '))
    for i in range(q_n):
        q = list(map(int, input('Введите запрос состоящий из целых чисел через пробел: ').split(' ')))
        if q[0] == 1:
            print(q[1], 'самых релевантных документов:', end=' ')
            for j in range(q[1]):
                print(relevance_index[j], end=' ')
            print()
        elif q[0] == 2:
            rel_i = relevance_index.index(q[1])
            new_rel = relevance_data[rel_i] - (a[q[2] - 1] * f[q[1] - 1][q[2] - 1]) + (a[q[2] - 1] * q[3])
            relevance_data.pop(rel_i)
            relevance_index.pop(rel_i)
            f[q[1] - 1][q[2] - 1] = q[3]
            mind = binary_search(relevance_data, 0, len(relevance_data) - 1, new_rel)
            relevance_data.insert(mind, new_rel)
            relevance_index.insert(mind, q[1])


if __name__ == "__main__":
    in_out()

"""
Вывод:

Введите количество параметров ранжирования: 2
Введите 2 целых чисел через пробел: 1 100
Введите количество объектов для ранжирования: 10
Введите 2 целых чисел через пробел: 1 2
Введите 2 целых чисел через пробел: 2 1
Введите 2 целых чисел через пробел: 3 1
Введите 2 целых чисел через пробел: 4 1
Введите 2 целых чисел через пробел: 5 1
Введите 2 целых чисел через пробел: 6 1
Введите 2 целых чисел через пробел: 7 1
Введите 2 целых чисел через пробел: 8 1
Введите 2 целых чисел через пробел: 9 1
Введите 2 целых чисел через пробел: 10 1
Введите количество запросов к системе ранжирования: 4
Введите запрос состоящий из целых чисел через пробел: 1 2
2 самых релевантных документов: 1 10 
Введите запрос состоящий из целых чисел через пробел: 1 10
10 самых релевантных документов: 1 10 9 8 7 6 5 4 3 2 
Введите запрос состоящий из целых чисел через пробел: 2 4 1 1000
Введите запрос состоящий из целых чисел через пробел: 1 10
10 самых релевантных документов: 4 1 10 9 8 7 6 5 3 2 
"""
