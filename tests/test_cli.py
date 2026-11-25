import subprocess
import sys
import unittest


def cli(*args):
    return subprocess.run([sys.executable, "frame_math.py", *args], text=True, capture_output=True)


class FrameMathTests(unittest.TestCase):
    def test_ntsc_duration_keeps_exact_fraction(self):
        result = cli("--frame", "1")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "00:00:00.033  (1001/30000 exact seconds)\n")

    def test_elapsed_rounds_ties_to_even(self):
        for seconds, frame in (("0.25", "0"), ("0.75", "2")):
            with self.subTest(seconds=seconds):
                result = cli("--fps", "2", "--elapsed", seconds)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout.strip(), frame)

    def test_zero_rate_is_a_usage_error(self):
        result = cli("--fps", "0", "--frame", "1")
        self.assertEqual(result.returncode, 2)
        self.assertIn("frame rate must be positive", result.stderr)
