# Performance for 2025

This was developed and ran on an Intel(R) Core(TM) i3-3217U CPU @ 1.80GHz
from Q2/2012, 16GB RAM, running Arch Linux and Python 3.13.7 + Gleam 1.13.0.

## Python

This is just `time python day01.py ...` while stripping stdout output where needed.
The system was idling, but X and Firefox were running.

Day 10 was ran via `uv run --with numpy --with scipy day10py ...`

Without further optimization only 3 days were slower than 1 second.

## Gleam

Normal release build, stdout stripped as needed.

| Day | Python P 1 | P2 | Gleam P1 | P2 |
| - | - | - | - | - |
| 1 | 0.05s | 0.26s | 0.68s | - |
| 2 | 7.23s | 68.13s | 16.5s | - |
| 3 | 0.07s | - | - | - |
| 4 | 0.17s | 0.02s | 4.44s | - |
| 5 | 0.07s | 0.06s | 0.15s | 0.16s |
| 6 | 0.02s | 0.01s | 0.14s | 0.14s |
| 7 | 0.06s | 0.06s | - | - |
| 8 | 42.39s | 56.66s | - | - |
| 9 | 0.44s | 2.94s | - | - |
| 10 | 2.01s | 2.56s | - | - |
| 11 | 0.06s | 0.05s | - | - |
| 12 | 0.08s | . | - | . |
