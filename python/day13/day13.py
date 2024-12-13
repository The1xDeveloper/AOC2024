import re
import sys
import heapq
import math
from collections import deque, defaultdict, Counter
import numpy as np


input = open("../../inputs/day13.txt").read().splitlines()


def is_in_bounds(point, max_x, max_y):
    return (0 <= point[0] <= max_x) and (0 <= point[1] <= max_y)


def is_int(a):
    b = math.floor(a)
    # print(a, b, abs(a - b), sys.float_info.epsilon)
    return abs(a - b) < 0.0001 or ((1 - abs(a - b)) < 0.0001)


def part1(lines):
    start_idx = 0
    ans = 0
    good_math = set()
    good_search = set()
    while start_idx <= len(lines) - 4:
        # print(lines[start_idx])
        btn_a = lines[start_idx]
        matches = re.findall(r"X\+(\d+),\s*Y\+(\d+)", btn_a)
        btn_a = [(int(a), int(b)) for a, b in matches][0]

        btn_b = lines[start_idx + 1]
        matches = re.findall(r"X\+(\d+),\s*Y\+(\d+)", btn_b)
        btn_b = [(int(a), int(b)) for a, b in matches][0]
        target = lines[start_idx + 2]
        matches = re.findall(r"X=(\d+),\s*Y=(\d+)", target)
        target = [(int(a), int(b)) for a, b in matches][0]
        a = np.array([[btn_a[0], btn_b[0]], [btn_a[1], btn_b[1]]])
        b = np.array([target[0], target[1]])
        res = np.linalg.solve(a, b)
        if start_idx == 4:
            print(res)
        if is_int(res[0]) and is_int(res[1]):
            if start_idx == 4:
                print(res)
            # print("good: ", res)
            good_math.add(start_idx)
            ans += res[0] * 3 + res[1]
        else:
            if start_idx == 4:
                print(is_int(res[0]), is_int(res[1]))
                t = math.floor(res[0])
                # print(a, b, abs(a - b), sys.float_info.epsilon)
                print(abs(res[0] - t))

        start_idx += 4
        #    cost, sub_total_x, sub_total_y
        # h = [(0, 0, 0)]
        # seen = set()
        # while h:
        #     cost, sub_total_x, sub_total_y = heapq.heappop(h)
        #     seen.add((sub_total_x, sub_total_y))
        #
        #     if sub_total_x == -target[0] and sub_total_y == -target[1]:
        #         # print(f"on target: {target}, cost: {cost}")
        #         good_search.add(start_idx - 4)
        #         ans += cost
        #         break
        #     if (
        #         sub_total_x - btn_a[0] >= -target[0]
        #         and sub_total_y - btn_a[1] >= -target[1]
        #     ):
        #         to_add = (sub_total_x - btn_a[0], sub_total_y - btn_a[1])
        #         if to_add not in seen:
        #             seen.add(to_add)
        #             heapq.heappush(
        #                 h, (cost + 3, sub_total_x - btn_a[0], sub_total_y - btn_a[1])
        #             )
        #     if (
        #         sub_total_x - btn_b[0] >= -target[0]
        #         and sub_total_y - btn_b[1] >= -target[1]
        #     ):
        #         to_add = (sub_total_x - btn_b[0], sub_total_y - btn_b[1])
        #         if to_add not in seen:
        #             seen.add(to_add)
        #             heapq.heappush(
        #                 h, (cost + 1, sub_total_x - btn_b[0], sub_total_y - btn_b[1])
        #             )

    return ans


# 62044065817615.0 too low
def part2(lines):
    start_idx = 0
    ans = 0
    while start_idx <= len(lines) - 3:
        # print(lines[start_idx])
        btn_a = lines[start_idx]
        matches = re.findall(r"X\+(\d+),\s*Y\+(\d+)", btn_a)
        btn_a = [(int(a), int(b)) for a, b in matches][0]

        btn_b = lines[start_idx + 1]
        matches = re.findall(r"X\+(\d+),\s*Y\+(\d+)", btn_b)
        btn_b = [(int(a), int(b)) for a, b in matches][0]
        target = lines[start_idx + 2]
        matches = re.findall(r"X=(\d+),\s*Y=(\d+)", target)
        target = [
            (int(a) + 10000000000000, int(b) + 10000000000000) for a, b in matches
        ][0]
        a = np.array([[btn_a[0], btn_b[0]], [btn_a[1], btn_b[1]]])
        b = np.array([target[0], target[1]])
        res = np.linalg.solve(a, b)
        if is_int(res[0]) and is_int(res[1]):
            # print("good: ", res)
            ans += res[0] * 3 + res[1]
        start_idx += 4
    return ans


print("ans pt1:", part1(input))
print("***********part 2***************")
print(part2(input))
