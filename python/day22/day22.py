import re
import sys
import heapq
import math
import time
from collections import deque, defaultdict, Counter
from functools import cache
sys.setrecursionlimit(100000)
i = open("../../inputs/day22.txt").read().splitlines()

def manhat(curr, end):
    return abs(curr[0] - end[0]) + abs(curr[1] - end[1])


def is_in_bounds(point, max_x, max_y):
    return (0 <= point[0] <= max_x) and (0 <= point[1] <= max_y)


def is_int(a):
    b = math.floor(a + 0.5)
    # print(a, b, abs(a - b), sys.float_info.epsilon)
    return abs(a - b) < 0.001

m = 16777216
def play2(number, time, t = None, c = Counter()):
    if time == 0:
        return c
    orig = number
    number = ((number * 64) ^ number) % m
    number = ((number // 32) ^ number) % m
    number = ((number * 2048) ^ number) % m
    s = int(str(number)[-1]) - int(str(orig)[-1])
    if t and len(t) == 4:
        k = (t[0], t[1], t[2], t[3])
        if k not in c:
            c[k] = int(str(orig)[-1])
        t.popleft()
    if t is None:
        t = deque([s])
    else:
        t.append(s)
    return play2(number, time - 1, t, c)

def play3(number, time, t = None, c = Counter()):
    if time == 0:
        return c
    orig = number
    number = ((number << 6) ^ number) & 0xFFFFFF
    number = ((number >> 5) ^ number) & 0xFFFFFF
    number = ((number << 11) ^ number) & 0xFFFFFF
    s = number % 10 - orig % 10
    if t and len(t) == 4:
        k = (t[0], t[1], t[2], t[3])
        if k not in c:
            c[k] = orig % 10
        t.popleft()
    if t is None:
        t = deque([s])
    else:
        t.append(s)
    return play3(number, time - 1, t, c)

def play(number, time):
    if time == 0:
        return number
    number = ((number * 64) ^ number) % m
    number = ((number // 32) ^ number) % m
    number = ((number * 2048) ^ number) % m
    return play(number, time - 1)

def part1(lines):
    ans = 0
    for yi, line in enumerate(lines):
        ans += play(int(line), 2000)

    return ans

def part2(lines):
    all = Counter()
    s = time.time()
    for yi, line in enumerate(lines):
        all += play2(int(line), 2000, None, Counter())
    print("Original took: ", time.time() - s)
    s = time.time()
    all2 = Counter()
    for yi, line in enumerate(lines):
        all2 += play3(int(line), 2000, None, Counter())
    print("mod 10 took: ", time.time() - s)

    print(all.most_common(1)[0][1])
    print(all2.most_common(1)[0][1])
    return all.most_common(1)[0][1]

print("ans pt1:", part1(i))
print("***********part 2***************")
print(part2(i))
