import re
import typing
import math
from collections.abc import Iterable
import sys
import numpy as np

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

def propagate(map, pos, direction):
    x, y = pos
    dx, dy = direction
    boundary = False
    while True:
        x += dx
        y += dy
        if x < 0 or y < 0 or x >= map.shape[0] or y >= map.shape[1]:
            boundary = True
            break
        if map[x, y] == '#':
            pos = (x - dx, y - dy)
            direction = (dy, -dx)
            break
        if map[x, y] == '.':
            map[x, y] = 'X'
    return boundary, map, pos, direction

def solve(path):
    ans = 0
    with open(path) as f:
        input = f.read().strip().split('\n')

    grid = [list(line) for line in input]
    map = np.array(grid)
    
    light_cols = {np.where(map == 'S')[1][0]: 1}
    for row in range(1, map.shape[0]):
        new_light_cols = defaultdict(int)
        for col, count in light_cols.items():
            if map[row, col] == '.':
                if col not in new_light_cols:
                    new_light_cols[col] = count
                else:
                    new_light_cols[col] += count
            elif map[row, col] == '^':
                if col > 0:
                    if col - 1 not in new_light_cols:
                        new_light_cols[col - 1] = count
                    else:
                        new_light_cols[col - 1] += count
                if col < map.shape[1] - 1:
                    if col + 1 not in new_light_cols:
                        new_light_cols[col + 1] = count
                    else:
                        new_light_cols[col + 1] += count
        light_cols = new_light_cols
    
    for count in light_cols.values():
        ans += count
    
    return int(ans)

EXAMPLE_ANS = 40

ex_ans = solve('./example1.txt')

if ex_ans == EXAMPLE_ANS:
    print("\nWorks on the example! Trying full case.\n")
    final_ans = solve('./input1.txt')
    print("=====>     ", final_ans, "     <=====\n")
else:
    print(f"\nDoes not work on the example, got {ex_ans} instead of {EXAMPLE_ANS}\n")
