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

def check_valid(nums, rules, rules_2):
    for i in range(len(nums)):
        if nums[i] in rules.keys():
            for j in rules[nums[i]]:
                if j in nums[:i]:
                    return False
        if nums[i] in rules_2.keys():
            for j in rules_2[nums[i]]:
                if j in nums[i+1:]:
                    return False
    return True

def solve(path):
    ans = 0
    with open(path) as f:
        input = f.read().strip().split('\n')

    ranges = []
    for i, line in enumerate(input):
        if line == '':
            rest_lines = input[i+1:]
            break
        parts = line.split('-')
        ranges.append((int(parts[0]), int(parts[1])))

    ranges.sort(key=lambda x: x[0])
    merged_ranges = []
    flexi_start, flexi_end = ranges[0]
    for start, end in ranges[1:]:
        if start <= flexi_end + 1:
            flexi_end = max(flexi_end, end)
        else:
            merged_ranges.append((flexi_start, flexi_end))
            flexi_start, flexi_end = start, end
    merged_ranges.append((flexi_start, flexi_end))

    for range_start, range_end in merged_ranges:
        ans += (range_end - range_start + 1)
    return int(ans)

EXAMPLE_ANS = 14

ex_ans = solve('./example1.txt')

if ex_ans == EXAMPLE_ANS:
    print("\nWorks on the example! Trying full case.\n")
    final_ans = solve('./input1.txt')
    print("=====>     ", final_ans, "     <=====\n")
else:
    print(f"\nDoes not work on the example, got {ex_ans} instead of {EXAMPLE_ANS}\n")
