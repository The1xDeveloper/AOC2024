import re
import sys
import heapq
import math
import time
from collections import deque, defaultdict, Counter
from functools import cache

i = open("../../inputs/day21.txt").read().splitlines()

np = [
    [" ", " ", " ", " ", " "],
    [" ", "7", "8", "9", " "],
    [" ", "4", "5", "6", " "],
    [" ", "1", "2", "3", " "],
    [" ", " ", "0", "A", " "],
    [" ", " ", " ", " ", " "],
]


def np_bfs(start, target):
    directions = {
        "^": (0, -1),
        "v": (0, 1),
        ">": (1, 0),
        "<": (-1, 0),
    }
    q = deque([])
    #         node, path, dir path
    q.append((start, [], ""))
    paths_to_target = defaultdict(list)
    min_found = defaultdict(lambda: 1e999)
    while q:
        curr_node, curr_path, curr_dpath = q.popleft()
        if np[curr_node[1]][curr_node[0]] == target:
            num = np[curr_node[1]][curr_node[0]]
            if len(curr_path) <= min_found[num]:
                paths_to_target[num].append(curr_dpath)
                min_found[num] = len(curr_path)
            else:
                break


        for dc, (dx, dy) in directions.items():
            nx = curr_node[0] + dx
            ny = curr_node[1] + dy
            if np[ny][nx] != " " and (nx, ny) not in set(curr_path):
                q.append(((nx, ny), curr_path + [(nx, ny)], curr_dpath + dc))
    all_paths = []
    for p1 in paths_to_target[target]:
        tmp_path = p1 + "A"
        all_paths.append(tmp_path)
    return all_paths


test = {
    "A": {
        "A": "",
        "^": "<",
        ">": "v",
        "v": "<v",
        "<": "v<<",
    },
    "^": {
        "^": "",
        "A": ">",
        ">": "v>", # unknown >v or v>
        "v": "v",
        "<": "v<",
    },
    "v": {
        "v": "",
        "A": "^>", #unkonwn ^> or >^
        ">": ">",
        "^": "^",
        "<": "<",
    },
    ">": {
        ">": "",
        "A": "^",
        "^": "<^", #unkonwn ^< or <^ tried both
        "v": "<",
        "<": "<<",
    },
    "<": {
        "<": "",
        "A": ">>^",
        ">": ">>",
        "v": ">",
        "^": ">^",
    },
}


def fi(to_find):
    for yi, line in enumerate(np):
        for xi, ch in enumerate(line):
            if ch == to_find:
                return (xi, yi)
    return -1

@cache
def dfs(f, to, time):
    if time == 1:
        return len(test[f][to]) + 1
    next_str = "A" + test[f][to] + "A"
    sub_s = 0
    for a, b in zip(next_str, next_str[1:]):
        sub_s += dfs(a, b, time - 1)
    return sub_s


def part(lines, r=2):
    ans = 0

    for line in lines:
        line = line.strip()
        with_a = "A" + line
        s = 0
        for a, b in zip(with_a, with_a[1:]):
            num_short = np_bfs(fi(a), b)
            min_found = 1e999
            for num in num_short:
                num = "A" + num
                tmp = 0
                for a, b in zip(num, num[1:]):
                    tmp += dfs(a, b, r)
                min_found = min(min_found, tmp)
            s += min_found

        ans += s * int(line[:-1])

    return ans


print("ans pt1:", part(i, r=2))
print("***********part 2***************")
print(part(i, r=25))
