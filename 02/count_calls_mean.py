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
                f"Mean time of executing last {len(execution_times)} "
                + f"calls of {function.__name__} is {mean_time:.6e} s."
            )
            return result

        return inner

    return decorator_mean


def sleep_1s() -> None:
    time.sleep(1.0)


if __name__ == "__main__":
    mean_sleep_1s = mean(10)(sleep_1s)

    for _ in range(10):
        mean_sleep_1s()
