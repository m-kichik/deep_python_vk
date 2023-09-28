import contextlib
import os
from typing import TextIO


@contextlib.contextmanager
def fopen(file: str | TextIO, mode: str, encoding: str = "utf-8") -> TextIO:
    if isinstance(file, str):
        file = open(file, mode, encoding=encoding)
    try:
        yield file
    finally:
        file.close()


def words_in_line(line: str, words: list[str]) -> bool:
    return any(word.lower() in line.strip().lower().split() for word in words)


def search_word_in_line(file_to_seach: str | TextIO, words_to_search: list[str]) -> str:
    with fopen(file_to_seach, "r", encoding="utf-8") as file:
        for line in file:
            if line:
                if words_in_line(line, words_to_search):
                    yield line.strip()
            else:
                return "End of file"


if __name__ == "__main__":
    for good_line in search_word_in_line(
        os.path.abspath("01/alice_normal.txt"), ["сдержанна"]
    ):
        print(good_line)

    # 3G - file volume. Also works well, but too large for github.
    # with open(os.path.abspath('01/alice_normal_3G.txt'), 'r') as file:
    #     for line in search_word_in_line(file, ['сдержанна']):
    #         print(line)
