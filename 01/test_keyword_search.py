import unittest
from io import StringIO
from keyword_search import fopen, words_in_line, search_word_in_line


class TestFileOperations(unittest.TestCase):
    def test_fopen_with_file(self):
        with self.subTest("Test fopen for reading with file"):
            with fopen("test_file.txt", "r") as file:
                self.assertTrue(file.readable())

        with self.subTest("Test fopen for writing with file"):
            with fopen("test_file.txt", "w") as file:
                self.assertTrue(file.writable())

        with self.subTest("Test fopen for reading with file object"):
            with StringIO("test text") as text_io:
                with fopen(text_io, "r") as file:
                    self.assertTrue(file.readable())

        with self.subTest("Test fopen for writing with file object"):
            with StringIO("test text") as text_io:
                with fopen(text_io, "w") as file:
                    self.assertTrue(file.writable())

    def test_words_in_line(self):
        line = "The Ultimate Question of Life the Universe and Everything"

        with self.subTest("Test mathing registers"):
            self.assertTrue(words_in_line(line, ["question"]))

        with self.subTest("Test non-mathing registers"):
            self.assertTrue(words_in_line(line, ["Question"]))

        with self.subTest("Test several words"):
            self.assertTrue(words_in_line(line, ["life", "universe", "everything"]))

        with self.subTest("Test not presented words"):
            self.assertFalse(words_in_line(line, ["answer"]))

        with self.subTest("Test part of a word"):
            self.assertFalse(words_in_line(line, ["very"]))

    def test_search_word_in_line(self):
        text = """
        The computer answered 42
        Forty two screeched Lunkquool
        And thats all you can say after seven and a half million years of work
        I checked everything very carefully said the computer and I declare with all
        certainty that this is the Answer
        It seems to me to be absolutely honest with you that the whole point is that
        you yourself did not know what the Question was
        """

        with self.subTest("Test presented word"):
            with StringIO(text) as text_io:
                result = list(search_word_in_line(text_io, ["computer"]))
                self.assertEqual(
                    result,
                    [
                        "The computer answered 42",
                        "I checked everything very carefully said the computer and I declare with all",
                    ],
                )

        with self.subTest("Test not presented word"):
            with StringIO(text) as text_io:
                result = list(search_word_in_line(text_io, ["Universe"]))
                self.assertEqual(result, [])

        with self.subTest("Test StopIteration"):
            with StringIO() as text_io:
                gen = search_word_in_line(text_io, ["test"])
                with self.assertRaises(StopIteration):
                    self.assertEqual(next(gen), "End of file")


if __name__ == "__main__":
    unittest.main()
