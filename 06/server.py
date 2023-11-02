import argparse
import json
import multiprocessing
import re
import requests
import socket


class Server:
    def __init__(
        self,
        n_words: int,
        host: str = "localhost",
        port: int = 65001,
        n_workers: int = 1,
    ) -> None:
        self.n_words = n_words
        self.host = host
        self.port = port
        self.n_workers = n_workers
        self.n_calls = 0

    def callback(self, *args) -> None:
        self.n_calls += 1
        print(f"Processed {self.n_calls} calls")

    def count_words(self, line: str) -> dict:
        words = re.findall(r"\w+", line)
        words_dict = dict()

        for word in words:
            words_dict[word] = words_dict.get(word, 0) + 1

        top_words = set(
            sorted(words_dict.keys(), key=lambda x: words_dict[x], reverse=True)[
                : self.n_words
            ]
        )
        return {k: v for (k, v) in words_dict.items() if k in top_words}

    def worker(self, connection) -> None:
        data = connection.recv(1024)
        url = data.decode("utf-8")
        try:
            resp = requests.get(url, timeout=3)
            top_words = self.count_words(resp.text)
            connection.sendall(json.dumps(top_words).encode("utf-8"))
        except:
            connection.sendall(b"{}")
        finally:
            connection.close()
            return url

    def work(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as master:
            master.bind((self.host, self.port))
            master.listen()

            with multiprocessing.Pool(self.n_workers) as pool:
                while True:
                    connection, _ = master.accept()
                    pool.apply_async(self.worker, (connection,), callback=self.callback)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", type=int, help="Number of workers")
    parser.add_argument("-k", type=int, help="Number of words to count")
    args = parser.parse_args()
    workers, words = args.w, args.k

    server = Server(words, n_workers=workers)
    server.work()


if __name__ == "__main__":
    main()
