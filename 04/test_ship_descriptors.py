import unittest

from ship_descriptors import (
    NameDescriptor,
    ShipClassDescriptor,
    YearDescriptor,
    CrewSizeDescriptor,
    ExpeditionStateDescriptor,
)


class TestDescriptors(unittest.TestCase):
    def test_name_descriptor(self):
        name_descriptor = NameDescriptor()

        with self.subTest("Test set name without owner"):
            self.assertEqual(name_descriptor.__get__(None, None), None)

        owner = type("Ship", (), {})
        name_descriptor.__set_name__(owner, "ship")
        instance = owner()

        with self.subTest("Test set (and get) correct name"):
            name_descriptor.__set__(instance, "Erebus")
            self.assertEqual(name_descriptor.__get__(instance, None), "Erebus")

        with self.subTest("Test set incorrect type on name"):
            with self.assertRaises(TypeError):
                name_descriptor.__set__(instance, 42)

    def test_ship_class_descriptor(self):
        ship_class_descriptor = ShipClassDescriptor()

        with self.subTest("Test set class without owner"):
            self.assertEqual(ship_class_descriptor.__get__(None, None), None)

        owner = type("Ship", (), {})
        ship_class_descriptor.__set_name__(owner, "ship_class")
        instance = owner()

        with self.subTest("Test set (and get) correct class"):
            ship_class_descriptor.__set__(instance, "Bomb Vessel")
            self.assertEqual(
                ship_class_descriptor.__get__(instance, None), "Bomb Vessel"
            )

        with self.subTest("Test set incorrect type of class"):
            with self.assertRaises(TypeError):
                ship_class_descriptor.__set__(instance, 42)

        with self.subTest("Test set incorrect class"):
            with self.assertRaises(ValueError):
                ship_class_descriptor.__set__(instance, "Submarine")

    def test_year_descriptor(self):
        year_descriptor = YearDescriptor()

        with self.subTest("Test set year without owner"):
            self.assertEqual(year_descriptor.__get__(None, None), None)

        owner = type("Ship", (), {})
        year_descriptor.__set_name__(owner, "year")
        instance = owner()

        with self.subTest("Test set (and get) correct year"):
            year_descriptor.__set__(instance, 1826)
            self.assertEqual(year_descriptor.__get__(instance, None), 1826)

        with self.subTest("Test set incorrect type of year"):
            with self.assertRaises(TypeError):
                year_descriptor.__set__(instance, "1826")

    def test_crew_size_descriptor(self):
        crew_size_descriptor = CrewSizeDescriptor()

        with self.subTest("Test crew size name without owner"):
            self.assertEqual(crew_size_descriptor.__get__(None, None), None)

        owner = type("Ship", (), {})
        crew_size_descriptor.__set_name__(owner, "crew_size")
        instance = owner()

        with self.subTest("Test set (and get) correct crew size"):
            crew_size_descriptor.__set__(instance, 67)
            self.assertEqual(crew_size_descriptor.__get__(instance, None), 67)

        with self.subTest("Test set incorrect type of crew size"):
            with self.assertRaises(TypeError):
                crew_size_descriptor.__set__(instance, "67")

        with self.subTest("Test set incorrect value of crew size"):
            with self.assertRaises(ValueError):
                crew_size_descriptor.__set__(instance, 1)

    def test_expedition_state_descriptor(self):
        expedition_state_descriptor = ExpeditionStateDescriptor()

        with self.subTest("Test expedition state name without owner"):
            self.assertEqual(expedition_state_descriptor.__get__(None, None), None)

        owner = type("Ship", (), {})
        expedition_state_descriptor.__set_name__(owner, "expedition_state")
        instance = owner()

        with self.subTest("Test set (and get) correct expedition state"):
            expedition_state_descriptor.__set__(instance, True)
            self.assertTrue(expedition_state_descriptor.__get__(instance, None))

        with self.subTest("Test set incorrect type of expedition state"):
            with self.assertRaises(TypeError):
                expedition_state_descriptor.__set__(instance, "False")


if __name__ == "__main__":
    unittest.main()
