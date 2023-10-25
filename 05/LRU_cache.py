import copy
from typing import Any, Hashable

# class Node:
#     def __init__(self, value: Hashable = None, left: Any = None, right: Any = None) -> None:
#         self.__value = value
#         self.__left = left
#         self.__right = right

#     def set_value(self, value: Hashable) -> None:
#         self.__value = value

#     def get_value(self) -> Hashable:
#         return self.__value

#     def set_left(self, other):
#         if isinstance(other, Node) or other is None:
#             self.__left = other
#         else:
#             raise TypeError('Other have to be Node or None')
        
#     def set_right(self, other):
#         if isinstance(other, Node) or other is None:
#             self.__right = other
#         else:
#             raise TypeError('Other have to be Node or None')
        
#     def get_left(self):
#         return self.__left
    
#     def get_right(self):
#         return self.__right

class TwoWayList:
    class Node:
        def __init__(self,
                     value: Hashable = None,
                     left: Any = None, right:
                     Any = None):
            self.value = value
            self.left = left
            self.right = right

    def __init__(self) -> None:
        self.head = None
        self.tail = None

    def add2top(self, value: Hashable) -> Node:
        new_node = self.Node(value)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.right = self.head
            # new_node.set_right(self.head)
            self.head.left = new_node
            # self.head.set_left(new_node)
            self.head = new_node
        return new_node

    def pop_last(self) -> Hashable:
        if not self.tail:
            raise IndexError('Can not pop item from empty list')
        if self.head == self.tail:
            value = self.head.value
            # value = self.head.get_value()
            self.head = None
            self.tail = None
        else:
            value = self.tail.value
            # value = self.tail.get_value()
            self.tail = self.tail.left
            # self.tail = self.tail.get_left()
            self.tail.right = None
            # self.tail.set_right(None)
        return value

    def move2top(self, node:Node) -> None:
        if node is self.head:
            return
        
        if node is self.tail:
            self.tail = node.left
            # self.tail = node.get_left()
            self.tail.right = None
            # self.tail.set_right(None)
        else:
            node.left.right = node.right
            # node.get_left().set_right(node.get_right())
            node.right.left = node.left
            # node.get_right().set_left(node.get_left())
        
        node.right = self.head
        # node.set_right(self.head)
        node.left = None
        # node.set_left(None)
        self.head.left = node
        # self.head.set_left(node)
        self.head = node

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.value)
            # result.append(current.get_value())
            current = current.right
            # current = current.get_right()
        return result

class LRUCache:
    def __init__(self, limit: int = 42):
        self.limit = limit
        self.n_items = 0
        self.queue = TwoWayList()
        self.items_dict = dict()

    def get(self, key):
        if not key in self.items_dict:
            return None
        self.queue.move2top(self.items_dict[key]['list_in_queue'])
        return self.items_dict[key]['value']

    def __set_value(self, key, value):
        list_in_queue = self.queue.add2top(key)
        self.items_dict[key] = {
                'value' : value,
                'list_in_queue' : list_in_queue
            }
    
    def set(self, key: Any, value: Any):
        if key in self.items_dict:
            self.queue.move2top(self.items_dict[key]['list_in_queue'])
            self.items_dict[key]['value'] = value
        else:
            if self.n_items == self.limit:
                key2remove = self.queue.pop_last()
                self.items_dict.pop(key2remove)
                self.__set_value(key, value)
            else:
                self.__set_value(key, value)
                self.n_items += 1


def main():
    cache = LRUCache(2)

    cache.set("k1", "val1")
    cache.set("k2", "val2")
    assert cache.get("k3") is None
    assert cache.get("k2") == "val2"
    assert cache.get("k1") == "val1"

    cache.set("k3", "val3")
    assert cache.get("k3") == "val3"
    assert cache.get("k2") is None
    assert cache.get("k1") == "val1"


if __name__ == "__main__":
    main()
