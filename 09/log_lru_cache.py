from argparse import ArgumentParser
import logging
from typing import Any, Hashable

from custom_formatter import CustomFormatter


class TwoWayList:
    class Node:
        def __init__(self, value: Hashable = None, left: Any = None, right: Any = None):
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

    def to_list(self) -> list:
        result = []
        current = self.head
        while current:
            result.append(current.value)
            current = current.right
        return result


class LRUCache:
    def __init__(self, logger: Any, limit: int = 42):
        self.__limit = limit
        self.__n_items = 0
        self.__queue = TwoWayList()
        self.__items_dict = {}
        self.__logger = logger
        self.__logger.info(f"Created LRUCache with capacity of {limit} items")

    def get(self, key) -> Any:
        if not isinstance(key, Hashable):
            msg = f"Attempt to call get with unhashable type: {type(key)}"
            self.__logger.error(msg)
            raise TypeError(msg)

        if key not in self.__items_dict:
            self.__logger.warning("Accessing a non-existent key")
            return None

        self.__logger.debug(f"Access key {key}")
        self.__queue.move2top(self.__items_dict[key]["list_in_queue"])
        return self.__items_dict[key]["value"]

    def __set_value(self, key, value) -> None:
        list_in_queue = self.__queue.add2top(key)
        self.__items_dict[key] = {"value": value, "list_in_queue": list_in_queue}

    def set(self, key: Hashable, value: Any) -> None:
        if not isinstance(key, Hashable):
            msg = f"Attempt to call set with unhashable type: {type(key)}"
            self.__logger.error(msg)
            raise TypeError(msg)

        if key in self.__items_dict:
            self.__queue.move2top(self.__items_dict[key]["list_in_queue"])
            self.__items_dict[key]["value"] = value
            self.__logger.debug(f"Set existed key {key} with value {value}")
        else:
            if self.__n_items == self.__limit:
                key2remove = self.__queue.pop_last()
                value2remove = self.__items_dict.pop(key2remove)["value"]
                self.__logger.debug(
                    f"Set key {key} with value {value}, "
                    + f"removed key {key2remove} with value {value2remove}"
                )
                self.__set_value(key, value)
            else:
                self.__logger.debug(f"Set key {key} with value {value}")
                self.__set_value(key, value)
                self.__n_items += 1
                if self.__n_items == self.__limit:
                    self.__logger.debug(
                        f"Сapacity limit of {self.__limit} items reached"
                    )


def make_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "-s", nargs="?", const=True, default=False, help="Log to terminal."
    )
    parser.add_argument(
        "-f", nargs="?", const=True, default=False, help="Activates logger formatting."
    )
    return parser


def main():
    args = make_parser().parse_args()

    handlers = [logging.FileHandler("cache.log", mode="w")]
    if args.s:
        stream_handler = logging.StreamHandler()
        if args.f:
            stream_handler.setFormatter(CustomFormatter())
        handlers.append(stream_handler)

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s\t%(levelname)s\t%(name)s\t%(message)s",
        handlers=handlers,
    )

    cache = LRUCache(logging.getLogger("lru_logger"), limit=2)

    cache.set("k1", "val1")
    cache.set("k2", "val2")
    assert cache.get("k3") is None
    assert cache.get("k2") == "val2"
    assert cache.get("k1") == "val1"

    cache.set("k3", "val3")
    assert cache.get("k3") == "val3"
    assert cache.get("k2") is None

    try:
        cache.set([4, 2], 42)
    except TypeError:
        pass

    try:
        cache.get([4, 2])
    except TypeError:
        pass


if __name__ == "__main__":
    main()
