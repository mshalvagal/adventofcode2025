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
    
    # 1. Define Variables (Bool is best for 0/1 toggles)
    ops = [Bool(f'op_{i}') for i in range(n)]

    # 2. Define Constraints
    for j in range(len(target)):
        # Gather switches that affect index j
        relevant_ops = [ops[i] for i in range(n) if sources[i][j]]
        
        # We need to convert Bools to 0/1 integers to sum them
        # If(op, 1, 0) transforms True->1, False->0
        active_switches = [If(op, 1, 0) for op in relevant_ops]
        
        if not active_switches:
            # If no switches touch this light, and we need it ON (1), it's impossible.
            if target[j] == 1:
                return math.inf
        else:
            # Target 1 => Odd toggles needed (1, 3, 5...)
            # Target 0 => Even toggles needed (0, 2, 4...)
            s.add(Sum(active_switches) % 2 == int(target[j]))

    # 3. Objective: Minimize total operations
    s.minimize(Sum([If(op, 1, 0) for op in ops]))

    # 4. Solve
    if s.check() == sat:
        m = s.model()
        return sum(1 for op in ops if is_true(m[op]))
    else:
        return math.inf
    
    
def solve(path):
    ans = 0
    with open(path) as f:
        input = f.read().strip().split('\n')
    
    for line in input:
        # find string enclosed in []
        light_target = re.search(r'\[(.*?)\]', line)
        # convert to binary string by replacing . with 0 and # with 1
        light_target = light_target.group(1).replace('.', '0').replace('#', '1')
        light_target_bin = np.array(list(map(int, light_target)), dtype=bool)

        # find all integer groups enclosed in (), separated by commas
        light_sources = re.findall(r'\((.*?)\)', line)
        light_sources = [list(map(int, group.split(','))) for group in light_sources]
        # convert each group to binary string by setting the indices to 1
        light_sources_bin = []
        for group in light_sources:
            group_spec = np.zeros(len(light_target), dtype=bool)
            for idx in group:
                group_spec[idx] = 1
            light_sources_bin.append(group_spec)
        light_sources_bin = np.array(light_sources_bin, dtype=bool)

        # print("Target: ", light_target_bin)
        # print("Sources: ", light_sources_bin)
        ops_needed = min_ops(light_target_bin, light_sources_bin)
        # print("Ops needed: ", ops_needed)
        ans += ops_needed

    return int(ans)

EXAMPLE_ANS = 7

ex_ans = solve('./example1.txt')

if ex_ans == EXAMPLE_ANS:
    print("\nWorks on the example! Trying full case.\n")
    final_ans = solve('./input1.txt')
    print("=====>     ", final_ans, "     <=====\n")
else:
    print(f"\nDoes not work on the example, got {ex_ans} instead of {EXAMPLE_ANS}\n")
