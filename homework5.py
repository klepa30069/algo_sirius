"""
Задача 5:
Написать класс, реализующий структуру данных на базе красно-черного дерева для
хранения пар “ключ-значение”

Весь код работает на основе красно-чёрного дерева.
Функция add по времени получилась примерно O(log n) по памяти O(1).
Функция get_value по времени получилась примерно O(log n) по памяти O(1).
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
        self.__key = None
        self.__value = None
        self.__right = None
        self.__left = None
        self.__color = Color.RED

    def get_parent(self):
        return self.__parent

    def get_key(self):
        return self.__key

    def get_value(self):
        return self.__value

    def get_right(self):
        return self.__right

    def get_left(self):
        return self.__left

    def get_color(self):
        return self.__color

    def set_parent(self, node):
        self.__parent = node

    def set_key(self, key):
        self.__key = key

    def set_value(self, value):
        self.__value = value

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
            print(node.get_key(), '=', node.get_value())
            if node.get_left() is not None:
                print('left:', node.get_left().get_key(), '=', node.get_left().get_value())
            if node.get_right() is not None:
                print('right:', node.get_right().get_key(), '=', node.get_right().get_value())
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

    def add(self, key, value):
        new_node = Node()
        new_node.set_key(key)
        new_node.set_value(value)
        root = self.__root
        root_parent = None
        while root is not None:
            root_parent = root
            if new_node.get_key() < root.get_key():
                root = root.get_left()
            else:
                root = root.get_right()
        new_node.set_parent(root_parent)
        if root_parent is None:
            self.__root = new_node
        elif new_node.get_key() < root_parent.get_key():
            root_parent.set_left(new_node)
        else:
            root_parent.set_right(new_node)
        self.__add(new_node)

    def __find_node_key(self, node, key):
        if node is None or node.get_key() == key:
            return node
        elif key < node.get_key():
            return self.__find_node_key(node.get_left(), key)
        else:
            return self.__find_node_key(node.get_right(), key)

    def find_key(self, key):
        if self.__root is not None:
            result = self.__find_node_key(self.__root, key)
            return result

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

    def delete(self, value):
        node = None
        if self.__root is not None:
            node = self.__find_node_key(self.__root, value)
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


class DictionaryTree:
    def __init__(self):
        self.__tree = RedBlackTree()

    def get_tree(self):
        return self.__tree

    def add(self, key, value):
        self.__tree.add(key, value)

    def get_value(self, key):
        node = self.__tree.find_key(key)
        if node is not None:
            return node.get_value()
        return None

    def delete(self, key):
        node = self.__tree.find_key(key)
        if node is not None:
            self.__tree.delete(key)


if __name__ == "__main__":
    d = DictionaryTree()
    print('New DictionaryTree:', d.get_tree().get_root())
    d.add('Question?', 'Answer!')
    print('-----Add Question? = Answer! into DictionaryTree-----')
    d.get_tree().tree_print()
    d.add('What\'s time now?', '14:00!')
    print('-----Add What\'s time now? = 14:00! into DictionaryTree-----')
    d.get_tree().tree_print()
    print('Get Question? =', d.get_value('Question?'))
    print('Get What\'s time now? =', d.get_value('What\'s time now?'))
    d.delete('Question?')
    print('-----Delete Question? in DictionaryTree-----')
    d.get_tree().tree_print()
    print('Get Question? =', d.get_value('Question?'))

"""
Вывод:

New DictionaryTree: None
-----Add Question? = Answer! into DictionaryTree-----
Question? = Answer!
--------------------------------------------------
-----Add What's time now? = 14:00! into DictionaryTree-----
Question? = Answer!
right: What's time now? = 14:00!
--------------------------------------------------
What's time now? = 14:00!
--------------------------------------------------
Get Question? = Answer!
Get What's time now? = 14:00!
-----Delete Question? in DictionaryTree-----
What's time now? = 14:00!
--------------------------------------------------
Get Question? = None
"""
