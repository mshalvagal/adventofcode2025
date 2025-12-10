import re
import typing
import math
from collections.abc import Iterable
import sys
import numpy as np

from scipy.ndimage import binary_fill_holes

def lmap(func, *iterables):
    return list(map(func, *iterables))
def ints(s: str) -> typing.List[int]:
    return lmap(int, re.findall(r"-?\d+", s))
def positive_ints(s: str) -> typing.List[int]:
    return lmap(int, re.findall(r"\d+", s))
def floats(s: str) -> typing.List[float]:
    return lmap(float, re.findall(r"-?\d+(?:\.\d+)?", s))
def positive_floats(s: str) -> typing.List[float]:
    return lmap(float, re.findall(r"\d+(?:\.\d+)?", s))
def words(s: str) -> typing.List[str]:
    return re.findall(r"[a-zA-Z]+", s)
def alphanums(s: str) -> typing.List[str]:
    return re.findall(r"[a-zA-Z0-9]+", s)
def lfilter(func, *iterables):
    return list(filter(func, *iterables))
def pprint(a, name):
    print(f'\n{name}:\n{a}')

import random
from collections import defaultdict

def solve(path):
    with open(path) as f:
        points = [tuple(ints(line)) for line in f.read().strip().split('\n')]
    
    line_segments = [(points[i], points[(i + 1) % len(points)]) for i in range(len(points))]
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    ans = 0

    x_ranks = {x: i for i, x in enumerate(sorted(set(xs)))}
    y_ranks = {y: i for i, y in enumerate(sorted(set(ys)))}

    sorted_xs = sorted(x_ranks.keys())
    sorted_ys = sorted(y_ranks.keys())

    compressed_points = [(x_ranks[x]+1, y_ranks[y]+1) for x, y in points]
    max_x = len(x_ranks) + 2
    max_y = len(y_ranks) + 2

    grid = np.zeros((max_x, max_y), dtype=int)

    for (x1, y1), (x2, y2) in line_segments:
        x1_c = x_ranks[x1] + 1
        y1_c = y_ranks[y1] + 1
        x2_c = x_ranks[x2] + 1
        y2_c = y_ranks[y2] + 1

        grid[min(x1_c, x2_c):max(x1_c, x2_c)+1, min(y1_c, y2_c):max(y1_c, y2_c)+1] += 1

    filled_grid = binary_fill_holes(grid > 0)

    for p1 in compressed_points: 
        for p2 in compressed_points:
            (x1, y1) = p1
            (x2, y2) = p2

            if filled_grid[min(x1, x2):max(x1, x2)+1, min(y1, y2):max(y1, y2)+1].all():
                area = (abs(sorted_xs[x1-1] - sorted_xs[x2-1]) + 1) * (abs(sorted_ys[y1-1] - sorted_ys[y2-1]) + 1)
                ans = max(ans, area)

    return ans

EXAMPLE_ANS = 24

ex_ans = solve('./example1.txt')

if ex_ans == EXAMPLE_ANS:
    print("\nWorks on the example! Trying full case.\n")
    final_ans = solve('./input1.txt')
    print("=====>     ", final_ans, "     <=====\n")
else:
    print(f"\nDoes not work on the example, got {ex_ans} instead of {EXAMPLE_ANS}\n")
