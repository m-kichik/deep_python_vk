import cProfile
import pstats
from typing import Callable


def profile_deco(function):
    class ProfileDecoClass:
        def __init__(self, function: Callable):
            self.profiler = cProfile.Profile()
            self.function = function
            self.__name__ = function.__name__

        def __call__(self, *args, **kwargs):
            result = self.profiler.runcall(self.function, *args, **kwargs)

            return result

        def print_stat(self):
            print(f"\t\t***Function {self.function.__name__} stats***")
            stats = pstats.Stats(self.profiler).sort_stats(pstats.SortKey.TIME)
            stats.print_stats()

    return ProfileDecoClass(function)


# @profile_deco
def add(a, b):
    return a + b


# @profile_deco
def sub(a, b):
    return a - b


@profile_deco
def strange_func(a, b):
    for _ in range(1_000_000):
        sub(a, b)
        add(a, b)


def main():
    #     add(1, 2)
    #     add(4, 5)
    #     sub(4, 5)

    strange_func(4, 2)
    strange_func.print_stat()
    # add.print_stat()
    # sub.print_stat()


if __name__ == "__main__":
    main()
