import re
import heapq
from collections import deque, defaultdict, Counter


input = open("../../inputs/day11.txt").read().splitlines()


def is_in_bounds(point, max_x, max_y):
    return (0 <= point[0] <= max_x) and (0 <= point[1] <= max_y)


def part1(lines):
    stones = [int(x) for x in lines[0].split()]
    for _ in range(25):
        new_stones = []
        for stone in stones:
            if stone == 0:
                new_stones.append(1)
            elif len(str(stone)) % 2 == 0:
                str_stone = str(stone)
                a = str_stone[: len(str_stone) // 2]
                b = str_stone[len(str_stone) // 2 :]
                new_stones.append(int(a))
                new_stones.append(int(b))
            else:
                new_stones.append(stone * 2024)
        stones = new_stones

    return len(stones)


def part2(lines):
    stones = [int(x) for x in lines[0].split()]
    m = defaultdict(int)
    for stone in stones:
        m[stone] += 1
    for _ in range(75):
        new_m = defaultdict(int)
        for stone, num in m.items():
            if stone == 0:
                new_m[1] += num
            elif len(str(stone)) % 2 == 0:
                str_stone = str(stone)
                a = str_stone[: len(str_stone) // 2]
                b = str_stone[len(str_stone) // 2 :]
                new_m[int(a)] += num
                new_m[int(b)] += num
            else:
                new_m[stone * 2024] += num
        m = new_m

    return sum(m.values())


print("ans pt1:", part1(input))
print("***********part 2***************")
print(part2(input))