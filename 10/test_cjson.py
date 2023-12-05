import unittest

import cjson


class TestCJSON(unittest.TestCase):
    def test_loads(self):
        with self.subTest("Test incorrect string argument"):
            with self.assertRaises(ValueError):
                cjson.loads("abc")

        with self.subTest("Test incorrect non-string argument"):
            with self.assertRaises(TypeError):
                cjson.loads(42)

        with self.subTest("Test incorrect key"):
            with self.assertRaises(ValueError):
                cjson.loads("{42: 42}")

        with self.subTest("Test incorrect value"):
            with self.assertRaises(ValueError):
                cjson.loads("{42: 42.0}")

        with self.subTest("Test string key and string value"):
            self.assertEqual(cjson.loads('{"x": "y"}'), {"x": "y"})

        with self.subTest("Test string key and int value"):
            self.assertEqual(cjson.loads('{"42": 42}'), {"42": 42})

        with self.subTest("Test multiple values"):
            self.assertEqual(
                cjson.loads('{"x": "y", "42": 42, "hello": "world", "-4242": -4242}'),
                {"x": "y", "42": 42, "hello": "world", "-4242": -4242},
            )

    def test_dumps(self):
        with self.subTest("Test incorrect key"):
            with self.assertRaises(TypeError):
                cjson.loads({42: 42})

        with self.subTest("Test incorrect value"):
            with self.assertRaises(TypeError):
                cjson.loads({42: 42.0})

        with self.subTest("Test empty dict"):
            self.assertEqual(cjson.dumps({}), "{}")

        with self.subTest("Test dict with string key and string value"):
            self.assertEqual(cjson.dumps({"x": "y"}), '{"x":"y"}')

        with self.subTest("Test dict with string key and non-string value"):
            self.assertEqual(cjson.dumps({"42": 42}), '{"42":42}')

        with self.subTest("Test multiple values"):
            self.assertEqual(
                cjson.dumps({"x": "y", "42": 42, "hello": "world", "-4242": -4242}),
                '{"x":"y","42":42,"hello":"world","-4242":-4242}',
            )


if __name__ == "__main__":
    unittest.main()
