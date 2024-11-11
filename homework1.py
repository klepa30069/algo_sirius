"""
Задача 1:
Сделать реверс односвязного списка.

Пример:
Входные данные: 1, 2, 3, 4, 5
Результат: 5, 4, 3, 2, 1

Функция reverse по времени получилась примерно O(n^2) по памяти O(1).
Функция reverse_function по времени получилась примерно O(n^2) по памяти O(1).
Функция reverse_quik по времени получилась примерно O(n) по памяти O(1).
Функция reverse_recursive по времени получилась примерно O(n) по памяти O(1).
"""


class Node:
    def __init__(self, data):
        self.__data = data
        self.__next = None

    def get_data(self):
        return self.__data

    def get_next(self):
        return self.__next

    def set_data(self, data):
        self.__data = data

    def set_next(self, next):
        self.__next = next


class LinkedList:
    def __init__(self):
        self.__head = None
        self.__size = 0

    def get_head(self):
        return self.__head

    def get_size(self):
        return self.__size

    def get_last(self):
        iteration = self.__head
        if iteration is None:
            return None
        while iteration.get_next() is not None:
            iteration = iteration.get_next()
        return iteration

    def __get_last_rec(self, node):
        if node.get_next() is None:
            return node
        return self.__get_last_rec(node.get_next())

    def get_last_rec(self):
        if self.__head is None:
            return None
        return self.__get_last_rec(self.__head)

    def add(self, data):
        new_node = Node(data)
        if self.__head is None:
            self.__head = new_node
        else:
            last = self.get_last()
            last.set_next(new_node)
        self.__size += 1

    def __print_rec(self, node):
        print(node.get_data(), end=' ')
        if node.get_next() is not None:
            return self.__print_rec(node.get_next())
        else:
            print()

    def print_rec(self):
        if self.__head is not None:
            self.__print_rec(self.__head)

    def get_nth_elem(self, n):
        iteration = None
        if 0 <= n < self.__size:
            iteration = self.__head
            for i in range(n):
                iteration = iteration.get_next()
        return iteration

    def insert(self, data, n):
        if n < self.__size:
            iteration = self.get_nth_elem(n - 1)
            new_node = Node(data)
            if iteration is not None:
                new_node.set_next(iteration.get_next())
                iteration.set_next(new_node)
            else:
                new_node.set_next(self.__head)
                self.__head = new_node
            self.__size += 1
        else:
            # TODO: think about 5 as element add on 12 index
            self.add(data)

    def delete(self, n):
        if n < self.__size:
            iteration = self.get_nth_elem(n - 1)
            if iteration is not None:
                iteration.set_next(iteration.get_next().get_next())
            else:
                self.__head = self.__head.get_next()
            self.__size -= 1

    def reverse(self):
        iteration_first = self.__head
        for i in range(self.__size // 2):
            iteration_last = iteration_first
            for j in range(self.__size - i * 2 - 1):
                iteration_last = iteration_last.get_next()
            t = iteration_first.get_data()
            iteration_first.set_data(iteration_last.get_data())
            iteration_last.set_data(t)
            iteration_first = iteration_first.get_next()

    def pop(self):
        if self.__size > 0:
            new_node = self.get_nth_elem(self.__size - 2)
            result = new_node.get_next().get_data()
            new_node.set_next(None)
            self.__size -= 1
            return result
        return None

    def reverse_function(self):
        n = self.__size - 1
        for i in range(n):
            self.insert(self.pop(), i)

    def reverse_quik(self):
        previous = None
        iteration = self.__head
        while iteration is not None:
            next_node = iteration.get_next()
            iteration.set_next(previous)
            previous = iteration
            iteration = next_node
        self.__head = previous

    def __reverse(self, iteration, previous):
        if iteration is None:
            return previous
        next_node = iteration.get_next()
        iteration.set_next(previous)
        return self.__reverse(next_node, iteration)

    def reverse_recursive(self):
        self.__head = self.__reverse(self.__head, None)


if __name__ == "__main__":
    l = LinkedList()
    print('New LinkedList:', l.get_size(), l.get_head())
    l.add(0)
    print('Add 0 into LinkedList:', l.get_size(), l.get_head(), l.get_head().get_data())
    l.add(1)
    print('Add 1 into LinkedList:', l.get_size(), l.get_head(), l.get_last().get_data(), l.get_last_rec().get_data())
    print('Print LinkedList:')
    l.print_rec()
    l.insert(2, 1)
    print('Insert 2 in 1 into LinkedList:', l.get_size())
    l.print_rec()
    l.insert(4, 0)
    print('Insert 4 in 0 into LinkedList:', l.get_size())
    l.print_rec()
    l.insert(21, 12)
    print('Insert 21 in 12 into LinkedList:', l.get_size())
    l.print_rec()
    l.reverse()
    print('Reverse LinkedList:', l.get_size())
    l.print_rec()
    l.insert(12, 21)
    print('Insert 12 in 21 into LinkedList:', l.get_size())
    l.print_rec()
    l.reverse_function()
    print('Reverse with function LinkedList:', l.get_size())
    l.print_rec()
    print('Get 3th element into LinkedList:', l.get_nth_elem(3), l.get_nth_elem(3).get_data())
    print('Get 25th element into LinkedList:', l.get_nth_elem(25))
    l.delete(3)
    print('Delete 3th element into LinkedList:', l.get_size())
    l.print_rec()
    print('Pop into LinkedList:', l.pop())
    l.print_rec()
    l.reverse_quik()
    print('Reverse quik LinkedList:', l.get_size())
    l.print_rec()
    l.reverse_recursive()
    print('Reverse recursive LinkedList:', l.get_size())
    l.print_rec()

"""
Вывод:

New LinkedList: 0 None
Add 0 into LinkedList: 1 <__main__.Node object at 0x00000181791132F0> 0
Add 1 into LinkedList: 2 <__main__.Node object at 0x00000181791132F0> 1 1
Print LinkedList:
0 1 
Insert 2 in 1 into LinkedList: 3
0 2 1 
Insert 4 in 0 into LinkedList: 4
4 0 2 1 
Insert 21 in 12 into LinkedList: 5
4 0 2 1 21 
Reverse LinkedList: 5
21 1 2 0 4 
Insert 12 in 21 into LinkedList: 6
21 1 2 0 4 12 
Reverse with function LinkedList: 6
12 4 0 2 1 21 
Get 3th element into LinkedList: <__main__.Node object at 0x0000018179110170> 2
Get 25th element into LinkedList: None
Delete 3th element into LinkedList: 5
12 4 0 1 21 
Pop into LinkedList: 21
12 4 0 1 
Reverse quik LinkedList: 4
1 0 4 12 
Reverse recursive LinkedList: 4
12 4 0 1 
"""
