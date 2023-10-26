import unittest

from LRU_cache import TwoWayList, LRUCache


class TestTwoWayList(unittest.TestCase):
    def test_empty_list(self):
        twoway_list = TwoWayList()
        self.assertIsNone(twoway_list.head)
        self.assertIsNone(twoway_list.tail)
        self.assertEqual(twoway_list.to_list(), [])

    def test_add2top(self):
        twoway_list = TwoWayList()

        with self.subTest("Test add first value"):
            twoway_list.add2top("first")

            self.assertIs(twoway_list.head, twoway_list.tail)
            self.assertEqual(twoway_list.head.value, "first")
            self.assertIsNone(twoway_list.head.left)
            self.assertIsNone(twoway_list.head.right)

        with self.subTest("Test add second value"):
            twoway_list.add2top("second")

            self.assertEqual(twoway_list.head.value, "second")
            self.assertEqual(twoway_list.tail.value, "first")
            self.assertIsNone(twoway_list.head.left)
            self.assertIs(twoway_list.head.right, twoway_list.tail)
            self.assertIs(twoway_list.head, twoway_list.tail.left)
            self.assertIsNone(twoway_list.tail.right)

        with self.subTest("Test add third to have smth between head and tail"):
            twoway_list.add2top("third")

            self.assertEqual(twoway_list.head.value, "third")
            self.assertEqual(twoway_list.tail.value, "first")
            self.assertIsNone(twoway_list.head.left)
            self.assertIs(twoway_list.head.right, twoway_list.tail.left)
            self.assertIs(twoway_list.head.right, twoway_list.tail.left)
            self.assertIsNone(twoway_list.tail.right)

    def test_to_list(self):
        twoway_list = TwoWayList()

        with self.subTest("Test empty"):
            self.assertEqual(twoway_list.to_list(), [])

        twoway_list.add2top("first")
        twoway_list.add2top("second")
        twoway_list.add2top("third")

        with self.subTest("Test not empty"):
            self.assertEqual(twoway_list.to_list(), ["third", "second", "first"])

    def test_pop_last(self):
        twoway_list = TwoWayList()
        twoway_list.add2top("first")  # tail
        twoway_list.add2top("second")  # middle
        twoway_list.add2top("third")  # head

        with self.subTest("Test pop item"):
            self.assertEqual(twoway_list.pop_last(), "first")

            self.assertEqual(twoway_list.to_list(), ["third", "second"])
            self.assertEqual(twoway_list.tail.value, "second")
            self.assertIsNone(twoway_list.tail.right)

        with self.subTest("Test pop tail"):
            self.assertEqual(twoway_list.pop_last(), "second")

            self.assertEqual(twoway_list.to_list(), ["third"])
            self.assertEqual(twoway_list.tail.value, "third")
            self.assertIs(twoway_list.tail, twoway_list.head)
            self.assertIsNone(twoway_list.head.left)
            self.assertIsNone(twoway_list.head.right)

        with self.subTest("Test pop head"):
            self.assertEqual(twoway_list.pop_last(), "third")

            self.assertEqual(twoway_list.to_list(), [])
            self.assertIsNone(twoway_list.head)
            self.assertIsNone(twoway_list.tail)

        with self.subTest("Test pop empty"):
            with self.assertRaises(IndexError):
                twoway_list.pop_last()

    def test_move2top(self):
        twoway_list = TwoWayList()
        node_with_first = twoway_list.add2top("first")
        node_with_second = twoway_list.add2top("second")
        node_with_third = twoway_list.add2top("third")

        with self.subTest("Test move from middle"):
            twoway_list.move2top(node_with_second)

            self.assertEqual(twoway_list.to_list(), ["second", "third", "first"])
            self.assertIs(twoway_list.head, node_with_second)
            self.assertIs(twoway_list.head.right, node_with_third)
            self.assertIs(twoway_list.tail.left, node_with_third)
            self.assertIs(twoway_list.tail, node_with_first)

        with self.subTest("Test move head"):
            twoway_list.move2top(node_with_second)

            self.assertEqual(twoway_list.to_list(), ["second", "third", "first"])
            self.assertIs(twoway_list.head, node_with_second)
            self.assertIs(twoway_list.tail, node_with_first)
            self.assertIs(twoway_list.head.right, node_with_third)
            self.assertIs(twoway_list.tail.left, node_with_third)

        with self.subTest("Test move tail"):
            twoway_list.move2top(node_with_first)

            self.assertEqual(twoway_list.to_list(), ["first", "second", "third"])
            self.assertIs(twoway_list.head, node_with_first)
            self.assertIs(twoway_list.tail, node_with_third)
            self.assertIs(twoway_list.head.right, node_with_second)
            self.assertIs(twoway_list.tail.left, node_with_second)


class TestLRUCache(unittest.TestCase):
    def test_set_and_get(self):
        cache = LRUCache(4)

        with self.subTest("Test set incorrect key"):
            with self.assertRaises(TypeError):
                cache.set(["k1"], 1)

        with self.subTest("Test get incorrect key"):
            with self.assertRaises(TypeError):
                cache.get(["k1"])

        with self.subTest("Test get from empty cache"):
            self.assertIsNone(cache.get("k1"))

        with self.subTest("Test set and get correct key"):
            cache.set("k1", 1)
            self.assertEqual(cache.get("k1"), 1)

        with self.subTest("Test set new value"):
            cache.set("k1", 11)
            self.assertEqual(cache.get("k1"), 11)

        with self.subTest("Test get with non-existed key"):
            self.assertIsNone(cache.get(42))

        with self.subTest("Test set multiple items"):
            cache.set("k2", 2)
            cache.set("k3", 3)
            cache.set("k4", 4)

            self.assertEqual(cache.get("k2"), 2)
            self.assertEqual(cache.get("k3"), 3)
            self.assertEqual(cache.get("k4"), 4)

        with self.subTest("Test set more than cache capacity"):
            cache.set("k5", 5)  # ['k5', 'k4', 'k3', 'k2']

            self.assertEqual(cache.get("k5"), 5)
            self.assertIsNone(cache.get("k1"))

        with self.subTest("Test 'get' moves to top"):
            self.assertEqual(cache.get("k2"), 2)  # ['k2', 'k5', 'k4', 'k3']

            cache.set("k6", 6)  # ['k6', 'k2', 'k5', 'k4']

            self.assertEqual(cache.get("k6"), 6)
            self.assertEqual(cache.get("k3"), None)

        with self.subTest("Test 'set' new value moves to top"):
            cache.set("k4", 44)  # ['k4', 'k6', 'k2', 'k5']
            cache.set("k7", 7)  # ['k7', 'k4', 'k6', 'k2']

            self.assertIsNone(cache.get("k5"))
            self.assertEqual(cache.get("k4"), 44)
            self.assertEqual(cache.get("k7"), 7)


if __name__ == "__main__":
    unittest.main()
