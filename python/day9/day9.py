import re
import heapq
from collections import deque, defaultdict, Counter


input = open("../../inputs/day9.txt").read().splitlines()


def is_in_bounds(point, max_x, max_y):
    return (0 <= point[0] <= max_x) and (0 <= point[1] <= max_y)


# 3236920750373 too low too huh
# 6349343813585 too low wow
# 6442070500327 not right either
def part1b(line):
    line = line[0]
    t = []
    c = 0
    for i, ch in enumerate(line):
        can = int(ch)
        if i % 2 == 0:
            for _ in range(can):
                t.append(c)
            c += 1
        else:
            for _ in range(can):
                t.append(".")

    l = 0
    r = len(t) - 1
    while l <= r:
        if t[l] == ".":
            while t[r] == ".":
                r -= 1
            t[l], t[r] = t[r], t[l]
            r -= 1
            l += 1
        else:
            l += 1
            while t[r] == ".":
                r -= 1

    l = 0
    r = len(t) - 1
    while l <= r:
        if t[l] == ".":
            while t[r] == ".":
                r -= 1
            t[l], t[r] = t[r], t[l]
            r -= 1
            l += 1
        else:
            l += 1
            if t[r] == ".":
                r -= 1

    # print(q)
    # print(t[q : q + 10])
    # t[q], t[q + 1] = t[q + 1], t[q]
    ans = 0
    for i, el in enumerate(t):
        if el == ".":
            break
        ans += i * el
    s = "".join([str(x) for x in t])
    return ans


# dots count as 0's
# 15730301980218 too high fk
# 15730301980218
# 15730301980218 aasdafsdfasfsdef
# 6934256157800 too high
# 6442070500327
# 6376648986651 is right, jesus. Okay so dumb me, if original char is 0 and is in even position, that consumes that elements number
def part2(line):
    line = line[0]
    t = []
    c = 0
    s = []
    for i, ch in enumerate(line):
        can = int(ch)
        if i % 2 == 0:
            if can != 0:
                s.append((can, c))
            c += 1
        else:
            s.append((can, "."))
    l = 0
    for i, el in enumerate(s):
        if el[1] == ".":
            l = i
            break
    r = 0
    for i, el in enumerate(s):
        if el[1] != ".":
            r = i
    first_empty = l
    w = 0
    while r > 0:
        # print(s)
        # print(r, s[r])
        if first_empty >= len(s):
            break
        # print(first_empty, s[first_empty])
        if s[r][1] == ".":
            r -= 1
            continue
        for l in range(first_empty, r):
            # print("s[l] and s[r]")
            # print(s[l])
            # print(s[r])
            # print("===")
            if s[l][1] == "." and s[l][0] >= s[r][0]:
                if s[l][0] > s[r][0]:
                    tmp = (s[l][0] - s[r][0], ".")
                    # print(s)
                    s.insert(l + 1, tmp)
                    # print(s)
                    # print(s[l + 1])
                    # print(s[r + 1])
                    s[l], s[r + 1] = s[r + 1], (s[r + 1][0], ".")
                    # s[r + 1] = (s[l][0], ".")
                    # print(s)
                    if l == first_empty:
                        while s[first_empty][1] != ".":
                            first_empty += 1
                    break
                else:
                    s[l], s[r] = s[r], s[l]
                    if l == first_empty:
                        while s[first_empty][1] != ".":
                            first_empty += 1
                    break
        r -= 1
    # print(s)

    c = 0
    ans = 0
    for i, el in enumerate(s):
        for _ in range(el[0]):
            if el[1] != ".":
                ans += c * el[1]
            c += 1

    return ans


print(part1b(input))
print("***********part 2***************")
print(part2(input))
