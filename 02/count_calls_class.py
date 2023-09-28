import functools
from typing import Callable

class mean():
    def __init__(self, function: Callable):
        functools.update_wrapper(self, function)
        self.function = function
        self.repeats  = 0

    def __call__(self, count=10):
        pass