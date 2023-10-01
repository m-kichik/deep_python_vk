import unittest
from unittest.mock import Mock, patch
from parse_json import parse_json, default_callback


class TestParseJSON(unittest.TestCase):
    def test_default_callback(self):
        with patch("builtins.print") as mock_print:
            default_callback("hello")
            mock_print.assert_called_with("Received hello!")

    def test_parse_json(self):
        json_str = '{"k1": "w1 w2", "k2": "w2 w3", "k3": "w3 w4"}'
        required_fields = ["k1", "k2"]
        keywords = ["w1", "w2"]

        with self.subTest("Test parse_json with default callback"):
            with patch("builtins.print") as mock_print:
                parse_json(json_str, required_fields=required_fields, keywords=keywords)
                calls = mock_print.call_args_list
            self.assertEqual(
                len([call for call in calls if call[0][0] == "Received w1!"]), 1
            )
            self.assertEqual(
                len([call for call in calls if call[0][0] == "Received w2!"]), 2
            )

        with self.subTest("Test parse_json with custom callback"):
            mock_custom_callback = Mock()
            parse_json(
                json_str,
                required_fields=required_fields,
                keywords=keywords,
                keyword_callback=mock_custom_callback,
            )
            calls = mock_custom_callback.call_args_list
            self.assertEqual(len([call for call in calls if call[0][0] == "w1"]), 1)
            self.assertEqual(len([call for call in calls if call[0][0] == "w2"]), 2)

        with self.subTest("Test parse_json without required_fields"):
            mock_custom_callback = Mock()
            parse_json(
                json_str, keywords=keywords, keyword_callback=mock_custom_callback
            )
            calls = mock_custom_callback.call_args_list
            self.assertFalse(calls)

        with self.subTest("Test parse_json without keywords"):
            mock_custom_callback = Mock()
            parse_json(
                json_str,
                required_fields=required_fields,
                keyword_callback=mock_custom_callback,
            )
            calls = mock_custom_callback.call_args_list
            self.assertFalse(calls)

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
            calls = mock_custom_callback.call_args_list
            self.assertFalse(calls)

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
            calls = mock_custom_callback.call_args_list
            self.assertFalse(calls)

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
            calls = mock_custom_callback.call_args_list
            self.assertFalse(calls)


if __name__ == "__main__":
    unittest.main()
