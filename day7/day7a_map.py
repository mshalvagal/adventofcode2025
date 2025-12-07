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

def solve(path):
    ans = 0
    with open(path) as f:
        input = f.read().strip().split('\n')

    grid = [list(line) for line in input]
    map = np.array(grid)
    
    start_col = np.where(map == 'S')[1][0]
    map[0, start_col] = '|'
    for row in range(1, map.shape[0]):
        for col in range(map.shape[1]):
            if map[row - 1, col] == '|':
                if map[row, col] == '.':
                    map[row, col] = '|'
                elif map[row, col] == '^':
                    ans += 1
                    if col > 0:
                        map[row, col - 1] = '|'
                    if col < map.shape[1] - 1:
                        map[row, col + 1] = '|'

    print(map)
    return int(ans)

EXAMPLE_ANS = 21

ex_ans = solve('./example1.txt')

if ex_ans == EXAMPLE_ANS:
    print("\nWorks on the example! Trying full case.\n")
    final_ans = solve('./input1.txt')
    print("=====>     ", final_ans, "     <=====\n")
else:
    print(f"\nDoes not work on the example, got {ex_ans} instead of {EXAMPLE_ANS}\n")
