import argparse
import asyncio
from typing import Any

import aiohttp


class AsyncFetcher:
    async def fetch_url(self, url: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=3) as resp:
                return resp.status

    async def producer(self, input: Any, output: Any) -> None:
        while True:
            url = await input.get()
            try:
                await output.put(await self.fetch_url(url))
            finally:
                input.task_done()

    async def consumer(self, input: Any) -> None:
        while True:
            result = await input.get()

            print(result)
            input.task_done()

    async def batch_fetch(self, urls_file: str, num_workers: int = 4) -> None:
        with open(urls_file, "r") as file:
            urls = file.read().splitlines()

        url_queue = asyncio.Queue()
        status_queue = asyncio.Queue()

        workers = [
            asyncio.create_task(self.producer(url_queue, status_queue))
            for _ in range(num_workers)
        ]
        workers.append(asyncio.create_task(self.consumer(status_queue)))
        for url in urls:
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

    fetcher = AsyncFetcher()
    await fetcher.batch_fetch(filename, n_workers)


if __name__ == "__main__":
    asyncio.run(main())
