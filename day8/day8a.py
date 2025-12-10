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

def solve(path, n):
    ans = 0
    with open(path) as f:
        input = f.read().strip().split('\n')
    
    positions = np.array([[int(x) for x in line.split(',')] for line in input])
    
    pairwise_distances = np.linalg.norm(positions[:, np.newaxis, :] - positions[np.newaxis, :, :], axis=-1)
    pairwise_distances = np.triu(pairwise_distances, k=1)
    pairwise_distances[pairwise_distances == 0] = np.inf

    circuits = []

    for _ in range(n):
        i, j = np.unravel_index(np.argmin(pairwise_distances), pairwise_distances.shape)
        pairwise_distances[i, j] = np.inf
        circuits.append([i, j])

    merged_circuits = []
    while len(circuits) > 0:
        first, *rest = circuits
        first = set(first)
        changed = True
        while changed:
            changed = False
            for other in rest[:]:
                if len(first.intersection(set(other))) > 0:
                    first.update(other)
                    rest.remove(other)
                    changed = True
        merged_circuits.append(first)
        circuits = rest
    
    # print(f'Merged circuits: {merged_circuits}')

    ans = 1
    sizes = [len(c) for c in merged_circuits]
    sorted_sizes = sorted(sizes, reverse=True)
    ans = sorted_sizes[0] * sorted_sizes[1] * sorted_sizes[2]

    return int(ans)

EXAMPLE_ANS = 40

ex_ans = solve('./example1.txt', 10)

if ex_ans == EXAMPLE_ANS:
    print("\nWorks on the example! Trying full case.\n")
    final_ans = solve('./input1.txt', 1000)
    print("=====>     ", final_ans, "     <=====\n")
else:
    print(f"\nDoes not work on the example, got {ex_ans} instead of {EXAMPLE_ANS}\n")
