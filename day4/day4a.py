import re
import typing
import math
from collections.abc import Iterable
import sys
import numpy as np
from scipy.signal import convolve2d

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

def count_xmas(line):
    matches = re.findall(r'XMAS', line)
    matches_reverse = re.findall(r'SAMX', line)
    return len(matches) + len(matches_reverse)

def solve(path):
    ans = 0
    with open(path) as f:
        input = f.read().strip().split('\n')
    
    # convert to numpy array
    input = np.array([list(x) for x in input])

    # convert @ to 1 and . to 0
    input = np.where(input == '@', 1, 0)
    input = input.astype(int)

    filter = np.ones((3, 3), dtype=int)
    filter[1, 1] = 0  # center is not counted
    
    convolved = convolve2d(input, filter, mode='same')
    convolved = convolved * input

    result = np.zeros_like(convolved)
    result[convolved < 4] = 1
    result[convolved == 0] = 0

    print(result)

    ans = np.sum(result)

    return int(ans)

EXAMPLE_ANS = 13

ex_ans = solve('./example1.txt')

if ex_ans == EXAMPLE_ANS:
    print("\nWorks on the example! Trying full case.\n")
    final_ans = solve('./input1.txt')
    print("=====>     ", final_ans, "     <=====\n")
else:
    print(f"\nDoes not work on the example, got {ex_ans} instead of {EXAMPLE_ANS}\n")
import re
import typing
import math
from collections.abc import Iterable
import sys
import numpy as np
from scipy.signal import convolve2d

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

def count_xmas(line):
    matches = re.findall(r'XMAS', line)
    matches_reverse = re.findall(r'SAMX', line)
    return len(matches) + len(matches_reverse)

def solve(path):
    ans = 0
    with open(path) as f:
        input = f.read().strip().split('\n')
    
    # convert to numpy array
    input = np.array([list(x) for x in input])

    # convert @ to 1 and . to 0
    input = np.where(input == '@', 1, 0)
    input = input.astype(int)

    filter = np.ones((3, 3), dtype=int)
    filter[1, 1] = 0  # center is not counted
    
    convolved = convolve2d(input, filter, mode='same')
    convolved = convolved * input

    result = (convolved < 4).astype(int) & (input == 1).astype(int)

    ans = np.sum(result)

    return int(ans)

EXAMPLE_ANS = 13

ex_ans = solve('./example1.txt')

if ex_ans == EXAMPLE_ANS:
    print("\nWorks on the example! Trying full case.\n")
    final_ans = solve('./input1.txt')
    print("=====>     ", final_ans, "     <=====\n")
else:
    print(f"\nDoes not work on the example, got {ex_ans} instead of {EXAMPLE_ANS}\n")
