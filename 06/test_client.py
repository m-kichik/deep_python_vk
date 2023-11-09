import os

import unittest
from unittest import mock

from client import Client


class TestClient(unittest.TestCase):
    def test_init(self):
        with self.subTest("Test default"):
            client = Client()
            self.assertEqual(client.host, "localhost")
            self.assertEqual(client.port, 65001)
            self.assertEqual(client.n_threads, 1)

        with self.subTest("Test custom"):
            client = Client(host="host", port=8000, n_threads=4)
            self.assertEqual(client.host, "host")
            self.assertEqual(client.port, 8000)
            self.assertEqual(client.n_threads, 4)

    def test_send_urls(self):
        client = Client(n_threads=1)

        with self.subTest("Test incorrect argument"):
            with self.assertRaises(ValueError):
                urls = 42
                client.send_urls(urls)

            with self.assertRaises(FileNotFoundError):
                urls = "non-existed.txt"
                client.send_urls(urls)

        urls = ["https://google.com", "https://vk.company", "https://home.vk.team"]
        test_file = os.path.abspath("test_urls.txt")
        with open(test_file, "w") as file:
            file.write("\n".join(urls))

        # with self.subTest("Test correct argument"):
            # with mock.patch('socket.socket') as mock_socket:
            #     mock_socket.return_value.recv.return_value = some_data
            #     t = TCPSocket()
            #     t.connect('example.com', 12345)
            # self.assertEqual(t.recv_bytes(), whatever_you_expect)
            # t.sock.connect.assert_called_with(('example.com', 12345))

        with self.subTest("Test correct argument"):
            with mock.patch("socket.socket") as mock_socket:
                # mock_socket.return_value.recv.return_value = some_data
                # t.sock.connect.assert_called_with(('example.com', 12345))
                mock_sock = mock_socket.return_value
                mock_sock.connect.return_value = None
                mock_sock.sendall.return_value = None
                mock_sock.recv.return_value = b"OK"

                # with mock.patch("threading.Thread") as mock_thread:
                client.send_urls(test_file)

            mock_socket.assert_called()

            # mock_sock.connect.assert_called_once_with(("localhost", 65001))
            # mock_sock.sendall.assert_called_with(b"https://google.com")

            # self.assertEqual(mock_thread.call_count, 4)

            os.remove(test_file)


if __name__ == "__main__":
    unittest.main()
