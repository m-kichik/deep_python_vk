import time
from typing import Callable
import weakref

import random

random.seed(42)

from memory_profiler import profile


class Mouse:
    def __init__(self, name: str):
        self.name = name


class NormalCat:
    def __init__(self, last_mouse: Mouse, answer: Callable):
        self.last_mouse = last_mouse
        self.answer = answer


class SlotCat:
    __slots__ = ("last_mouse", "answer")

    def __init__(self, last_mouse: Mouse, answer: Callable):
        self.last_mouse = last_mouse
        self.answer = answer


class WeakCat:
    def __init__(self, last_mouse: Mouse, answer: Callable):
        self.last_mouse = weakref.ref(last_mouse)
        self.answer = weakref.ref(answer)


@profile
def compare_creation_from_existed(n_instances: int = 10_000_000):
    mice = [Mouse("average_mouce"), Mouse("average_mouce"), Mouse("ran_away_mouce")]
    answers = [lambda: "mew", lambda: "mrr", lambda: "mau"]

    start_time = time.time()
    normals = [NormalCat(mice[0], answers[0]) for _ in range(n_instances)]
    normal_time = time.time() - start_time
    print(f"normal: {normal_time:.6f} s")
    del normals

    start_time = time.time()
    slots = [SlotCat(mice[1], answers[1]) for _ in range(n_instances)]
    slot_time = time.time() - start_time
    print(f"slot:   {slot_time:.6f} s")
    del slots

    start_time = time.time()
    weaks = [WeakCat(mice[2], answers[2]) for _ in range(n_instances)]
    weak_time = time.time() - start_time
    print(f"weak:   {weak_time:.6f} s")
    del weaks


@profile
def compare_creation_with_new(n_instances: int = 10_000_000):
    start_time = time.time()
    normals = [
        NormalCat(Mouse("small_mouce"), lambda: "mew") for _ in range(n_instances)
    ]
    normal_time = time.time() - start_time
    print(f"normal: {normal_time:.6f} s")
    del normals

    start_time = time.time()
    slots = [SlotCat(Mouse("average_mouce"), lambda: "mrr") for _ in range(n_instances)]
    slot_time = time.time() - start_time
    print(f"slot:   {slot_time:.6f} s")
    del slots

    start_time = time.time()
    weaks = [
        WeakCat(Mouse("ran_away_mouce"), lambda: "mau") for _ in range(n_instances)
    ]
    weak_time = time.time() - start_time
    print(f"weak:   {weak_time:.6f} s")
    del weaks


def compare_access_mouse_name(n_iterations: int = 10_000_000):
    mice = ["small_mouce", "big_mouse", "average_mouse", "strange_mouce"]

    norm_cat = NormalCat(Mouse(random.choice(mice)), lambda: "mew")
    start_time = time.time()
    for _ in range(n_iterations):
        name = norm_cat.last_mouse.name
    normal_time = time.time() - start_time
    print(f"normal: {normal_time:.6f} s")

    slot_cat = SlotCat(Mouse(random.choice(mice)), lambda: "mrr")
    start_time = time.time()
    for _ in range(n_iterations):
        name = slot_cat.last_mouse.name
    slot_time = time.time() - start_time
    print(f"slot:   {slot_time:.6f} s")

    mouse = Mouse(random.choice(mice))
    weak_cat = WeakCat((mouse), lambda: "mau")
    start_time = time.time()
    for _ in range(n_iterations):
        name = weak_cat.last_mouse().name
        weak_time = time.time() - start_time
    print(f"weak:   {weak_time:.6f} s")


def compare_change_mouse_name(n_iterations: int = 10_000_000):
    mice = ["small_mouce", "big_mouse", "average_mouse", "strange_mouce"]

    norm_cat = NormalCat(Mouse(random.choice(mice)), lambda: "mew")
    start_time = time.time()
    for _ in range(n_iterations):
        norm_cat.last_mouse.name = random.choice(mice)
    normal_time = time.time() - start_time
    print(f"normal: {normal_time:.6f} s")

    slot_cat = SlotCat(Mouse(random.choice(mice)), lambda: "mrr")
    start_time = time.time()
    for _ in range(n_iterations):
        slot_cat.last_mouse.name = random.choice(mice)
    slot_time = time.time() - start_time
    print(f"slot:   {slot_time:.6f} s")

    mouse = Mouse(random.choice(mice))
    weak_cat = WeakCat((mouse), lambda: "mau")
    start_time = time.time()
    for _ in range(n_iterations):
        weak_cat.last_mouse().name = random.choice(mice)
    weak_time = time.time() - start_time
    print(f"weak:   {weak_time:.6f} s")


def study_time(n: int = 10_000_000):
    print(f"Creation time for {n} instances with existed args")
    compare_creation_from_existed(n)
    print()
    print(f"Creation time for {n} instances with new args")
    compare_creation_with_new(n)
    print()
    print(f"Attribute access time for {n} instances")
    compare_access_mouse_name(n)
    print()
    print(f"Attribute change time for {n} instances")
    compare_change_mouse_name(n)


def main():
    n = 100_000
    study_time(n)


if __name__ == "__main__":
    main()
