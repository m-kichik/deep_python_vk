import unittest
from unittest.mock import MagicMock, patch

import requests

from server import Server


class TestServer(unittest.TestCase):
    def test_init(self):
        with self.subTest("Test default"):
            server = Server(n_words=4)
            self.assertEqual(server.n_words, 4)
            self.assertEqual(server.host, "localhost")
            self.assertEqual(server.port, 65001)
            self.assertEqual(server.n_workers, 1)

        with self.subTest("Test default"):
            server = Server(n_words=2, host="host", port=8000, n_workers=4)
            self.assertEqual(server.n_words, 2)
            self.assertEqual(server.host, "host")
            self.assertEqual(server.port, 8000)
            self.assertEqual(server.n_workers, 4)

    def test_callback(self):
        server = Server(4)

        with self.subTest("Test first call"):
            with patch("builtins.print") as mock_print:
                server.callback()

                mock_print.assert_called_once_with("Processed 1 calls")
                self.assertEqual(server.n_calls, 1)

        with self.subTest("Test subsequent calls"):
            with patch("builtins.print") as mock_print:
                for _ in range(42):
                    server.callback()

                mock_print.assert_called_with("Processed 43 calls")
                self.assertEqual(server.n_calls, 43)

    def test_count_words(self):
        server = Server(2)

        with self.subTest("Test normal line"):
            test_line = "two one three three two three"
            result = server.count_words(test_line)
            self.assertEqual(result, {"three": 3, "two": 2})

        with self.subTest("Test line with a few words"):
            test_line = "two two"
            result = server.count_words(test_line)
            self.assertEqual(result, {"two": 2})

        with self.subTest("Test empty line"):
            test_line = ""
            result = server.count_words(test_line)
            self.assertEqual(result, {})

    def test_worker(self):
        server = Server(3)

        with self.subTest("Test correct responce"):
            with patch("requests.get") as mock_requests_get:
                mock_requests_get.return_value.text = "one two two three three three"
                connection = MagicMock()
                connection.recv.return_value = "http://test.ru".encode("utf-8")

                url = server.worker(connection)

                self.assertEqual(url, "http://test.ru")
                connection.sendall.assert_called_with(
                    '{"one": 1, "two": 2, "three": 3}'.encode("utf-8")
                )

        with self.subTest("Test request exception"):
            with patch(
                "requests.get", side_effect=requests.exceptions.RequestException
            ) as mock_requests_get:
                connection = MagicMock()
                connection.recv.return_value = "http://bad_link.com".encode("utf-8")
                url = server.worker(connection)
                self.assertEqual(url, "http://bad_link.com")
                connection.sendall.assert_called_with(b"{}")


if __name__ == "__main__":
    unittest.main()
