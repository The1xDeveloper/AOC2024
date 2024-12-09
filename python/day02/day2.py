import re
import heapq
from collections import deque, defaultdict, Counter


input = open("../../inputs/day2.txt").readlines()


def is_between_bounds(nums):
    return all(1 <= abs(a - b) <= 3 for a, b in zip(nums, nums[1:]))


def mono(nums):
    return all(a <= b for a, b in zip(nums, nums[1:])) or all(
        a >= b for a, b in zip(nums, nums[1:])
    )


# 371 too low...
def part1(lines):
    ans = 0
    for line in lines:
        nums = [int(x) for x in line.split()]
        if not mono(nums):
            continue
        if not is_between_bounds(nums):
            continue
        ans += 1

    return ans


def test_nums(nums, mulligan):
    if not mono(nums) and not mulligan:
        return False
    if not mono(nums):
        for i in range(len(nums)):
            if test_nums(nums[:i] + nums[i + 1 :], False):
                return True
        else:
            return False
    if not is_between_bounds(nums) and not mulligan:
        return False
    if not is_between_bounds(nums):
        for i in range(len(nums)):
            if test_nums(nums[:i] + nums[i + 1 :], False):
                return True
        else:
            return False
    return True


def part2(lines):
    ans = 0
    for line in lines:
        nums = [int(x) for x in line.split()]
        if test_nums(nums, True):
            ans += 1

    return ans


print(part1(input))
print("***********part 2***************")
print(part2(input))
