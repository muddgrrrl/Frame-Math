#!/usr/bin/env python3
"""Convert between a video frame number and elapsed time."""
import argparse
from fractions import Fraction
import re

ELAPSED = re.compile(r"(\d+):([0-5]\d):([0-5]\d)(\.\d+)?\Z")


def duration(value):
    match = ELAPSED.fullmatch(value)
    if match:
        h, m, s, fraction = match.groups()
        return Fraction(int(h) * 3600 + int(m) * 60 + int(s)) + Fraction(fraction or "0")
    return Fraction(value)


def timestamp(seconds):
    total = round(seconds * 1000)
    whole, fraction = divmod(total, 1000)
    hours, rest = divmod(whole, 3600)
    minutes, sec = divmod(rest, 60)
    return f"{hours:02}:{minutes:02}:{sec:02}.{fraction:03}"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fps", default="30000/1001", help="positive rate, e.g. 24 or 30000/1001")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--frame", type=int, help="zero-based frame number")
    source.add_argument("--elapsed", help="elapsed decimal seconds or H:MM:SS.sss")
    args = parser.parse_args()
    try:
        rate = Fraction(args.fps)
        if rate <= 0:
            raise ValueError("frame rate must be positive")
        if args.frame is not None:
            if args.frame < 0:
                raise ValueError("frame number must be nonnegative")
            seconds = args.frame / rate
            print(f"{timestamp(seconds)}  ({seconds} exact seconds)")
        else:
            seconds = duration(args.elapsed)
            if seconds < 0:
                raise ValueError("elapsed time must be nonnegative")
            print(round(seconds * rate))
    except (ValueError, ZeroDivisionError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
