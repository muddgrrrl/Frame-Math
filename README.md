# Frame Math

Translate elapsed time into a zero-based video frame number and back using exact rational frame rates.

```sh
python3 frame_math.py --fps 30000/1001 --frame 30000
python3 frame_math.py --fps 24000/1001 --elapsed 00:01:12.500
```

Requires Python 3.8+. Elapsed output shows a clock rounded to milliseconds and an exact fraction in seconds. Converting elapsed time selects the nearest frame, with ties rounded to the even frame. The clock is elapsed time. It does not interpret SMPTE drop-frame labels. [MIT](LICENSE)
