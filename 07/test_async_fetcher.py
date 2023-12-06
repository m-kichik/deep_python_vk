import os
import unittest
from unittest.mock import patch, call
import asyncio
from async_fetcher import AsyncFetcher


class TestAsyncFetcher(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        urls = ["https://google.com", "https://vk.company", "https://home.vk.team"]
        self.test_file = os.path.abspath("test_urls.txt")
        with open(self.test_file, "w") as file:
            file.write("\n".join(urls))

    def tearDown(self):
        os.remove(self.test_file)

    def test_creation(self):
        with self.subTest("Test default"):
            async_fetcher = AsyncFetcher()
            self.assertEqual(async_fetcher.num_workers, 4)

        with self.subTest("Test not default"):
            async_fetcher = AsyncFetcher(8)
            self.assertEqual(async_fetcher.num_workers, 8)

    @patch("aiohttp.ClientSession.get")
    async def test_fetch_url(self, mock_session_get):
        mock_session_get.return_value.__aenter__.return_value.status = 200

        async_fetcher = AsyncFetcher()
        url = "http://example.com"

        result = await async_fetcher.fetch_url(url)
        self.assertEqual(result, 200)
        mock_session_get.assert_called_once_with("http://example.com", timeout=3)

    @patch("async_fetcher.AsyncFetcher.fetch_url")
    async def test_producer(self, mock_fetch_url):
        mock_fetch_url.return_value = 200
        async_fetcher = AsyncFetcher()

        url = "http://example.com"
        input_queue = asyncio.Queue()
        await input_queue.put(url)
        output_queue = asyncio.Queue()

        task = asyncio.create_task(async_fetcher.producer(input_queue, output_queue))
        await input_queue.join()
        task.cancel()
        try:
            await task
        except asyncio.exceptions.CancelledError:
            pass

        self.assertEqual(mock_fetch_url.mock_calls, [call(url)])
        self.assertEqual(await output_queue.get(), 200)

    @patch("builtins.print")
    async def test_consumer(self, mock_print):
        async_fetcher = AsyncFetcher()

        retval = 200
        input_queue = asyncio.Queue()
        await input_queue.put(retval)

        task = asyncio.create_task(async_fetcher.consumer(input_queue))
        await input_queue.join()
        task.cancel()
        try:
            await task
        except asyncio.exceptions.CancelledError:
            pass

        self.assertEqual(mock_print.mock_calls, [call(200)])

    @patch("aiohttp.ClientSession.get")
    @patch("builtins.print")
    async def test_batch_fetch_ie_full_pipeline(self, mock_print, mock_session_get):
        mock_session_get.return_value.__aenter__.return_value.status = 200
        async_fetcher = AsyncFetcher(42)
        await async_fetcher.batch_fetch(self.test_file)

        self.assertIn(
            call("https://google.com", timeout=3), mock_session_get.mock_calls
        )
        self.assertIn(
            call("https://vk.company", timeout=3), mock_session_get.mock_calls
        )
        self.assertIn(
            call("https://home.vk.team", timeout=3), mock_session_get.mock_calls
        )
        self.assertEqual([call(200), call(200), call(200)], mock_print.mock_calls)


if __name__ == "__main__":
    unittest.main()
