from typing import Any, Hashable


class TwoWayList:
    class Node:
        def __init__(self,
                     value: Hashable = None,
                     left: Any = None,
                     right: Any = None):
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
            self.head.left = new_node
            self.head = new_node
        return new_node

    def pop_last(self) -> Hashable:
        if not self.tail:
            raise IndexError("Can not pop item from empty list")
        if self.head == self.tail:
            value = self.head.value
            self.head = None
            self.tail = None
        else:
            value = self.tail.value
            self.tail = self.tail.left
            self.tail.right = None
        return value

    def move2top(self, node: Node) -> None:
        if node is self.head:
            return

        if node is self.tail:
            self.tail = node.left
            self.tail.right = None
        else:
            node.left.right = node.right
            node.right.left = node.left

        node.right = self.head
        node.left = None
        self.head.left = node
        self.head = node

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.value)
            current = current.right
        return result


class LRUCache:
    def __init__(self, limit: int = 42):
        self.__limit = limit
        self.__n_items = 0
        self.__queue = TwoWayList()
        self.__items_dict = {}

    def get(self, key):
        if not isinstance(key, Hashable):
            raise TypeError(f"Unhashable type: {type(key)}")

        if key not in self.__items_dict:
            return None
        self.__queue.move2top(self.__items_dict[key]["list_in_queue"])
        return self.__items_dict[key]["value"]

    def __set_value(self, key, value):
        list_in_queue = self.__queue.add2top(key)
        self.__items_dict[key] = {
            "value": value,
            "list_in_queue": list_in_queue
            }

    def set(self, key: Hashable, value: Any):
        if not isinstance(key, Hashable):
            raise TypeError(f"Unhashable type: {type(key)}")

        if key in self.__items_dict:
            self.__queue.move2top(self.__items_dict[key]["list_in_queue"])
            self.__items_dict[key]["value"] = value
        else:
            if self.__n_items == self.__limit:
                key2remove = self.__queue.pop_last()
                self.__items_dict.pop(key2remove)
                self.__set_value(key, value)
            else:
                self.__set_value(key, value)
                self.__n_items += 1


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
