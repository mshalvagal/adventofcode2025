import re
import typing
import math
from collections.abc import Iterable
import sys
import numpy as np

from z3 import *

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

def min_ops(target, sources):
    n = len(sources)
    s = Optimize()
    
    # 1. Define Variables (Int for counting operations)
    ops = [Int(f'op_{i}') for i in range(n)]

    # Constraint: You can't have negative operations
    for op in ops:
        s.add(op >= 0)

    # 2. Define Constraints
    for j in range(len(target)):
        # Gather switches that affect index j
        relevant_ops = [ops[i] for i in range(n) if sources[i][j]]
        
        if not relevant_ops:
            # If no switches touch this light, and we need it ON (1), it's impossible.
            if target[j] > 0:
                return math.inf
        else:
            # LOGIC CHANGE:
            # Since we start at 0, the sum of toggles must match the target parity.
            # Target 1 => Odd toggles needed (1, 3, 5...)
            # Target 0 => Even toggles needed (0, 2, 4...)
            s.add(Sum(relevant_ops) == int(target[j]))

    # 3. Objective: Minimize total operations
    s.minimize(Sum(ops))

    # 4. Solve
    if s.check() == sat:
        m = s.model()
        return sum(m[op].as_long() for op in ops)
    else:
        return math.inf
    
    
def solve(path):
    ans = 0
    with open(path) as f:
        input = f.read().strip().split('\n')
    
    for line in input:
        # find ints enclosed in {}
        joltage_target = re.search(r'\{(.*?)\}', line)
        joltage_target = list(map(int, joltage_target.group(1).split(',')))

        # find all integer groups enclosed in (), separated by commas
        joltage_sources = re.findall(r'\((.*?)\)', line)
        joltage_sources = [list(map(int, group.split(','))) for group in joltage_sources]
        # convert each group to one-hot integer by setting the indices to 1
        joltage_sources_bin = []
        for group in joltage_sources:
            group_spec = np.zeros(len(joltage_target), dtype=bool)
            for idx in group:
                group_spec[idx] = 1
            joltage_sources_bin.append(group_spec)
        joltage_sources_bin = np.array(joltage_sources_bin, dtype=bool)

        # print("Target: ", joltage_target)
        # print("Sources: ", joltage_sources_bin)
        ops_needed = min_ops(joltage_target, joltage_sources_bin)
        # print("Ops needed: ", ops_needed)
        ans += ops_needed

    return int(ans)

EXAMPLE_ANS = 33

ex_ans = solve('./example1.txt')

if ex_ans == EXAMPLE_ANS:
    print("\nWorks on the example! Trying full case.\n")
    final_ans = solve('./input1.txt')
    print("=====>     ", final_ans, "     <=====\n")
else:
    print(f"\nDoes not work on the example, got {ex_ans} instead of {EXAMPLE_ANS}\n")
