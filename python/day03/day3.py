import re
import heapq
from collections import deque, defaultdict, Counter


input = open("../../inputs/day3.txt").readlines()


def part1(lines):
    ans = 0
    for line in lines:
        matches = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", line)
        ans += sum((int(a) * int(b) for a, b in matches))

    return ans


def find_all(s, sub, start):
    idx = s.find(sub, start)
    if idx == -1:
        return None
    more = find_all(s, sub, idx + 1)
    rtn = [idx]
    if more is not None:
        rtn.extend(more)
    return rtn


def find_closest(idx, nums):
    diffs = list(filter(lambda x: x > 0, map(lambda x: idx - x, nums)))
    if diffs == []:
        return 1e99
    return min(diffs)


def part2(lines):
    ans = 0
    potentials = []
    full_str = ""
    for line in lines:
        # saw even cooler idea where you can regex capture do()'s and don't()'s and flip if the next mul should count
        matches = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", line)
        full_str += line
        potentials.extend(matches)
    # saw really interesting idea in solutions thread to addpend do() to start of str and don't() to end, makes this cleaner
    t = find_all(full_str, "do()", 0)
    dos = [0]
    if t is not None:
        dos.extend(t)
    donts = []
    t = find_all(full_str, "don't()", 0)
    if t is not None:
        donts.extend(t)

    # I made a set out of my matching tuples and noticed they're all unique, so below find idx of mul and closest do/dont works
    for p in potentials:
        idx = full_str.find(f"mul({p[0]},{p[1]}")
        closest_do = find_closest(idx, dos)
        closest_dont = find_closest(idx, donts)
        if closest_do < closest_dont:
            ans += int(p[0]) * int(p[1])

    return ans


print(part1(input))
print("***********part 2***************")
print(part2(input))
