import re
import heapq
from time import time
from collections import deque, defaultdict, Counter


input = open("../../inputs/day7.txt").readlines()


def part1(lines):
    ans = 0
    for line in lines:
        target, nums = line.split(":")
        target = int(target)
        nums = [int(x) for x in nums.split()]
        idx = 1
        s = nums[0]
        q = deque([(s, idx)])
        while q:
            sub_s, c_idx = q.popleft()
            if c_idx >= len(nums):
                continue
            r = nums[c_idx]
            add = sub_s + r
            mul = sub_s * r
            if (c_idx == len(nums) - 1) and target in [add, mul]:
                ans += target
                break
            if add <= target:
                q.append((add, c_idx + 1))
            if mul <= target:
                q.append((mul, c_idx + 1))

    return ans


# 249943303573988 too high
# 249908125305812 too low
# 249943041417600 correct but I changed nothing....
def part2(lines):
    ans = 0
    for line in lines:
        target, nums = line.split(":")
        target = int(target)
        nums = [int(x) for x in nums.split()]
        idx = 1
        s = nums[0]
        q = deque([(s, idx)])
        while q:
            sub_s, c_idx = q.popleft()
            if c_idx >= len(nums):
                break
            r = nums[c_idx]
            add = sub_s + r
            mul = sub_s * r
            comb = int(str(sub_s) + str(r))
            if (c_idx == len(nums) - 1) and target in [add, mul, comb]:
                ans += target
                break
            if add <= target:
                q.append((add, c_idx + 1))
            if mul <= target:
                q.append((mul, c_idx + 1))
            if comb <= target:
                q.append((comb, c_idx + 1))
    return ans


s = time()
print(part1(input))
print(f"took: {time() - s}")
print("********************")
s = time()
print(part2(input))
print(f"took: {time() - s}")
