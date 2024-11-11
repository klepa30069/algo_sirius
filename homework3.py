"""
Задача 3:
Инвертировать бинарное дерево поиска. Инвертировать дерево – значит перекомпоновать
его элементы таким образом, чтобы узлы справа от материнского узла были больше,
а слева-меньше.

Функция invert по времени получилась примерно O(n) по памяти O(1).
"""


class Node:
    def __init__(self, data):
        self.__data = data
        self.__left = None
        self.__right = None

    def get_data(self):
        return self.__data

    def get_left(self):
        return self.__left

    def get_right(self):
        return self.__right

    def set_data(self, data):
        self.__data = data

    def set_left(self, left):
        self.__left = left

    def set_right(self, right):
        self.__right = right


class BinarySearchTree:
    def __init__(self):
        self.__root = None
        self.__count = 0
        self.__inverted = False

    def get_root(self):
        return self.__root

    def get_count(self):
        return self.__count

    def add(self, data):
        self.__count += 1
        if self.__root is None:
            self.__root = Node(data)
        else:
            node = self.__root
            while node is not None:
                if self.__inverted:
                    if data > node.get_data():
                        if node.get_left() is None:
                            node.set_left(Node(data))
                            break
                        else:
                            node = node.get_left()
                    else:
                        if node.get_right() is None:
                            node.set_right(Node(data))
                            break
                        else:
                            node = node.get_right()
                else:
                    if data < node.get_data():
                        if node.get_left() is None:
                            node.set_left(Node(data))
                            break
                        else:
                            node = node.get_left()
                    else:
                        if node.get_right() is None:
                            node.set_right(Node(data))
                            break
                        else:
                            node = node.get_right()

    def __print_easy(self, node):
        if node is not None:
            print(node.get_data())
            if node.get_left() is not None:
                print('left:', node.get_left().get_data())
            if node.get_right() is not None:
                print('right:', node.get_right().get_data())
            print('-' * 50)
            self.__print_easy(node.get_left())
            self.__print_easy(node.get_right())

    def print_easy(self):
        self.__print_easy(self.__root)

    def __print_horizontal(self, nodes):
        new_nodes = list()
        if len(nodes) != 0:
            for node in nodes:
                print(node.get_data(), end=' ')
                if node.get_left() is not None:
                    new_nodes.append(node.get_left())
                if node.get_right() is not None:
                    new_nodes.append(node.get_right())
            print()
            self.__print_horizontal(new_nodes)

    def print_horizontal(self):
        self.__print_horizontal([self.__root])

    def __height(self, node):
        if node is None:
            return 0
        return max(self.__height(node.get_left()), self.__height(node.get_right())) + 1

    def height(self):
        if self.__root is None:
            return 0
        return self.__height(self.__root)

    def __print_level(self, node, level):
        if node is None:
            return
        if level == 0:
            print(node.get_data(), end=' ')
        self.__print_level(node.get_left(), level - 1)
        self.__print_level(node.get_right(), level - 1)

    def print_bfs(self):
        for i in range(self.height()):
            self.__print_level(self.__root, i)
            print()

    def __rotation(self, node, is_right):
        if is_right:
            root = node
            root_left = node.get_left()
            root_left_right = root_left.get_right()
            node = root_left
            node.set_right(root)
            root.set_left(root_left_right)
        else:
            root = node
            root_right = node.get_right()
            root_right_left = root_right.get_left()
            node = root_right
            node.set_left(root)
            root.set_right(root_right_left)
        return node

    def __tree_minimum(self, node):
        if self.__inverted:
            if node.get_right() is not None:
                return self.__tree_minimum(node.get_right())
            else:
                return node
        else:
            if node.get_left() is not None:
                return self.__tree_minimum(node.get_left())
            else:
                return node

    def __delete(self, node, data):
        if node is None:
            return node
        if self.__inverted:
            if data > node.get_data():
                node.set_left(self.__delete(node.get_left(), data))
            elif data < node.get_data():
                node.set_right(self.__delete(node.get_right(), data))
            else:
                if node.get_left() is None:
                    new_node = node.get_right()
                    node = None
                    return new_node
                elif node.get_right() is None:
                    new_node = node.get_left()
                    node = None
                    return new_node
                min_node = self.__tree_minimum(node.get_left())
                node.set_data(min_node.get_data())
                node.set_left(self.__delete(node.get_left(), min_node.get_data()))
        else:
            if data < node.get_data():
                node.set_left(self.__delete(node.get_left(), data))
            elif data > node.get_data():
                node.set_right(self.__delete(node.get_right(), data))
            else:
                if node.get_left() is None:
                    new_node = node.get_right()
                    node = None
                    return new_node
                elif node.get_right() is None:
                    new_node = node.get_left()
                    node = None
                    return new_node
                min_node = self.__tree_minimum(node.get_right())
                node.set_data(min_node.get_data())
                node.set_right(self.__delete(node.get_right(), min_node.get_data()))
        return node

    def delete(self, data):
        self.__count -= 1
        self.__root = self.__delete(self.__root, data)

    def __balance(self, node):
        if node is not None:
            node.set_left(self.__balance(node.get_left()))
            height_left = self.__height(node.get_left())
            height_right = self.__height(node.get_right())
            if (height_left - height_right) > 1:
                height_left_left = self.__height(node.get_left().get_left())
                height_left_right = self.__height(node.get_left().get_right())
                if height_left_left < height_left_right:
                    node.set_left(self.__rotation(node.get_left(), False))
                node = self.__rotation(node, True)
            node.set_right(self.__balance(node.get_right()))
            height_left = self.__height(node.get_left())
            height_right = self.__height(node.get_right())
            if (height_right - height_left) > 1:
                height_right_left = self.__height(node.get_right().get_left())
                height_right_right = self.__height(node.get_right().get_right())
                if height_right_left > height_right_right:
                    node.set_right(self.__rotation(node.get_right(), True))
                node = self.__rotation(node, False)
        return node

    def balance(self):
        if self.__root is not None:
            self.__root = self.__balance(self.__root)
        return self.__count

    def __invert(self, node):
        if node is None:
            return None
        new_node = node.get_right()
        node.set_right(node.get_left())
        node.set_left(new_node)
        self.__invert(node.get_right())
        self.__invert(node.get_left())
        return node

    def invert(self):
        self.__inverted = not self.__inverted
        self.__root = self.__invert(self.__root)


if __name__ == "__main__":
    b = BinarySearchTree()
    print('New BinarySearchTree:', b.get_count(), b.get_root())
    b.add(20)
    print('Add 20 into BinarySearchTree:', b.get_count(), b.get_root(), b.get_root().get_data())
    b.add(60)
    print('Add 60 into BinarySearchTree:', b.get_count())
    print('Print easy BinarySearchTree:')
    b.print_easy()
    b.add(8)
    print('Add 8 into BinarySearchTree:', b.get_count())
    print('Print horizontal BinarySearchTree:')
    b.print_horizontal()
    b.add(7)
    print('Add 7 into BinarySearchTree:', b.get_count())
    print('Print BinarySearchTree:')
    b.print_bfs()
    b.add(27)
    print('Add 27 into BinarySearchTree:', b.get_count())
    print('Print BinarySearchTree:')
    b.print_bfs()
    b.add(96)
    print('Add 96 into BinarySearchTree:', b.get_count())
    print('Print BinarySearchTree:')
    b.print_bfs()
    b.add(23)
    print('Add 23 into BinarySearchTree:', b.get_count())
    print('Print BinarySearchTree:')
    b.print_bfs()
    b.add(53)
    print('Add 53 into BinarySearchTree:', b.get_count())
    print('Print BinarySearchTree:')
    b.print_bfs()
    b.add(52)
    print('Add 52 into BinarySearchTree:', b.get_count())
    print('Print BinarySearchTree:')
    b.print_bfs()
    b.add(54)
    print('Add 54 into BinarySearchTree:', b.get_count())
    print('Print BinarySearchTree:')
    b.print_bfs()
    b.add(55)
    print('Add 55 into BinarySearchTree:', b.get_count())
    print('Print BinarySearchTree:')
    b.print_bfs()
    b.add(56)
    print('Add 56 into BinarySearchTree:', b.get_count())
    print('Print BinarySearchTree:')
    b.print_bfs()
    b.add(72)
    print('Add 72 into BinarySearchTree:', b.get_count())
    print('Print BinarySearchTree:')
    b.print_bfs()
    b.add(2)
    print('Add 2 into BinarySearchTree:', b.get_count())
    print('Print BinarySearchTree:')
    b.print_bfs()
    b.add(5)
    print('Add 5 into BinarySearchTree:', b.get_count())
    print('Print BinarySearchTree:')
    b.print_bfs()
    b.delete(7)
    print('Delete 7 element into BinarySearchTree:', b.get_count())
    print('Print BinarySearchTree:')
    b.print_bfs()
    b.balance()
    print('Balance BinarySearchTree:', b.get_count())
    print('Print BinarySearchTree:')
    b.print_bfs()
    b.delete(55)
    print('Delete 55 element into BinarySearchTree:', b.get_count())
    print('Print BinarySearchTree:')
    b.print_bfs()
    b.invert()
    print('Invert BinarySearchTree:', b.get_count())
    print('Print BinarySearchTree:')
    b.print_bfs()
    b.add(55)
    print('Add 55 into BinarySearchTree:', b.get_count())
    print('Print BinarySearchTree:')
    b.print_bfs()
    b.balance()
    print('Balance BinarySearchTree:', b.get_count())
    print('Print BinarySearchTree:')
    b.print_bfs()
    b.delete(55)
    print('Delete 55 element into BinarySearchTree:', b.get_count())
    print('Print BinarySearchTree:')
    b.print_bfs()

"""
Вывод:

New BinarySearchTree: 0 None
Add 20 into BinarySearchTree: 1 <__main__.Node object at 0x00000212DC4732F0> 20
Add 60 into BinarySearchTree: 2
Print easy BinarySearchTree:
20
right: 60
--------------------------------------------------
60
--------------------------------------------------
Add 8 into BinarySearchTree: 3
Print horizontal BinarySearchTree:
20 
8 60 
Add 7 into BinarySearchTree: 4
Print BinarySearchTree:
20 
8 60 
7 
Add 27 into BinarySearchTree: 5
Print BinarySearchTree:
20 
8 60 
7 27 
Add 96 into BinarySearchTree: 6
Print BinarySearchTree:
20 
8 60 
7 27 96 
Add 23 into BinarySearchTree: 7
Print BinarySearchTree:
20 
8 60 
7 27 96 
23 
Add 53 into BinarySearchTree: 8
Print BinarySearchTree:
20 
8 60 
7 27 96 
23 53 
Add 52 into BinarySearchTree: 9
Print BinarySearchTree:
20 
8 60 
7 27 96 
23 53 
52 
Add 54 into BinarySearchTree: 10
Print BinarySearchTree:
20 
8 60 
7 27 96 
23 53 
52 54 
Add 55 into BinarySearchTree: 11
Print BinarySearchTree:
20 
8 60 
7 27 96 
23 53 
52 54 
55 
Add 56 into BinarySearchTree: 12
Print BinarySearchTree:
20 
8 60 
7 27 96 
23 53 
52 54 
55 
56 
Add 72 into BinarySearchTree: 13
Print BinarySearchTree:
20 
8 60 
7 27 96 
23 53 72 
52 54 
55 
56 
Add 2 into BinarySearchTree: 14
Print BinarySearchTree:
20 
8 60 
7 27 96 
2 23 53 72 
52 54 
55 
56 
Add 5 into BinarySearchTree: 15
Print BinarySearchTree:
20 
8 60 
7 27 96 
2 23 53 72 
5 52 54 
55 
56 
Delete 7 element into BinarySearchTree: 14
Print BinarySearchTree:
20 
8 60 
2 27 96 
5 23 53 72 
52 54 
55 
56 
Balance BinarySearchTree: 14
Print BinarySearchTree:
53 
20 60 
5 27 55 96 
2 8 23 52 54 56 72 
Delete 55 element into BinarySearchTree: 13
Print BinarySearchTree:
53 
20 60 
5 27 56 96 
2 8 23 52 54 72 
Invert BinarySearchTree: 13
Print BinarySearchTree:
53 
60 20 
96 56 27 5 
72 54 52 23 8 2 
Add 55 into BinarySearchTree: 14
Print BinarySearchTree:
53 
60 20 
96 56 27 5 
72 54 52 23 8 2 
55 
Balance BinarySearchTree: 14
Print BinarySearchTree:
53 
60 20 
96 55 27 5 
72 56 54 52 23 8 2 
Delete 55 element into BinarySearchTree: 13
Print BinarySearchTree:
53 
60 20 
96 56 27 5 
72 54 52 23 8 2 
"""
