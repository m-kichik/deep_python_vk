import unittest

from custom_list import CustomList


class TestCustomList(unittest.TestCase):
    @classmethod
    def assertEqualElementwise(self, first_list:list, second_list:list):
        assertion_msg = f'List {first_list} is not equal to {second_list}'
        n_elements = len(first_list)
        if len(second_list) != n_elements:
            raise self.failureException(assertion_msg)
        else:
            for i in range(n_elements):
                if first_list[i] != second_list[i]:
                    raise self.failureException(assertion_msg)
                
    def test_assert_equal_elementwise(self):
        with self.subTest("Test equal_lists"):
            self.assertEqualElementwise(CustomList([4, 2, 42]), CustomList([4, 2, 42]))

        with self.subTest("Test equal_lists"):
            with self.assertRaises(AssertionError):
                self.assertEqualElementwise(CustomList([4, 2, 42]), CustomList([4, 2]))

        with self.subTest("Test equal_lists"):
            with self.assertRaises(AssertionError):
                self.assertEqualElementwise(CustomList([4, 2, 42]), CustomList([2, 4, 42]))

    def test_add(self):
        with self.subTest("Test source CustomLists don't change"):
            custom_list1 = CustomList([4, 2, 42])
            custom_list2 = CustomList([4, 2, 42])
            result = custom_list1 + custom_list2
            self.assertEqualElementwise(custom_list1, CustomList([4, 2, 42]))
            self.assertEqualElementwise(custom_list2, CustomList([4, 2, 42]))

        with self.subTest("Test 2 CustomLists with same length"):
            custom_list1 = CustomList([1, 2, 3])
            custom_list2 = CustomList([4, 5, 6])
            result = custom_list1 + custom_list2
            self.assertEqualElementwise(result, CustomList([5, 7, 9]))

        with self.subTest("Test 2 CustomLists with different length"):
            custom_list1 = CustomList([7, 8, 9])
            custom_list2 = CustomList([10, 11])
            result = custom_list1 + custom_list2
            self.assertEqualElementwise(result, CustomList([17, 19, 9]))

        with self.subTest("Test 2 CustomLists with different length (another order)"):
            custom_list1 = CustomList([12])
            custom_list2 = CustomList([13, 14])
            result = custom_list1 + custom_list2
            self.assertEqualElementwise(result, CustomList([25, 14]))

        with self.subTest("Test CustomList and list of same length"):
            custom_list = CustomList([15, 16, 17])
            list_ = [18, 19, 20]
            result = custom_list + list_
            self.assertEqualElementwise(result, CustomList([33, 35, 37]))

        with self.subTest("Test CustomList and list of different length"):
            custom_list = CustomList([21, 22, 23])
            list_ = [24]
            result = custom_list + list_
            self.assertEqualElementwise(result, CustomList([45, 22, 23]))

        with self.subTest(
            "Test CustomList and list of different length (another order)"
        ):
            custom_list = CustomList([25])
            list_ = [26, 27, 28]
            result = custom_list + list_
            self.assertEqualElementwise(result, CustomList([51, 27, 28]))

        with self.subTest("Test CustomList and empty CustomList"):
            custom_list1 = CustomList([29, 30])
            custom_list2 = CustomList([])
            result = custom_list1 + custom_list2
            self.assertEqualElementwise(result, custom_list1)

        with self.subTest("Test CustomList and empty CustomList (another order)"):
            custom_list1 = CustomList([])
            custom_list2 = CustomList([31, 32])
            result = custom_list1 + custom_list2
            self.assertEqualElementwise(result, custom_list2)

        with self.subTest("Test CustomList and empty list"):
            custom_list = CustomList([33, 34])
            list_ = []
            result = custom_list + list_
            self.assertEqualElementwise(result, custom_list)

        with self.subTest("Test empty CustomList and non-empty list"):
            custom_list = CustomList([])
            list_ = [35, 36]
            result = custom_list + list_
            self.assertEqualElementwise(result, CustomList(list_))

        with self.subTest("Test two empty CustomLists"):
            custom_list1 = CustomList([])
            custom_list2 = CustomList([])
            result = custom_list1 + custom_list2
            self.assertEqualElementwise(result, CustomList([]))

        with self.subTest("Test empty CustomList and empty list"):
            custom_list = CustomList([])
            list_ = []
            result = custom_list + list_
            self.assertEqualElementwise(result, CustomList([]))

    def test_radd(self):
        with self.subTest("Test source CustomLists don't change"):
            custom_list1 = CustomList([4, 2, 42])
            custom_list2 = CustomList([4, 2, 42])
            result = custom_list1.__radd__(custom_list2)
            self.assertEqualElementwise(custom_list1, CustomList([4, 2, 42]))
            self.assertEqualElementwise(custom_list2, CustomList([4, 2, 42]))

        with self.subTest("Test 2 CustomLists"):
            custom_list1 = CustomList([1, 2, 3])
            custom_list2 = CustomList([4, 5, 6])
            result = custom_list1.__radd__(custom_list2)
            self.assertEqualElementwise(result, CustomList([5, 7, 9]))

        with self.subTest("Test list and CustomList"):
            list_ = [7, 8, 9]
            custom_list = CustomList([10, 11, 12])
            result = list_ + custom_list
            self.assertEqualElementwise(result, CustomList([17, 19, 21]))

        with self.subTest("Test 2 CustomLists with different length"):
            custom_list1 = CustomList([7, 8, 9])
            custom_list2 = CustomList([10, 11])
            result = custom_list1.__radd__(custom_list2)
            self.assertEqualElementwise(result, CustomList([17, 19, 9]))

        with self.subTest("Test 2 CustomLists with different length (another order)"):
            custom_list1 = CustomList([12])
            custom_list2 = CustomList([13, 14])
            result = custom_list1.__radd__(custom_list2)
            self.assertEqualElementwise(result, CustomList([25, 14]))

        with self.subTest("Test CustomList and list of different length"):
            custom_list = CustomList([21, 22, 23])
            list_ = [24]
            result = list_ + custom_list
            self.assertEqualElementwise(result, CustomList([45, 22, 23]))

        with self.subTest(
            "Test CustomList and list of different length (another order)"
        ):
            custom_list = CustomList([25])
            list_ = [26, 27, 28]
            result = list_ + custom_list
            self.assertEqualElementwise(result, CustomList([51, 27, 28]))

    def test_sub(self):
        with self.subTest("Test source CustomLists don't change"):
            custom_list1 = CustomList([4, 2, 42])
            custom_list2 = CustomList([4, 2, 42])
            result = custom_list1 - custom_list2
            self.assertEqualElementwise(custom_list1, CustomList([4, 2, 42]))
            self.assertEqualElementwise(custom_list2, CustomList([4, 2, 42]))

        with self.subTest("Test 2 CustomLists with same length"):
            custom_list1 = CustomList([1, 2, 3])
            custom_list2 = CustomList([4, 5, 6])
            result = custom_list1 - custom_list2
            self.assertEqualElementwise(result, CustomList([-3, -3, -3]))

        with self.subTest("Test 2 CustomLists with different length"):
            custom_list1 = CustomList([7, 8, 9])
            custom_list2 = CustomList([10, 11])
            result = custom_list1 - custom_list2
            self.assertEqualElementwise(result, CustomList([-3, -3, 9]))

        with self.subTest("Test 2 CustomLists with different length (another order)"):
            custom_list1 = CustomList([12])
            custom_list2 = CustomList([13, 14])
            result = custom_list1 - custom_list2
            self.assertEqualElementwise(result, CustomList([-1, -14]))

        with self.subTest("Test CustomList and list of same length"):
            custom_list = CustomList([15, 16, 17])
            list_ = [18, 19, 20]
            result = custom_list - list_
            self.assertEqualElementwise(result, CustomList([-3, -3, -3]))

        with self.subTest("Test CustomList and list of different length"):
            custom_list = CustomList([21, 22, 23])
            list_ = [24]
            result = custom_list - list_
            self.assertEqualElementwise(result, CustomList([-3, 22, 23]))

        with self.subTest(
            "Test CustomList and list of different length (another order)"
        ):
            custom_list = CustomList([25])
            list_ = [26, 27, 28]
            result = custom_list - list_
            self.assertEqualElementwise(result, CustomList([-1, -27, -28]))

        with self.subTest("Test CustomList and empty CustomList"):
            custom_list1 = CustomList([29, 30])
            custom_list2 = CustomList([])
            result = custom_list1 - custom_list2
            self.assertEqualElementwise(result, custom_list1)

        with self.subTest("Test CustomList and empty CustomList (another order)"):
            custom_list1 = CustomList([])
            custom_list2 = CustomList([31, 32])
            result = custom_list1 - custom_list2
            self.assertEqualElementwise(result, CustomList([-31, -32]))

        with self.subTest("Test CustomList and empty list"):
            custom_list = CustomList([33, 34])
            list_ = []
            result = custom_list - list_
            self.assertEqualElementwise(result, custom_list)

        with self.subTest("Test empty CustomList and non-empty list"):
            custom_list = CustomList([])
            list_ = [35, 36]
            result = custom_list - list_
            self.assertEqualElementwise(result, CustomList([-35, -36]))

        with self.subTest("Test two empty CustomLists"):
            custom_list1 = CustomList([])
            custom_list2 = CustomList([])
            result = custom_list1 - custom_list2
            self.assertEqualElementwise(result, CustomList([]))

        with self.subTest("Test empty CustomList and empty list"):
            custom_list = CustomList([])
            list_ = []
            result = custom_list - list_
            self.assertEqualElementwise(result, CustomList([]))

    def test_rsub(self):
        with self.subTest("Test source CustomLists don't change"):
            custom_list1 = CustomList([4, 2, 42])
            custom_list2 = CustomList([4, 2, 42])
            result = custom_list1.__rsub__(custom_list2)
            self.assertEqualElementwise(custom_list1, CustomList([4, 2, 42]))
            self.assertEqualElementwise(custom_list2, CustomList([4, 2, 42]))

        with self.subTest("Test 2 CustomLists"):
            custom_list1 = CustomList([1, 2, 3])
            custom_list2 = CustomList([4, 5, 6])
            result = custom_list1.__rsub__(custom_list2)
            self.assertEqualElementwise(result, CustomList([3, 3, 3]))

        with self.subTest("Test list and CustomList"):
            list_ = [7, 8, 9]
            custom_list = CustomList([10, 11, 12])
            result = list_ - custom_list
            self.assertEqualElementwise(result, CustomList([-3, -3, -3]))

        with self.subTest("Test 2 CustomLists with different length"):
            custom_list1 = CustomList([7, 8, 9])
            custom_list2 = CustomList([10, 11])
            result = custom_list1.__rsub__(custom_list2)
            self.assertEqualElementwise(result, CustomList([3, 3, -9]))

        with self.subTest("Test 2 CustomLists with different length (another order)"):
            custom_list1 = CustomList([12])
            custom_list2 = CustomList([13, 14])
            result = custom_list1.__rsub__(custom_list2)
            self.assertEqualElementwise(result, CustomList([1, 14]))

        with self.subTest("Test CustomList and list of different length"):
            custom_list = CustomList([21, 22, 23])
            list_ = [24]
            result =  list_ - custom_list
            self.assertEqualElementwise(result, CustomList([3, -22, -23]))

        with self.subTest(
            "Test CustomList and list of different length (another order)"
        ):
            custom_list = CustomList([25])
            list_ = [26, 27, 28]
            result = list_ - custom_list
            self.assertEqualElementwise(result, CustomList([1, 27, 28]))

    def test_str_representation(self):
        with self.subTest("Test CustomList"):
            custom_list = CustomList([4, 2, 42])
            result = str(custom_list)
            self.assertEqual(result, "items: 4, 2, 42; sum: 48")

        with self.subTest("Test empty CustomList"):
            custom_list = CustomList([])
            result = str(custom_list)
            self.assertEqual(result, "items: ; sum: 0")

    def test_equal(self):
        with self.subTest("Test CustomList"):
            custom_list1 = CustomList([1, 2, 3])
            custom_list2 = CustomList([1, 2, 3])
            self.assertTrue(custom_list1 == custom_list2)

        with self.subTest("Test CustomList with different order"):
            custom_list1 = CustomList([4, 5, 6])
            custom_list2 = CustomList([6, 4, 5])
            self.assertTrue(custom_list1 == custom_list2)

        with self.subTest("Test CustomList with different numbers"):
            custom_list1 = CustomList([21, 21])
            custom_list2 = CustomList([42])
            self.assertTrue(custom_list1 == custom_list2)

        with self.subTest("Test non-equal CustomList"):
            custom_list1 = CustomList([21])
            custom_list2 = CustomList([42])
            self.assertFalse(custom_list1 == custom_list2)

        with self.subTest("Test empty CustomList"):
            custom_list1 = CustomList([])
            custom_list2 = CustomList([])
            self.assertTrue(custom_list1 == custom_list2)

    def test_inequality(self):
        with self.subTest("Test CustomList"):
            custom_list1 = CustomList([1, 2, 3])
            custom_list2 = CustomList([4, 5, 6])
            self.assertTrue(custom_list1 != custom_list2)

        with self.subTest("Test equal CustomList"):
            custom_list1 = CustomList([21, 21])
            custom_list2 = CustomList([42])
            self.assertFalse(custom_list1 != custom_list2)

        with self.subTest("Test empty CustomLists"):
            custom_list1 = CustomList([])
            custom_list2 = CustomList([])
            self.assertFalse(custom_list1 != custom_list2)

    def test_less_than(self):
        with self.subTest("Test 'less' CustomList"):
            custom_list1 = CustomList([1, 2, 3])
            custom_list2 = CustomList([4, 5, 6])
            self.assertTrue(custom_list1 < custom_list2)

        with self.subTest("Test equal CustomList"):
            custom_list1 = CustomList([21, 21])
            custom_list2 = CustomList([42])
            self.assertFalse(custom_list1 < custom_list2)

        with self.subTest("Test non-'less' CustomList"):
            custom_list1 = CustomList([10, 11, 12])
            custom_list2 = CustomList([7, 8, 9])
            self.assertFalse(custom_list1 < custom_list2)

        with self.subTest("Test empty CustomLists"):
            custom_list1 = CustomList([])
            custom_list2 = CustomList([])
            self.assertFalse(custom_list1 < custom_list2)

    def test_less_equal(self):
        with self.subTest("Test 'less' CustomList"):
            custom_list1 = CustomList([1, 2, 3])
            custom_list2 = CustomList([4, 5, 6])
            self.assertTrue(custom_list1 <= custom_list2)

        with self.subTest("Test equal CustomList"):
            custom_list1 = CustomList([21, 21])
            custom_list2 = CustomList([42])
            self.assertTrue(custom_list1 <= custom_list2)

        with self.subTest("Test non-'less' CustomList"):
            custom_list1 = CustomList([10, 11, 12])
            custom_list2 = CustomList([7, 8, 9])
            self.assertFalse(custom_list1 <= custom_list2)

        with self.subTest("Test empty CustomLists"):
            custom_list1 = CustomList([])
            custom_list2 = CustomList([])
            self.assertTrue(custom_list1 <= custom_list2)

    def test_greater_than(self):
        with self.subTest("Test 'greater' CustomList"):
            custom_list1 = CustomList([4, 5, 6])
            custom_list2 = CustomList([1, 2, 3])
            self.assertTrue(custom_list1 > custom_list2)

        with self.subTest("Test equal CustomList"):
            custom_list1 = CustomList([21, 21])
            custom_list2 = CustomList([42])
            self.assertFalse(custom_list1 > custom_list2)

        with self.subTest("Test non-'greater' CustomList"):
            custom_list1 = CustomList([7, 8, 9])
            custom_list2 = CustomList([10, 11, 12])
            self.assertFalse(custom_list1 > custom_list2)

        with self.subTest("Test empty CustomLists"):
            custom_list1 = CustomList([])
            custom_list2 = CustomList([])
            self.assertFalse(custom_list1 > custom_list2)

    def test_greater_equal(self):
        with self.subTest("Test 'greater' CustomList"):
            custom_list1 = CustomList([4, 5, 6])
            custom_list2 = CustomList([1, 2, 3])
            self.assertTrue(custom_list1 >= custom_list2)

        with self.subTest("Test equal CustomList"):
            custom_list1 = CustomList([21, 21])
            custom_list2 = CustomList([42])
            self.assertTrue(custom_list1 >= custom_list2)

        with self.subTest("Test non-'greater' CustomList"):
            custom_list1 = CustomList([7, 8, 9])
            custom_list2 = CustomList([10, 11, 12])
            self.assertFalse(custom_list1 >= custom_list2)

        with self.subTest("Test empty CustomLists"):
            custom_list1 = CustomList([])
            custom_list2 = CustomList([])
            self.assertTrue(custom_list1 >= custom_list2)


if __name__ == "__main__":
    unittest.main()
