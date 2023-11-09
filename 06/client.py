import argparse
import os
import socket
import threading


class Client:
    def __init__(
        self, host: str = "localhost", port: int = 65001, n_threads: int = 1
    ) -> None:
        self.host = host
        self.port = port
        self.n_threads = n_threads

    def send_urls(self, urls_file: str) -> None:
        def fetch_urls(urls_):
            while len(urls_):
                url = urls_.pop()  # list is thread safe

                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.connect((self.host, self.port))
                    sock.sendall(url.encode("utf-8"))
                    data = sock.recv(1024)
                    message = data.decode("utf-8")
                    print(f"{url}: {message}")

        if not isinstance(urls_file, str):
            raise ValueError(f"Urls file have to be string, got {urls_file} instead")

        if not os.path.exists(urls_file):
            raise FileNotFoundError(f"No such file: {os.path.abspath(urls_file)}")

        with open(urls_file, "r") as file:
            urls = file.read().splitlines()

        threads = [
            threading.Thread(
                target=fetch_urls,
                name=f"fetch-{i}",
                args=(urls,),
            )
            for i in range(self.n_threads)
        ]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "num_threads", type=int, default=1, help="Number of client threads"
    )
    parser.add_argument("urls_file", type=str, help="File with URLs")
    args = parser.parse_args()
    urls_file, num_threads = args.urls_file, args.num_threads

    client = Client(n_threads=num_threads)
    client.send_urls(urls_file)


if __name__ == "__main__":
    main()
