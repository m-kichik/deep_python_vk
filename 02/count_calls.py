import functools
import time
from typing import Callable


def mean(count: int = 10):
    def decorator_mean(function: Callable):
        execution_times = []

        @functools.wraps(function)
        def inner(*args, **kwargs):
            start_time = time.time()
            result = function(*args, **kwargs)
            execution_times.append(time.time() - start_time)

            if len(execution_times) > count:
                execution_times.pop(0)
            mean_time = sum(execution_times) / len(execution_times)

            print(
                f'Mean time of executing last {len(execution_times)}' +
                f'calls of {function.__name__} is {mean_time:.3e} s.'
            )
            return result

        return inner

    return decorator_mean


@mean()
def add_one(value: int) -> int:
    return value + 1


if __name__ == "__main__":
    for i in range(20):
        add_one(1)
