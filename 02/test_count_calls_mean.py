import re
import time

import unittest
from unittest.mock import patch
from count_calls_mean import mean, sleep_1s


class TestCountCallsMean(unittest.TestCase):
    def test_sleep_1s(self):
        epsilon = 1e-2
        start_time = time.time()
        sleep_1s()
        self.assertTrue(abs(time.time() - start_time - 1.0) < epsilon)

    def test_mean(self):
        n_calls = 2
        n_repetitions = 4
        mean_sleep_1s = mean(n_calls)(sleep_1s)

        with patch("builtins.print") as mock_print:
            for _ in range(n_repetitions):
                mean_sleep_1s()
            calls = [call[0][0] for call in mock_print.call_args_list]

        with self.subTest("Test printed text"):
            full_string_pattern = r"Mean time of executing last \d+ calls " +\
                r"of [A-Za-z0-9_]+ is \d\.\d+e[+-]\d+ s."
            for call in calls:
                self.assertTrue(re.search(full_string_pattern, call))

        with self.subTest("Test repetitions counting"):
            repetitions_pattern = r"\s+\d+\s+"
            repetions_count = [
                int(re.search(repetitions_pattern, call).group()) for call in calls
            ]
            ref_repetitions_count = list(range(1, n_calls + 1))
            ref_repetitions_count.extend([n_calls] * (n_repetitions - n_calls))
            self.assertEqual(repetions_count, ref_repetitions_count)

        with self.subTest("Test mean time counting"):
            epsilon = 1e-2
            time_pattern = r"\d\.\d+e[+-]\d+"
            mean_times = [
                float(re.search(time_pattern, call).group()) for call in calls
            ]
            allowed_mean_times = [int(abs(mt - 1.0) < epsilon) for mt in mean_times]
            self.assertEqual(sum(allowed_mean_times), len(allowed_mean_times))


if __name__ == "__main__":
    unittest.main()
