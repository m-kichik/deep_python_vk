import argparse
import asyncio
from typing import Any

import aiohttp


class AsyncFetcher:
    def __init__(self, num_workers: int = 4):
        self.num_workers = num_workers

    async def fetch_url(self, url: str) -> str:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=3) as resp:
                    return resp.status
        except Exception as err:
            print(f"{err} occured in fetch_url")
            return 418

    async def producer(self, input: Any, output: Any) -> None:
        while True:
            try:
                url = await input.get()
                try:
                    await output.put(await self.fetch_url(url))
                finally:
                    input.task_done()
            except Exception as err:
                print(f"{err} occured, continue work")

    async def consumer(self, input: Any) -> None:
        while True:
            try:
                result = await input.get()
                print(result)
                input.task_done()
            except Exception as err:
                print(f"{err} occured in consumer, continue working")

    async def batch_fetch(self, urls_file: str) -> None:
        url_queue = asyncio.Queue()
        status_queue = asyncio.Queue()

        workers = [
            asyncio.create_task(self.producer(url_queue, status_queue))
            for _ in range(self.num_workers)
        ]
        workers.append(asyncio.create_task(self.consumer(status_queue)))
        with open(urls_file, "r") as file:
            while url := file.readline():
                url = url.strip()
                await url_queue.put(url)

        await url_queue.join()
        await status_queue.join()

        for worker in workers:
            worker.cancel()


async def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-c", type=int, help="Number of workers")
    parser.add_argument("urls", type=str, help="File with URLs")
    args = parser.parse_args()
    n_workers, filename = args.c, args.urls

    fetcher = AsyncFetcher(n_workers)
    await fetcher.batch_fetch(filename)


if __name__ == "__main__":
    asyncio.run(main())
