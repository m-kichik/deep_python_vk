import unittest

from ship_descriptors import (
    Ship,
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
            self.assertEqual(name_descriptor.__get__(instance, None), "Erebus")

        with self.subTest("Test re-set correct type on name"):
            name_descriptor.__set__(instance, "Victoria")
            self.assertEqual(name_descriptor.__get__(instance, None), "Victoria")

        with self.subTest("Test re-set incorrect type on name"):
            with self.assertRaises(TypeError):
                name_descriptor.__set__(instance, 42)
            self.assertEqual(name_descriptor.__get__(instance, None), "Victoria")

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
            self.assertEqual(
                ship_class_descriptor.__get__(instance, None), "Bomb Vessel"
            )

        with self.subTest("Test set incorrect class"):
            with self.assertRaises(ValueError):
                ship_class_descriptor.__set__(instance, "Submarine")
            self.assertEqual(
                ship_class_descriptor.__get__(instance, None), "Bomb Vessel"
            )

        with self.subTest("Test re-set correct class"):
            ship_class_descriptor.__set__(instance, "Ship of the line")
            self.assertEqual(
                ship_class_descriptor.__get__(instance, None), "Ship of the line"
            )

        with self.subTest("Test re-set incorrect type of class"):
            with self.assertRaises(TypeError):
                ship_class_descriptor.__set__(instance, 42)
            self.assertEqual(
                ship_class_descriptor.__get__(instance, None), "Ship of the line"
            )

        with self.subTest("Test set incorrect class"):
            with self.assertRaises(ValueError):
                ship_class_descriptor.__set__(instance, "Submarine")
            self.assertEqual(
                ship_class_descriptor.__get__(instance, None), "Ship of the line"
            )

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
            self.assertEqual(year_descriptor.__get__(instance, None), 1826)

        with self.subTest("Test re-set (and get) correct year"):
            year_descriptor.__set__(instance, 1887)
            self.assertEqual(year_descriptor.__get__(instance, None), 1887)
        
        with self.subTest("Test re-set incorrect type of year"):
            with self.assertRaises(TypeError):
                year_descriptor.__set__(instance, "1887")
            self.assertEqual(year_descriptor.__get__(instance, None), 1887)

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
            self.assertEqual(crew_size_descriptor.__get__(instance, None), 67)

        with self.subTest("Test set incorrect value of crew size"):
            with self.assertRaises(ValueError):
                crew_size_descriptor.__set__(instance, 1)
            self.assertEqual(crew_size_descriptor.__get__(instance, None), 67)

        with self.subTest("Test re-set (and get) correct crew size"):
            crew_size_descriptor.__set__(instance, 430)
            self.assertEqual(crew_size_descriptor.__get__(instance, None), 430)

        with self.subTest("Test re-set incorrect type of crew size"):
            with self.assertRaises(TypeError):
                crew_size_descriptor.__set__(instance, "430")
            self.assertEqual(crew_size_descriptor.__get__(instance, None), 430)

        with self.subTest("Test re-set incorrect value of crew size"):
            with self.assertRaises(ValueError):
                crew_size_descriptor.__set__(instance, 1)
            self.assertEqual(crew_size_descriptor.__get__(instance, None), 430)

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
            self.assertTrue(expedition_state_descriptor.__get__(instance, None))

        with self.subTest("Test re-set (and get) correct expedition state"):
            expedition_state_descriptor.__set__(instance, False)
            self.assertFalse(expedition_state_descriptor.__get__(instance, None))

        with self.subTest("Test re-set incorrect type of expedition state"):
            with self.assertRaises(TypeError):
                expedition_state_descriptor.__set__(instance, "True")
            self.assertFalse(expedition_state_descriptor.__get__(instance, None))

    def test_with_ship(self):
        ship = Ship("Aurora", "Cruiser", 1903, 590, False)

        with self.subTest("Test name"):
            self.assertEqual(ship.name, "Aurora")

        with self.subTest("Test new correct name"):
            ship.name = "Novik"
            self.assertEqual(ship.name, "Novik")
        
        with self.subTest("Test new incorrect name"):
            with self.assertRaises(TypeError):
                ship.name = 404
            self.assertEqual(ship.name, "Novik")

        with self.subTest("Test ship class"):
            self.assertEqual(ship.ship_class, "Cruiser")

        with self.subTest("Test new correct ship class"):
            ship.ship_class = "Destroyer"
            self.assertEqual(ship.ship_class, "Destroyer")

        with self.subTest("Test new incorrect (by type) ship class"):
            with self.assertRaises(TypeError):
                ship.ship_class = 404
            self.assertEqual(ship.ship_class, "Destroyer")

        with self.subTest("Test new incorrect (by name) ship class"):
            with self.assertRaises(ValueError):
                ship.ship_class = "Boat"
            self.assertEqual(ship.ship_class, "Destroyer")

        with self.subTest("Test build year"):
            self.assertEqual(ship.build_year, 1903)

        with self.subTest("Test new build year"):
            ship.build_year = 1911
            self.assertEqual(ship.build_year, 1911)

        with self.subTest("Test new incorrect build year"):
            with self.assertRaises(TypeError):
                ship.build_year = "1911"
            self.assertEqual(ship.build_year, 1911)

        with self.subTest("Test crew size"):
            self.assertEqual(ship.crew_size, 590)

        with self.subTest("Test new correct crew size"):
            ship.crew_size = 142
            self.assertEqual(ship.crew_size, 142)

        with self.subTest("Test new incorrect (by type) crew size"):
            with self.assertRaises(TypeError):
                ship.crew_size = "142"
            self.assertEqual(ship.crew_size, 142)

        with self.subTest("Test new incorrect (by value) crew size"):
            with self.assertRaises(ValueError):
                ship.crew_size = 0
            self.assertEqual(ship.crew_size, 142)

        with self.subTest("Test expedition state"):
            self.assertFalse(ship.in_expedition)

        with self.subTest("Test new correct expedition state"):
            ship.in_expedition = True
            self.assertTrue(ship.in_expedition)

        with self.subTest("Test new incorrect expedition state"):
            with self.assertRaises(TypeError):
                ship.in_expedition = "True"
            self.assertTrue(ship.in_expedition)


if __name__ == "__main__":
    unittest.main()
