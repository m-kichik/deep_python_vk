import json
import time
import ujson

import cjson

from matplotlib import pyplot as plt

GRID = list(range(1, 1_00_000, 10_000))
small_test_str = '{"x": "x", "42": 42}'
small_test_dict = {"x": "x", "42": 42}
norm_test_str = (
    '{"hello": "world", "42": 42, "long int": 1000000000, "negative int": 42}'
)
norm_test_dict = {
    "hello": "world",
    "42": 42,
    "long int": 1000000000,
    "negative int": 42,
}
large_test_str = (
    "{"
    + '"name": "John Doe",'
    + '"age": 30,'
    + '"city": "Example City",'
    + '"isStudent": 0,'
    + '"grade": 80,'
    + '"course": "Math",'
    + '"employeeID": 123456,'
    + '"department": "Engineering",'
    + '"status": "active",'
    + '"projectName": "Phoenix",'
    + '"startDate": "2023-01-15",'
    + '"endDate": "2023-12-31",'
    + '"task": "Bug Fixing",'
    + '"taskHour": 40,'
    + '"mathGrade": 92,'
    + '"englishGrade": 88,'
    + '"historyGrade": 75,'
    + '"scienceGrade": 90,'
    + '"isPremiumMember": 1'
    + "}"
)

large_test_dict = {
    "name": "John Doe",
    "age": 30,
    "city": "Example City",
    "isStudent": 0,
    "grade": 80,
    "course": "Math",
    "employeeID": 123456,
    "department": "Engineering",
    "status": "active",
    "projectName": "Phoenix",
    "startDate": "2023-01-15",
    "endDate": "2023-12-31",
    "task": "Bug Fixing",
    "taskHour": 40,
    "mathGrade": 92,
    "englishGrade": 88,
    "historyGrade": 75,
    "scienceGrade": 90,
    "isPremiumMember": 1,
}


def study_loads(n_iters, test_str):
    start_t = time.time()
    for _ in range(n_iters):
        cjson.loads(test_str)
    cjson_t = time.time() - start_t

    start_t = time.time()
    for _ in range(n_iters):
        json.loads(test_str)
    json_t = time.time() - start_t

    start_t = time.time()
    for _ in range(n_iters):
        ujson.loads(test_str)
    ujson_t = time.time() - start_t

    return cjson_t, json_t, ujson_t


def study_dumps(n_iters, test_dict):
    start_t = time.time()
    for _ in range(n_iters):
        cjson.dumps(test_dict)
    cjson_t = time.time() - start_t

    start_t = time.time()
    for _ in range(n_iters):
        json.dumps(test_dict)
    json_t = time.time() - start_t

    start_t = time.time()
    for _ in range(n_iters):
        ujson.dumps(test_dict)
    ujson_t = time.time() - start_t

    return cjson_t, json_t, ujson_t


def draw_dep(data: dict, fname: str, plt_name: str = None):
    for k, v in data.items():
        plt.plot(GRID, v, label=k)
    plt.title(plt_name)
    plt.xlabel("N iterations")
    plt.ylabel("time, s")
    plt.legend()
    plt.grid()
    plt.savefig(fname)
    plt.clf()


def main():
    exp_size = "large"

    str_sizes = {
        "small": small_test_str,
        "norm": norm_test_str,
        "large": large_test_str,
    }

    dict_sizes = {
        "small": small_test_dict,
        "norm": norm_test_dict,
        "large": large_test_dict,
    }

    loads_times = list(zip(*[study_loads(n, str_sizes[exp_size]) for n in GRID]))
    loads_times_d = {
        "cjson time": loads_times[0],
        "json time": loads_times[1],
        "ujson time": loads_times[2],
    }
    draw_dep(
        loads_times_d,
        f"{exp_size}_size_loads_time.png",
        f"Function loads study for {exp_size} json size",
    )

    dumps_times = list(zip(*[study_dumps(n, dict_sizes[exp_size]) for n in GRID]))
    dumps_times_d = {
        "cjson time": dumps_times[0],
        "json time": dumps_times[1],
        "ujson time": dumps_times[2],
    }
    draw_dep(
        dumps_times_d,
        f"{exp_size}_size_dumps_time.png",
        f"Function dumps study for {exp_size} json size",
    )


if __name__ == "__main__":
    main()
