"""
Задача 6:
Дана информация о времени заезда и отъезда посетителей отеля. Необходимо определить,
в какой день посетителей в отеле единомоменто находилось больше всего.
Пример входных данных (один элемент данного листа – кортеж, содержащий дату заезда
отъезда одного посетителя): [(“2024-09-15”, “2024-09-15”), (“2024-09-14”, “2024-09-21”)]

Функция max_guest по времени получилась примерно O(n) по памяти O(1).
Функция in_out по времени получилась примерно O(n) по памяти O(1).
"""
from datetime import datetime, timedelta
from enum import IntEnum


class TypeDate(IntEnum):
    IN = 1
    OUT = -1


def max_guest(dates):
    dates.sort()
    max_count = 0
    guest = 0
    max_date_in = None
    max_date_out = None
    flags = False
    for date, type in dates:
        guest += type.value
        if max_count < guest:
            max_count = guest
            max_date_in = date
            flags = True
        if flags and type == TypeDate.OUT:
            max_date_out = date - timedelta(days=1)
            flags = False
    return (max_date_in, max_date_out, max_count)


def in_out():
    n = int(input('Введите количество посетителей: '))
    dates = list()
    for _ in range(n):
        check_in_date, check_out_date = input(
            'Введите дату заезда и отъезда посетителя отеля (в формате YYYY-MM-DD): ').split(' ')
        dates.append((datetime.strptime(check_in_date, "%Y-%m-%d"), TypeDate.IN))
        dates.append((datetime.strptime(check_out_date, "%Y-%m-%d") + timedelta(days=1), TypeDate.OUT))
    max_date_in, max_date_out, max_count = max_guest(dates)
    print('В период с', max_date_in.strftime("%Y-%m-%d"), 'до', max_date_out.strftime("%Y-%m-%d"),
          'было максимальное количество посетителей:', max_count)


if __name__ == "__main__":
    in_out()

"""
Вывод:

Введите количество посетителей: 2
Введите дату заезда и отъезда посетителя отеля (в формате YYYY-MM-DD): 2024-09-15 2024-09-15
Введите дату заезда и отъезда посетителя отеля (в формате YYYY-MM-DD): 2024-09-14 2024-09-21
В период с 2024-09-15 до 2024-09-15 было максимальное количество посетителей: 2
"""
