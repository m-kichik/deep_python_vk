import random
import re


def main():
    with open("../06/Strugackiy_Ponedelnik-nachinaetsya-v-subbotu.txt", "r") as file:
        book = file.read()

    words = list(
        {
            word.lower()
            for word in re.sub(r"[^А-Яа-яё\s]", "", book).strip().split()
            if len(word) > 4
        }
    )
    random_100 = random.choices(words, k=100)

    pattern = "https://www.google.com/search?q="

    with open("100_urls.txt", "w") as file:
        for word in random_100:
            file.write(pattern + word + "\n")


if __name__ == "__main__":
    main()
