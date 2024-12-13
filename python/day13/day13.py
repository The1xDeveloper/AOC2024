import re
import sys
import heapq
import math
from collections import deque, defaultdict, Counter


input = open("../../inputs/day13.txt").read().splitlines()


def is_in_bounds(point, max_x, max_y):
    return (0 <= point[0] <= max_x) and (0 <= point[1] <= max_y)


def is_int(a):
    b = math.floor(a + 0.5)
    # print(a, b, abs(a - b), sys.float_info.epsilon)
    return abs(a - b) < 0.001


"""
    x1 * X + x2 * Y = A
y1 * X + y2 * Y = B

x1 * X = A - (x2 * Y)
X = (A - (x2 * Y))/x1
X = A/x1 - (x2/x1) * Y


y1 * (A/x1 - (x2/x1) * Y) + y2 * Y = B
(y1 * A)/x1 - ((y1 * x2)/x1) * Y + y2 * Y = B

-((y1 * x2)/x1) * Y + y2 * Y = B - (y1 * A)/x1

Y * (-((y1 * x2)/x1)  + y2) = B - (y1 * A)/x1
Y = (B - (y1 * A)/x1)/ ((-((y1 * x2)/x1)  + y2))


x1 * X = A - (x2 * Y)

X = (A - (x2 * Y))/x1
"""


def part1(lines):
    start_idx = 0
    ans = 0
    while start_idx <= len(lines) - 4:
        # print(lines[start_idx])
        btn_a = lines[start_idx]
        matches = re.findall(r"X\+(\d+),\s*Y\+(\d+)", btn_a)
        btn_a = [(int(a), int(b)) for a, b in matches][0]
        x1 = btn_a[0]
        y1 = btn_a[1]

        btn_b = lines[start_idx + 1]
        matches = re.findall(r"X\+(\d+),\s*Y\+(\d+)", btn_b)
        btn_b = [(int(a), int(b)) for a, b in matches][0]
        x2 = btn_b[0]
        y2 = btn_b[1]
        target = lines[start_idx + 2]
        matches = re.findall(r"X=(\d+),\s*Y=(\d+)", target)
        target = [(int(a), int(b)) for a, b in matches][0]
        A = target[0]
        B = target[1]

        Y = (B - (y1 * A) / x1) / (-((y1 * x2) / x1) + y2)
        X = (A - (x2 * Y)) / x1
        if is_int(Y) and is_int(X):
            ans += int(X) * 3 + int(Y)

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
        x1 = btn_a[0]
        y1 = btn_a[1]

        btn_b = lines[start_idx + 1]
        matches = re.findall(r"X\+(\d+),\s*Y\+(\d+)", btn_b)
        btn_b = [(int(a), int(b)) for a, b in matches][0]
        x2 = btn_b[0]
        y2 = btn_b[1]
        target = lines[start_idx + 2]
        matches = re.findall(r"X=(\d+),\s*Y=(\d+)", target)
        target = [
            (int(a) + 10000000000000, int(b) + 10000000000000) for a, b in matches
        ][0]
        A = target[0]
        B = target[1]

        Y = (B - (y1 * A) / x1) / (-((y1 * x2) / x1) + y2)
        if is_int(Y):
            X = (A - (x2 * Y)) / x1
            if is_int(X):
                ans += X * 3 + Y
        start_idx += 4
    return ans


print("ans pt1:", part1(input))
print("***********part 2***************")
print(part2(input))
