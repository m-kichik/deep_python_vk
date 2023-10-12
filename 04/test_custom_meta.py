import unittest

from custom_meta import CustomMeta


class TestCustomMeta(unittest.TestCase):
    def test_class_attr(self):
        class SomeClass(metaclass=CustomMeta):
            attr = "some x"
            _protected_attr = "some protected x"
            __private_attr = "some private x"

            def __init__(self):
                self.value = 0
                self._protected_value = 4
                self.__private_value = 2

            def line(self):
                return "some line"

            def _protected_line(self):
                return "some protected line"

            def __private_line(self):
                return "some private line"

            def __str__(self):
                return "Some Class custom by CustomMeta"

        with self.subTest("Test ordinary class attribute name and value (class)"):
            with self.assertRaises(AttributeError):
                SomeClass.attr
            self.assertTrue(hasattr(SomeClass, "custom_attr"))
            self.assertEqual(SomeClass.custom_attr, "some x")

        with self.subTest("Test protected class attribute name and value (class)"):
            with self.assertRaises(AttributeError):
                SomeClass._protected_attr
            self.assertTrue(hasattr(SomeClass, "_custom_protected_attr"))
            self.assertEqual(SomeClass._custom_protected_attr, "some protected x")

        with self.subTest("Test private class attribute name and value (class)"):
            with self.assertRaises(AttributeError):
                SomeClass._SomeClass__private_attr
            self.assertTrue(hasattr(SomeClass, "_SomeClass__custom_private_attr"))
            self.assertEqual(
                SomeClass._SomeClass__custom_private_attr, "some private x"
            )

        with self.subTest("Test ordinary class method name (class)"):
            self.assertTrue(hasattr(SomeClass, "custom_line"))

        with self.subTest("Test protected class method name (class)"):
            self.assertTrue(hasattr(SomeClass, "_custom_protected_line"))

        with self.subTest("Test private class method name (class)"):
            self.assertTrue(hasattr(SomeClass, "_SomeClass__custom_private_line"))

        with self.subTest("Test magic method name (class)"):
            self.assertTrue(hasattr(SomeClass, "__str__"))

        some_instance = SomeClass()

        with self.subTest("Test ordinary class attribute name and value (instance)"):
            with self.assertRaises(AttributeError):
                some_instance.attr
            self.assertTrue(hasattr(some_instance, "custom_attr"))
            self.assertEqual(some_instance.custom_attr, "some x")

        with self.subTest("Test protected class attribute name and value (instance)"):
            with self.assertRaises(AttributeError):
                some_instance._protected_attr
            self.assertTrue(hasattr(some_instance, "_custom_protected_attr"))
            self.assertEqual(some_instance._custom_protected_attr, "some protected x")

        with self.subTest("Test private class attribute name and value (instance)"):
            with self.assertRaises(AttributeError):
                some_instance._SomeClass__private_attr
            self.assertTrue(hasattr(some_instance, "_SomeClass__custom_private_attr"))
            self.assertEqual(
                some_instance._SomeClass__custom_private_attr, "some private x"
            )

        with self.subTest("Test ordinary instance attribute name and value (instance)"):
            with self.assertRaises(AttributeError):
                some_instance.value
            self.assertTrue(hasattr(some_instance, "custom_value"))
            self.assertEqual(some_instance.custom_value, 0)

        with self.subTest(
            "Test protected instance attribute name and value (instance)"
        ):
            with self.assertRaises(AttributeError):
                some_instance._protected_value
            self.assertTrue(hasattr(some_instance, "_custom_protected_value"))
            self.assertEqual(some_instance._custom_protected_value, 4)

        with self.subTest("Test private instance attribute name and value (instance)"):
            with self.assertRaises(AttributeError):
                some_instance._SomeClass__private_value
            self.assertTrue(hasattr(some_instance, "_SomeClass__custom_private_value"))
            self.assertEqual(some_instance._SomeClass__custom_private_value, 2)

        with self.subTest("Test ordinary class method name (instance)"):
            with self.assertRaises(AttributeError):
                some_instance.line()
            self.assertTrue(hasattr(some_instance, "custom_line"))
            self.assertEqual(some_instance.custom_line(), "some line")

        with self.subTest("Test protected class method name (instance)"):
            with self.assertRaises(AttributeError):
                some_instance._protected_line()
            self.assertTrue(hasattr(some_instance, "_custom_protected_line"))
            self.assertEqual(
                some_instance._custom_protected_line(), "some protected line"
            )

        with self.subTest("Test private class method name (instance)"):
            with self.assertRaises(AttributeError):
                some_instance._SomeClass__private_line()
            self.assertTrue(hasattr(some_instance, "_SomeClass__custom_private_line"))
            self.assertEqual(
                some_instance._SomeClass__custom_private_line(), "some private line"
            )

        with self.subTest("Test magic method name (instance)"):
            self.assertTrue(hasattr(some_instance, "__str__"))
            self.assertEqual(str(some_instance), "Some Class custom by CustomMeta")

        with self.subTest("Test setting ordinary attribute dynamically"):
            some_instance.new_value = 24
            with self.assertRaises(AttributeError):
                some_instance.new_value
            self.assertTrue(hasattr(some_instance, "custom_new_value"))
            self.assertEqual(some_instance.custom_new_value, 24)

        with self.subTest("Test setting 'protected' attribute dynamically"):
            some_instance._new_protected_value = 24
            with self.assertRaises(AttributeError):
                some_instance._new_protected_value
            self.assertTrue(hasattr(some_instance, "_custom_new_protected_value"))
            self.assertEqual(some_instance._custom_new_protected_value, 24)


if __name__ == "__main__":
    unittest.main()
