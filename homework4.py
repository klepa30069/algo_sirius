"""
Задача 4:
Реализовать балансировку красно-черного дерева.

Балансировка происходит при добавлении и удалении элементов.
Функция add по времени получилась примерно O(log n) по памяти O(1).
Функция delete по времени получилась примерно O(log n) по памяти O(1).
"""
from enum import Enum


class Color(Enum):
    RED = 'красный'
    BLACK = 'чёрный'

    def __str__(self):
        return f'- {self.value}'


class Node:
    def __init__(self):
        self.__parent = None
        self.__data = None
        self.__right = None
        self.__left = None
        self.__color = Color.RED

    def get_parent(self):
        return self.__parent

    def get_data(self):
        return self.__data

    def get_right(self):
        return self.__right

    def get_left(self):
        return self.__left

    def get_color(self):
        return self.__color

    def set_parent(self, node):
        self.__parent = node

    def set_data(self, data):
        self.__data = data

    def set_right(self, node):
        self.__right = node

    def set_left(self, node):
        self.__left = node

    def set_color(self, color):
        self.__color = color


class RedBlackTree:
    def __init__(self):
        self.__root = None

    def get_root(self):
        return self.__root

    def __tree_print(self, node):
        if node is not None:
            print(node.get_data(), node.get_color())
            if node.get_left() is not None:
                print('left:', node.get_left().get_data(), node.get_left().get_color())
            if node.get_right() is not None:
                print('right:', node.get_right().get_data(), node.get_right().get_color())
            print('-' * 50)
            self.__tree_print(node.get_left())
            self.__tree_print(node.get_right())

    def tree_print(self):
        self.__tree_print(self.__root)

    def __height_black(self, node):
        if node is None:
            return 1
        left_height = self.__height_black(node.get_left())
        right_height = self.__height_black(node.get_right())
        if left_height == -1 or right_height == -1 or left_height != right_height:
            return -1
        if node.get_color() == Color.BLACK:
            return left_height + 1
        else:
            return left_height

    def height_black(self):
        if self.__root is not None:
            return self.__height_black(self.__root)

    def __rotation(self, node, is_right):
        if is_right:
            node_left = node.get_left()
            node.set_left(node_left.get_right())
            if node_left.get_right() is not None:
                node_left.get_right().set_parent(node)
            node_left.set_parent(node.get_parent())
            if node.get_parent() is None:
                self.__root = node_left
            elif node == node.get_parent().get_left():
                node.get_parent().set_left(node_left)
            else:
                node.get_parent().set_right(node_left)
            node_left.set_right(node)
            node.set_parent(node_left)
        else:
            node_right = node.get_right()
            node.set_right(node_right.get_left())
            if node_right.get_left() is not None:
                node_right.get_left().set_parent(node)
            node_right.set_parent(node.get_parent())
            if node.get_parent() is None:
                self.__root = node_right
            elif node == node.get_parent().get_left():
                node.get_parent().set_left(node_right)
            else:
                node.get_parent().set_right(node_right)
            node_right.set_left(node)
            node.set_parent(node_right)

    def __add(self, node):
        while node != self.__root and node.get_parent().get_color() == Color.RED:
            if node.get_parent() == node.get_parent().get_parent().get_left():
                parent_parent_right = node.get_parent().get_parent().get_right()
                if parent_parent_right is not None and parent_parent_right.get_color() == Color.RED:
                    node.get_parent().set_color(Color.BLACK)
                    parent_parent_right.set_color(Color.BLACK)
                    node.get_parent().get_parent().set_color(Color.RED)
                    node = node.get_parent().get_parent()
                else:
                    if node == node.get_parent().get_right():
                        node = node.get_parent()
                        self.__rotation(node, False)
                    node.get_parent().set_color(Color.BLACK)
                    node.get_parent().get_parent().set_color(Color.RED)
                    self.__rotation(node.get_parent().get_parent(), True)
            else:
                parent_parent_left = node.get_parent().get_parent().get_left()
                if parent_parent_left is not None and parent_parent_left.get_color() == Color.RED:
                    node.get_parent().set_color(Color.BLACK)
                    parent_parent_left.set_color(Color.BLACK)
                    node.get_parent().get_parent().set_color(Color.RED)
                    node = node.get_parent().get_parent()
                else:
                    if node == node.get_parent().get_left():
                        node = node.get_parent()
                        self.__rotation(node, True)
                    node.get_parent().set_color(Color.BLACK)
                    node.get_parent().get_parent().set_color(Color.RED)
                    self.__rotation(node.get_parent().get_parent(), False)
        self.__root.set_color(Color.BLACK)

    def add(self, data):
        new_node = Node()
        new_node.set_data(data)
        root = self.__root
        root_parent = None
        while root is not None:
            root_parent = root
            if new_node.get_data() < root.get_data():
                root = root.get_left()
            else:
                root = root.get_right()
        new_node.set_parent(root_parent)
        if root_parent is None:
            self.__root = new_node
        elif new_node.get_data() < root_parent.get_data():
            root_parent.set_left(new_node)
        else:
            root_parent.set_right(new_node)
        self.__add(new_node)

    def __find_node_data(self, node, data):
        if node is None or node.get_data() == data:
            return node
        elif data < node.get_data():
            return self.__find_node_data(node.get_left(), data)
        else:
            return self.__find_node_data(node.get_right(), data)

    def __swap_nodes(self, node1, node2):
        if node1.get_parent() is None:
            self.__root = node2
        elif node1 == node1.get_parent().get_left():
            node1.get_parent().set_left(node2)
        else:
            node1.get_parent().set_right(node2)
        if node2 is not None:
            node2.set_parent(node1.get_parent())
        else:
            node2 = node1.get_parent()

    def __tree_minimum(self, node):
        if node.get_left() is not None:
            return self.__tree_minimum(node.get_left())
        else:
            return node

    def __delete(self, node):
        while node != self.__root and node.get_color() == Color.BLACK:
            if node == node.get_parent().get_left():
                parent_right = node.get_parent().get_right()
                if parent_right.get_color() == Color.RED:
                    parent_right.set_color(Color.BLACK)
                    node.get_parent().set_color(Color.RED)
                    self.__rotation(node.get_parent(), False)
                    parent_right = node.get_parent().get_right()
                flag_left = True
                if parent_right.get_left() is not None:
                    flag_left = parent_right.get_left().get_color() == Color.BLACK
                flag_right = True
                if parent_right.get_right() is not None:
                    flag_right = parent_right.get_right().get_color() == Color.BLACK
                if flag_left and flag_right:
                    parent_right.set_color(Color.RED)
                    node = node.get_parent()
                else:
                    flag_right = True
                    if parent_right.get_right() is not None:
                        flag_right = parent_right.get_right().get_color() == Color.BLACK
                    if flag_right:
                        parent_right.get_left().set_color(Color.BLACK)
                        parent_right.set_color(Color.RED)
                        self.__rotation(parent_right, True)
                        parent_right = node.get_parent().get_right()
                    parent_right.set_color(node.get_parent().get_color())
                    node.get_parent().set_color(Color.BLACK)
                    parent_right.get_right().set_color(Color.BLACK)
                    self.__rotation(node.get_parent(), False)
                    node = self.__root
            else:
                parent_left = node.get_parent().get_left()
                if parent_left.get_color() == Color.RED:
                    parent_left.set_color(Color.BLACK)
                    node.get_parent().set_color(Color.RED)
                    self.__rotation(node.get_parent(), True)
                    parent_left = node.get_parent().get_left()
                flag_right = True
                if parent_left.get_right() is not None:
                    flag_right = parent_left.get_right().get_color() == Color.BLACK
                flag_left = True
                if parent_left.get_left() is not None:
                    flag_left = parent_left.get_left().get_color()
                if flag_right and flag_left:
                    parent_left.set_color(Color.RED)
                    node = node.get_parent()
                else:
                    flag_left = True
                    if parent_left.get_left() is not None:
                        flag_left = parent_left.get_left().get_color() == Color.BLACK
                    if flag_left:
                        parent_left.get_right().set_color(Color.BLACK)
                        parent_left.set_color(Color.RED)
                        self.__rotation(parent_left, False)
                        parent_left = node.get_parent().get_left()
                    parent_left.set_color(node.get_parent().get_color())
                    node.get_parent().set_color(Color.BLACK)
                    parent_left.get_left().set_color(Color.BLACK)
                    self.__rotation(node.get_parent(), True)
                    node = self.__root
        node.set_color(Color.BLACK)

    def delete(self, data):
        node = None
        if self.__root is not None:
            node = self.__find_node_data(self.__root, data)
        if node is None:
            return
        new_node = node
        new_node_color = new_node.get_color()
        if node.get_left() is None:
            node_child = node.get_right()
            self.__swap_nodes(node, node.get_right())
        elif node.get_right() is None:
            node_child = node.get_left()
            self.__swap_nodes(node, node.get_left())
        else:
            new_node = self.__tree_minimum(node.get_right())
            new_node_color = new_node.get_color()
            node_child = new_node.get_right()
            if new_node.get_parent() == node:
                if node_child is not None:
                    node_child.set_parent(new_node)
                else:
                    node_child = new_node
            else:
                self.__swap_nodes(new_node, new_node.get_right())
                new_node.set_right(node.get_right())
                new_node.get_right().set_parent(new_node)
            self.__swap_nodes(node, new_node)
            new_node.set_left(node.get_left())
            new_node.get_left().set_parent(new_node)
            new_node.set_color(node.get_color())
        if new_node_color == Color.BLACK:
            self.__delete(node_child)


if __name__ == "__main__":
    rb = RedBlackTree()
    print('New RedBlackTree:', rb.get_root())
    rb.add(20)
    print('Add 20 into RedBlackTree:', rb.get_root(), rb.get_root().get_data(), rb.get_root().get_color())
    rb.add(60)
    print('-----Add 60 into RedBlackTree-----')
    rb.tree_print()
    rb.add(8)
    print('-----Add 8 into RedBlackTree-----')
    rb.tree_print()
    rb.add(7)
    print('-----Add 7 into RedBlackTree-----')
    rb.tree_print()
    rb.add(27)
    print('-----Add 27 into RedBlackTree-----')
    rb.tree_print()
    rb.add(96)
    print('-----Add 96 into RedBlackTree-----')
    rb.tree_print()
    rb.add(23)
    print('-----Add 23 into RedBlackTree-----')
    rb.tree_print()
    rb.add(53)
    print('-----Add 53 into RedBlackTree-----')
    rb.tree_print()
    rb.add(52)
    print('-----Add 52 into RedBlackTree-----')
    rb.tree_print()
    rb.add(54)
    print('-----Add 54 into RedBlackTree-----')
    rb.tree_print()
    rb.add(55)
    print('-----Add 55 into RedBlackTree-----')
    rb.tree_print()
    rb.add(56)
    print('-----Add 56 into RedBlackTree-----')
    rb.tree_print()
    rb.add(72)
    print('-----Add 72 into RedBlackTree-----')
    rb.tree_print()
    rb.add(2)
    print('-----Add 2 into RedBlackTree-----')
    rb.tree_print()
    rb.add(5)
    print('-----Add 5 into RedBlackTree-----')
    rb.tree_print()
    rb.delete(7)
    print('-----Delete 7 element into RedBlackTree-----')
    rb.tree_print()
    rb.delete(55)
    print('-----Delete 55 element into RedBlackTree-----')
    rb.tree_print()
    rb.delete(53)
    print('-----Delete 53 element into RedBlackTree-----')
    rb.tree_print()

"""
Вывод:

New RedBlackTree: None
Add 20 into RedBlackTree: <__main__.Node object at 0x00000232A28E7E30> 20 - чёрный
-----Add 60 into RedBlackTree-----
20 - чёрный
right: 60 - красный
--------------------------------------------------
60 - красный
--------------------------------------------------
-----Add 8 into RedBlackTree-----
20 - чёрный
left: 8 - красный
right: 60 - красный
--------------------------------------------------
8 - красный
--------------------------------------------------
60 - красный
--------------------------------------------------
-----Add 7 into RedBlackTree-----
20 - чёрный
left: 8 - чёрный
right: 60 - чёрный
--------------------------------------------------
8 - чёрный
left: 7 - красный
--------------------------------------------------
7 - красный
--------------------------------------------------
60 - чёрный
--------------------------------------------------
-----Add 27 into RedBlackTree-----
20 - чёрный
left: 8 - чёрный
right: 60 - чёрный
--------------------------------------------------
8 - чёрный
left: 7 - красный
--------------------------------------------------
7 - красный
--------------------------------------------------
60 - чёрный
left: 27 - красный
--------------------------------------------------
27 - красный
--------------------------------------------------
-----Add 96 into RedBlackTree-----
20 - чёрный
left: 8 - чёрный
right: 60 - чёрный
--------------------------------------------------
8 - чёрный
left: 7 - красный
--------------------------------------------------
7 - красный
--------------------------------------------------
60 - чёрный
left: 27 - красный
right: 96 - красный
--------------------------------------------------
27 - красный
--------------------------------------------------
96 - красный
--------------------------------------------------
-----Add 23 into RedBlackTree-----
20 - чёрный
left: 8 - чёрный
right: 60 - красный
--------------------------------------------------
8 - чёрный
left: 7 - красный
--------------------------------------------------
7 - красный
--------------------------------------------------
60 - красный
left: 27 - чёрный
right: 96 - чёрный
--------------------------------------------------
27 - чёрный
left: 23 - красный
--------------------------------------------------
23 - красный
--------------------------------------------------
96 - чёрный
--------------------------------------------------
-----Add 53 into RedBlackTree-----
20 - чёрный
left: 8 - чёрный
right: 60 - красный
--------------------------------------------------
8 - чёрный
left: 7 - красный
--------------------------------------------------
7 - красный
--------------------------------------------------
60 - красный
left: 27 - чёрный
right: 96 - чёрный
--------------------------------------------------
27 - чёрный
left: 23 - красный
right: 53 - красный
--------------------------------------------------
23 - красный
--------------------------------------------------
53 - красный
--------------------------------------------------
96 - чёрный
--------------------------------------------------
-----Add 52 into RedBlackTree-----
27 - чёрный
left: 20 - красный
right: 60 - красный
--------------------------------------------------
20 - красный
left: 8 - чёрный
right: 23 - чёрный
--------------------------------------------------
8 - чёрный
left: 7 - красный
--------------------------------------------------
7 - красный
--------------------------------------------------
23 - чёрный
--------------------------------------------------
60 - красный
left: 53 - чёрный
right: 96 - чёрный
--------------------------------------------------
53 - чёрный
left: 52 - красный
--------------------------------------------------
52 - красный
--------------------------------------------------
96 - чёрный
--------------------------------------------------
-----Add 54 into RedBlackTree-----
27 - чёрный
left: 20 - красный
right: 60 - красный
--------------------------------------------------
20 - красный
left: 8 - чёрный
right: 23 - чёрный
--------------------------------------------------
8 - чёрный
left: 7 - красный
--------------------------------------------------
7 - красный
--------------------------------------------------
23 - чёрный
--------------------------------------------------
60 - красный
left: 53 - чёрный
right: 96 - чёрный
--------------------------------------------------
53 - чёрный
left: 52 - красный
right: 54 - красный
--------------------------------------------------
52 - красный
--------------------------------------------------
54 - красный
--------------------------------------------------
96 - чёрный
--------------------------------------------------
-----Add 55 into RedBlackTree-----
27 - чёрный
left: 20 - чёрный
right: 60 - чёрный
--------------------------------------------------
20 - чёрный
left: 8 - чёрный
right: 23 - чёрный
--------------------------------------------------
8 - чёрный
left: 7 - красный
--------------------------------------------------
7 - красный
--------------------------------------------------
23 - чёрный
--------------------------------------------------
60 - чёрный
left: 53 - красный
right: 96 - чёрный
--------------------------------------------------
53 - красный
left: 52 - чёрный
right: 54 - чёрный
--------------------------------------------------
52 - чёрный
--------------------------------------------------
54 - чёрный
right: 55 - красный
--------------------------------------------------
55 - красный
--------------------------------------------------
96 - чёрный
--------------------------------------------------
-----Add 56 into RedBlackTree-----
27 - чёрный
left: 20 - чёрный
right: 60 - чёрный
--------------------------------------------------
20 - чёрный
left: 8 - чёрный
right: 23 - чёрный
--------------------------------------------------
8 - чёрный
left: 7 - красный
--------------------------------------------------
7 - красный
--------------------------------------------------
23 - чёрный
--------------------------------------------------
60 - чёрный
left: 53 - красный
right: 96 - чёрный
--------------------------------------------------
53 - красный
left: 52 - чёрный
right: 55 - чёрный
--------------------------------------------------
52 - чёрный
--------------------------------------------------
55 - чёрный
left: 54 - красный
right: 56 - красный
--------------------------------------------------
54 - красный
--------------------------------------------------
56 - красный
--------------------------------------------------
96 - чёрный
--------------------------------------------------
-----Add 72 into RedBlackTree-----
27 - чёрный
left: 20 - чёрный
right: 60 - чёрный
--------------------------------------------------
20 - чёрный
left: 8 - чёрный
right: 23 - чёрный
--------------------------------------------------
8 - чёрный
left: 7 - красный
--------------------------------------------------
7 - красный
--------------------------------------------------
23 - чёрный
--------------------------------------------------
60 - чёрный
left: 53 - красный
right: 96 - чёрный
--------------------------------------------------
53 - красный
left: 52 - чёрный
right: 55 - чёрный
--------------------------------------------------
52 - чёрный
--------------------------------------------------
55 - чёрный
left: 54 - красный
right: 56 - красный
--------------------------------------------------
54 - красный
--------------------------------------------------
56 - красный
--------------------------------------------------
96 - чёрный
left: 72 - красный
--------------------------------------------------
72 - красный
--------------------------------------------------
-----Add 2 into RedBlackTree-----
27 - чёрный
left: 20 - чёрный
right: 60 - чёрный
--------------------------------------------------
20 - чёрный
left: 7 - чёрный
right: 23 - чёрный
--------------------------------------------------
7 - чёрный
left: 2 - красный
right: 8 - красный
--------------------------------------------------
2 - красный
--------------------------------------------------
8 - красный
--------------------------------------------------
23 - чёрный
--------------------------------------------------
60 - чёрный
left: 53 - красный
right: 96 - чёрный
--------------------------------------------------
53 - красный
left: 52 - чёрный
right: 55 - чёрный
--------------------------------------------------
52 - чёрный
--------------------------------------------------
55 - чёрный
left: 54 - красный
right: 56 - красный
--------------------------------------------------
54 - красный
--------------------------------------------------
56 - красный
--------------------------------------------------
96 - чёрный
left: 72 - красный
--------------------------------------------------
72 - красный
--------------------------------------------------
-----Add 5 into RedBlackTree-----
27 - чёрный
left: 20 - чёрный
right: 60 - чёрный
--------------------------------------------------
20 - чёрный
left: 7 - красный
right: 23 - чёрный
--------------------------------------------------
7 - красный
left: 2 - чёрный
right: 8 - чёрный
--------------------------------------------------
2 - чёрный
right: 5 - красный
--------------------------------------------------
5 - красный
--------------------------------------------------
8 - чёрный
--------------------------------------------------
23 - чёрный
--------------------------------------------------
60 - чёрный
left: 53 - красный
right: 96 - чёрный
--------------------------------------------------
53 - красный
left: 52 - чёрный
right: 55 - чёрный
--------------------------------------------------
52 - чёрный
--------------------------------------------------
55 - чёрный
left: 54 - красный
right: 56 - красный
--------------------------------------------------
54 - красный
--------------------------------------------------
56 - красный
--------------------------------------------------
96 - чёрный
left: 72 - красный
--------------------------------------------------
72 - красный
--------------------------------------------------
-----Delete 7 element into RedBlackTree-----
27 - чёрный
left: 20 - чёрный
right: 60 - чёрный
--------------------------------------------------
20 - чёрный
left: 8 - чёрный
right: 23 - чёрный
--------------------------------------------------
8 - чёрный
left: 2 - чёрный
--------------------------------------------------
2 - чёрный
right: 5 - красный
--------------------------------------------------
5 - красный
--------------------------------------------------
23 - чёрный
--------------------------------------------------
60 - чёрный
left: 53 - красный
right: 96 - чёрный
--------------------------------------------------
53 - красный
left: 52 - чёрный
right: 55 - чёрный
--------------------------------------------------
52 - чёрный
--------------------------------------------------
55 - чёрный
left: 54 - красный
right: 56 - красный
--------------------------------------------------
54 - красный
--------------------------------------------------
56 - красный
--------------------------------------------------
96 - чёрный
left: 72 - красный
--------------------------------------------------
72 - красный
--------------------------------------------------
-----Delete 55 element into RedBlackTree-----
27 - чёрный
left: 20 - чёрный
right: 60 - чёрный
--------------------------------------------------
20 - чёрный
left: 8 - чёрный
right: 23 - чёрный
--------------------------------------------------
8 - чёрный
left: 2 - чёрный
--------------------------------------------------
2 - чёрный
right: 5 - красный
--------------------------------------------------
5 - красный
--------------------------------------------------
23 - чёрный
--------------------------------------------------
60 - чёрный
left: 53 - красный
right: 96 - чёрный
--------------------------------------------------
53 - красный
left: 52 - чёрный
right: 56 - чёрный
--------------------------------------------------
52 - чёрный
--------------------------------------------------
56 - чёрный
left: 54 - красный
--------------------------------------------------
54 - красный
--------------------------------------------------
96 - чёрный
left: 72 - красный
--------------------------------------------------
72 - красный
--------------------------------------------------
-----Delete 53 element into RedBlackTree-----
27 - чёрный
left: 20 - чёрный
right: 60 - чёрный
--------------------------------------------------
20 - чёрный
left: 8 - чёрный
right: 23 - чёрный
--------------------------------------------------
8 - чёрный
left: 2 - чёрный
--------------------------------------------------
2 - чёрный
right: 5 - красный
--------------------------------------------------
5 - красный
--------------------------------------------------
23 - чёрный
--------------------------------------------------
60 - чёрный
left: 54 - красный
right: 96 - чёрный
--------------------------------------------------
54 - красный
left: 52 - чёрный
right: 56 - чёрный
--------------------------------------------------
52 - чёрный
--------------------------------------------------
56 - чёрный
--------------------------------------------------
96 - чёрный
left: 72 - красный
--------------------------------------------------
72 - красный
--------------------------------------------------
"""
