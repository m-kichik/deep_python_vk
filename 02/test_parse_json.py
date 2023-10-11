import unittest
from unittest.mock import Mock, patch
from parse_json import parse_json, default_callback


class TestParseJSON(unittest.TestCase):
    def test_default_callback(self):
        with patch("builtins.print") as mock_print:
            default_callback("world", "hello")
            mock_print.assert_called_with("Received hello in field world!")

    def test_parse_json(self):
        json_str = '{"k1": "w1 w2", "k2": "w2 w3", "k3": "w3 w4"}'
        required_fields = ["k1", "k2"]
        keywords = ["w1", "w2"]

        with self.subTest("Test parse_json with default callback"):
            with patch("builtins.print") as mock_print:
                parse_json(
                    json_str,
                    required_fields=required_fields,
                    keywords=keywords,
                    keyword_callback=default_callback,
                )
                calls = mock_print.call_args_list
            mock_print.assert_any_call("Received w1 in field k1!")
            mock_print.assert_any_call("Received w2 in field k1!")
            mock_print.assert_any_call("Received w2 in field k2!")
            self.assertEqual(len(calls), 3)

        with self.subTest("Test parse_json with custom callback"):
            mock_custom_callback = Mock()
            parse_json(
                json_str,
                required_fields=required_fields,
                keywords=keywords,
                keyword_callback=mock_custom_callback,
            )
            calls = mock_custom_callback.call_args_list
            mock_custom_callback.assert_any_call("k1", "w1")
            mock_custom_callback.assert_any_call("k1", "w2")
            mock_custom_callback.assert_any_call("k2", "w2")
            self.assertEqual(len(calls), 3)

        with self.subTest("Test parse_json without required_fields"):
            mock_custom_callback = Mock()
            with self.assertRaises(ValueError):
                parse_json(
                    json_str, keywords=keywords, keyword_callback=mock_custom_callback
                )

        with self.subTest("Test parse_json without keywords"):
            mock_custom_callback = Mock()
            with self.assertRaises(ValueError):
                parse_json(
                    json_str,
                    required_fields=required_fields,
                    keyword_callback=mock_custom_callback,
                )

        with self.subTest("Test parse_json without keyword_callback"):
            mock_custom_callback = Mock()
            with self.assertRaises(ValueError):
                parse_json(
                    json_str,
                    keywords=keywords,
                    required_fields=required_fields,
                    keyword_callback=None,
                )

        with self.subTest("Test parse_json with no matched kw-w"):
            json_str = '{"k1": "w1 w2", "k2": "w2 w3", "k3": "w3 w4"}'
            required_fields = ["k1", "k2"]
            keywords = ["w4"]
            mock_custom_callback = Mock()
            parse_json(
                json_str,
                required_fields=required_fields,
                keywords=keywords,
                keyword_callback=mock_custom_callback,
            )
            mock_custom_callback.assert_not_called()

        with self.subTest("Test parse_json with non-existed kw"):
            json_str = '{"k1": "w1 w2", "k2": "w2 w3", "k3": "w3 w4"}'
            required_fields = ["k5"]
            keywords = ["w1", "w2"]
            mock_custom_callback = Mock()
            parse_json(
                json_str,
                required_fields=required_fields,
                keywords=keywords,
                keyword_callback=mock_custom_callback,
            )
            mock_custom_callback.assert_not_called()

        with self.subTest("Test parse_json with non-existed w"):
            json_str = '{"k1": "w1 w2", "k2": "w2 w3", "k3": "w3 w4"}'
            required_fields = ["k1", "k2"]
            keywords = ["w5"]
            mock_custom_callback = Mock()
            parse_json(
                json_str,
                required_fields=required_fields,
                keywords=keywords,
                keyword_callback=mock_custom_callback,
            )
            mock_custom_callback.assert_not_called()

        with self.subTest("Test parse_json with keyword 'inside' another word"):
            json_str = '{"k1": "wordinnerword"}'
            required_fields = ["k1"]
            keywords = ["word", "inner"]
            mock_custom_callback = Mock()
            parse_json(
                json_str,
                required_fields=required_fields,
                keywords=keywords,
                keyword_callback=mock_custom_callback,
            )
            mock_custom_callback.assert_not_called()

        with self.subTest("Test parse_json with keyword 'inside' punctuation marks"):
            json_str = '{"k1": "word_,inner,word."}'
            required_fields = ["k1"]
            keywords = ["word"]
            mock_custom_callback = Mock()
            parse_json(
                json_str,
                required_fields=required_fields,
                keywords=keywords,
                keyword_callback=mock_custom_callback,
            )
            mock_custom_callback.assert_called_once_with("k1", "word")

        with self.subTest("Test parse_json with keyword in different register (upper)"):
            json_str = '{"42": "This is the answer."}'
            required_fields = ["42"]
            keywords = ["Answer"]
            mock_custom_callback = Mock()
            parse_json(
                json_str,
                required_fields=required_fields,
                keywords=keywords,
                keyword_callback=mock_custom_callback,
            )
            mock_custom_callback.assert_called_once_with("42", "answer")

        with self.subTest("Test parse_json with a number of keywords and required_fields"):
            json_str = '{"k1": "w1 w2", "k2": "w3 w4", "k3": "w1 w2"}'
            required_fields = ["k1", "k2"]
            keywords = ["w1", "w3"]
            mock_custom_callback = Mock()
            parse_json(
                json_str,
                required_fields=required_fields,
                keywords=keywords,
                keyword_callback=mock_custom_callback,
            )
            mock_custom_callback.assert_any_call("k1", "w1")
            mock_custom_callback.assert_any_call("k2", "w3")

        with self.subTest("Test parse_json with a number of required fields for same keyword"):
            json_str = '{"k1": "w1 w2", "k2": "w2 w3"}'
            required_fields = ["k1", "k2"]
            keywords = ["w2"]
            mock_custom_callback = Mock()
            parse_json(
                json_str,
                required_fields=required_fields,
                keywords=keywords,
                keyword_callback=mock_custom_callback,
            )
            mock_custom_callback.assert_any_call("k1", "w2")
            mock_custom_callback.assert_any_call("k2", "w2")

        with self.subTest("Test parse_json with a number of keyword duplicates"):
            json_str = '{"k1": "w1 w1", "k2": "w2 w3"}'
            required_fields = ["k1", "k2"]
            keywords = ["w1"]
            mock_custom_callback = Mock()
            parse_json(
                json_str,
                required_fields=required_fields,
                keywords=keywords,
                keyword_callback=mock_custom_callback,
            )
            mock_custom_callback.assert_called_with("k1", "w1")
            call_args = [call[0] for call in mock_custom_callback.call_args_list]
            self.assertEqual(len(call_args), 2)
            self.assertTrue(call_args[0] == call_args[1])

        with self.subTest("Test parse_json with a number of keywords in one required_field"):
            json_str = '{"k1": "w1 w2", "k2": "w1 w2 w3 w4 w5", "k3": "w3 w4"}'
            required_fields = ["k2"]
            keywords = ["w1", "w2", "w4", "w5"]
            mock_custom_callback = Mock()
            parse_json(
                json_str,
                required_fields=required_fields,
                keywords=keywords,
                keyword_callback=mock_custom_callback,
            )
            mock_custom_callback.assert_any_call("k2", "w1")
            mock_custom_callback.assert_any_call("k2", "w2")
            mock_custom_callback.assert_any_call("k2", "w4")
            mock_custom_callback.assert_any_call("k2", "w5")

        with self.subTest("Test parse_json with keyword in different register (lower)"):
            json_str = '{"42": "This is the Answer."}'
            required_fields = ["42"]
            keywords = ["answer"]
            mock_custom_callback = Mock()
            parse_json(
                json_str,
                required_fields=required_fields,
                keywords=keywords,
                keyword_callback=mock_custom_callback,
            )
            mock_custom_callback.assert_called_once_with("42", "answer")


if __name__ == "__main__":
    unittest.main()
