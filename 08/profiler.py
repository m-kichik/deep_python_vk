import copy
import inspect
from typing import Callable

from memory_profiler import memory_usage


def profile_deco(function):
    class ProfileDecoClass:
        def __init__(self, function: Callable):
            self.function = function
            self.source_code = inspect.getsource(function).splitlines()
            self.n_lines = len(self.source_code)
            self.calls = {}
            self.call_count = 0

        def __call__(self, *args, **kwargs):
            self.call_count += 1
            result = memory_usage(
                (self.function, copy.deepcopy(args), copy.deepcopy(kwargs))
            )
            self.calls[self.call_count] = result
            return self.function(*args, **kwargs)

        def print_stat(self):
            calls = "call" if self.call_count == 1 else "calls"
            format_string = "{:<20} | {:<20} | {:<20}"
            print(
                f"***Function {self.function.__name__} memory usage for {self.call_count} {calls}***"
            )
            for call_n, call_res in self.calls.items():
                print(f"Call {call_n}:")
                print(format_string.format("-" * 20, "-" * 20, "-" * 20))
                print(format_string.format("Memory Usage", "Increment", "Line content"))
                print(format_string.format("-" * 20, "-" * 20, "-" * 20))
                mem = 0.0
                for i in range(self.n_lines):
                    print(
                        format_string.format(
                            call_res[i],
                            call_res[i] - mem,
                            call_res[i],
                        )
                    )
                    mem += call_res[i] - mem
                print(format_string.format("-" * 20, "-" * 20, "-" * 20))

    return ProfileDecoClass(function)


@profile_deco
def add(a, b):
    return a + b


@profile_deco
def sub(a, b):
    return a - b


def main():
    add(1, 2)
    add(4, 5)
    sub(4, 5)

    add.print_stat()
    print()
    sub.print_stat()


if __name__ == "__main__":
    main()