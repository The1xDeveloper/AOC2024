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

arrow = [
    [" ", " ", " ", " ", " "],
    [" ", " ", "^", "A", " "],
    [" ", "<", "v", ">", " "],
    [" ", " ", " ", " ", " "],
]

def manhat(curr, end):
    return abs(curr[0] - end[0]) + abs(curr[1] - end[1])
def np_bfs2(start, target):
    directions = {
        "^": (0, -1),
        "v": (0, 1),
        ">": (1, 0),
        "<": (-1, 0),
    }
    q = deque([])
    #         node, path, dir path
    q.append((start, [], ""))
    i = 0
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

def np_bfs(targets):
    directions = {
        "^": (0, -1),
        "v": (0, 1),
        ">": (1, 0),
        "<": (-1, 0),
    }
    q = deque([])
    #         node, path, dir path
    q.append(((3, 4), [], ""))
    i = 0
    paths_to_target = defaultdict(list)
    min_found = defaultdict(lambda: 1e999)
    while q:
        curr_node, curr_path, curr_dpath = q.popleft()
        if np[curr_node[1]][curr_node[0]] == targets[i]:
            num = np[curr_node[1]][curr_node[0]]
            if len(curr_path) <= min_found[num]:
                paths_to_target[num].append(curr_dpath)
                min_found[num] = len(curr_path)
            else:
                i += 1
                if i >= len(targets):
                    break
                q = deque([(curr_node, [], "")])
                min_found = defaultdict(lambda: 1e999)
                continue


        for dc, (dx, dy) in directions.items():
            nx = curr_node[0] + dx
            ny = curr_node[1] + dy
            if np[ny][nx] != " " and (nx, ny) not in set(curr_path):
                q.append(((nx, ny), curr_path + [(nx, ny)], curr_dpath + dc))
    all_paths = []
    for p1 in paths_to_target[targets[0]]:
        tmp_path = p1 + "A"
        for p2 in paths_to_target[targets[1]]:
            tmp_path2 = tmp_path + p2 + "A"
            for p3 in paths_to_target[targets[2]]:
                tmp_path3 = tmp_path2 + p3 + "A"
                for p4 in paths_to_target[targets[3]]:
                    tmp_path4 = tmp_path3 + p4 + "A"
                    all_paths.append(tmp_path4)
    return all_paths



g_m = defaultdict(lambda: 1e999)
def arrow_bfs(targets, gidx):
    directions = {
        "^": (0, -1),
        "v": (0, 1),
        ">": (1, 0),
        "<": (-1, 0),
    }
    q = deque([])
    #         node, path, dir path, seen, target_num
    q.append(((3, 1), [], "", [], 0))
    min_found = defaultdict(lambda: 1e999)
    a = []
    total_min = 1e999
    while q:
        curr_node, curr_path, curr_dpath, curr_seen, i = q.popleft()
        if len(curr_dpath) >= g_m[gidx]:
            break
        if len(curr_path) > min_found[i]:
            continue
        if arrow[curr_node[1]][curr_node[0]] == targets[i]:
            if len(curr_path) + 1 <= g_m[gidx]:
                min_found[i] = len(curr_path) + 1
            else:
                continue
            if i + 1 < len(targets):
                q.append((curr_node, curr_path, curr_dpath + "A", [curr_node], i + 1))
            else:
                # print(total_min, len(curr_dpath + "A"))
                a.append(curr_dpath + "A")
                g_m[gidx] = len(curr_dpath + "A")
                total_min = len(curr_dpath + "A")


        for dc, (dx, dy) in directions.items():
            nx = curr_node[0] + dx
            ny = curr_node[1] + dy
            if arrow[ny][nx] != " " and (nx, ny) not in set(curr_seen):
                q.append(((nx, ny), curr_path + [(nx, ny)], curr_dpath + dc, curr_seen + [(nx, ny)], i))
    return a


@cache
def dfs2(f, to, time):
    # print("called with: ", f, to, time)
    if time == 1:
        # print("returning: ", f, to, test[f][to] + "A")
        return len(test[f][to] + "A")
    next_str = "A" + test[f][to] + "A"
    # print("next str: ", next_str)
    sub_s = 0
    for a, b in zip(next_str, next_str[1:]):
        sub_s += dfs2(a, b, time -1)
    return sub_s

    for ch in next_str:
        print(f, ch)
        l = dfs2(f, ch, time - 1)
        print(sub_s, l)
        input()
        sub_s += dfs2(f, ch, time - 1)
    return sub_s

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

def arrow_dijk(targets):
    directions = {
        "^": (0, -1),
        "v": (0, 1),
        ">": (1, 0),
        "<": (-1, 0),
    }
    q = []
    #         node, path, dir path, seen, target_num
    #         -target (i), manhat_dist, prev_dir_different, node, path, seen, 
    dist = manhat((3, 1), am[targets[0]])
    heapq.heappush(q, (0, 0, -dist, 0, am["A"], "A"))
    # q.append((am["A"], [], "", [], 0))
    min_found = defaultdict(lambda: 1e999)
    a = []
    total_min = 1e999
    while q:
        ni, steps, mdist, prev_dir_different, curr_node, curr_dpath = heapq.heappop(q)
        # curr_seen.add(curr_node)
        if -ni == len(targets) - 1 and arrow[curr_node[1]][curr_node[0]] == targets[-ni]:
            return (curr_dpath + "A")[1:]
        while arrow[curr_node[1]][curr_node[0]] == targets[-ni]:
            curr_dpath += "A"
            ni -= 1



        for dc, (dx, dy) in directions.items():
            nx = curr_node[0] + dx
            ny = curr_node[1] + dy
            if arrow[ny][nx] != " " and (nx, ny):
                heapq.heappush(q, (ni, steps + 1, manhat((nx, ny), am[targets[-ni]]), curr_dpath[-1] != dc, (nx, ny), curr_dpath + dc))
    return a



def is_in_bounds(point, max_x, max_y):
    return (0 <= point[0] <= max_x) and (0 <= point[1] <= max_y)


def is_int(a):
    b = math.floor(a + 0.5)
    # print(a, b, abs(a - b), sys.float_info.epsilon)
    return abs(a - b) < 0.001

def fi(ch):
    for yi, line in enumerate(np):
        for xi, qqq in enumerate(line):
            if qqq == ch:
                return (xi, yi)
    return -1

@cache
def dfs(f, to, time):
    if time == 0:
        return len(test[f][to]) + 1
    next_str = test[f][to] + "A"
    sub_s = 0
    for a, b in zip(next_str, next_str[1:]):
        sub_s += dfs(a, b, time - 1)
    return sub_s

    # for a, b in zip(next_str, next_str[1:]):
    #     sub_s += next_str + dfs2(a, b, time - 1) + "A"
    # for a, b in zip(next_str, next_str[1:]):
    #     sub_s += dfs2(a, b, time - 1) + "A"
nm = {
    "A": (2, 3),
    "1": (0, 2),
    "2": (1, 2),
    "3": (2, 2),
    "4": (0, 1),
    "5": (1, 1),
    "6": (2, 1),
    "7": (0, 0),
    "8": (1, 0),
    "9": (2, 0),
    "0": (1, 3),
}
am = {
    "A": (3, 1),
    "^": (2, 1),
    "<": (1, 2),
    "v": (2, 2),
    ">": (3, 2),
}
# 491521772034956 too high
# 400643217405238 too high 
# 401371770472788 cant be
# 373082798062118 not right...
# 248919739734728 maybe?
# 191944654229018 too low
def part1b(lines):
    ans = 0
    g_seen = set()
    ans2 = 0
    r = 25

    for yi, line in enumerate(lines):
        print("==========\n",line)
        # num_short = np_bfs([x for x in line.strip()])
        # bethtest1 = np_bfs2(fi("A"), "8")
        # for _ in range(r):
        #     # print(_ + 1)
        #     t = []
        #     for num in bethtest1:
        #         num = "A" + num
        #         tmp = ""
        #         for a, b in zip(num, num[1:]):
        #             tmp += test[a][b] + "A"
        #         t.append(tmp)
        #     # print([len(zz) for zz in t])
        #     # print(t)
        #     t = [x for x in t if len(x) ==  min(len(y) for y in t)]
        #     # print([len(x) for x in t])
        #     bethtest1 = t
        # bethtest1 = len(bethtest1[0])
        # bethtest2 = np_bfs2(fi("A"), "0")
        # for _ in range(r):
        #     # print(_ + 1)
        #     t = []
        #     for num in bethtest2:
        #         num = "A" + num
        #         tmp = ""
        #         for a, b in zip(num, num[1:]):
        #             tmp += test[a][b] + "A"
        #         t.append(tmp)
        #     t = [x for x in t if len(x) ==  min(len(y) for y in t)]
        #     # print([len(x) for x in t])
        #     bethtest2 = t
        # bethtest2 = len(bethtest2[0])
        # bethtest3 = np_bfs2(fi("0"),"2")
        # for _ in range(r):
        #     # print(_ + 1)
        #     t = []
        #     for num in bethtest3:
        #         num = "A" + num
        #         tmp = ""
        #         for a, b in zip(num, num[1:]):
        #             tmp += test[a][b] + "A"
        #         t.append(tmp)
        #     t = [x for x in t if len(x) ==  min(len(y) for y in t)]
        #     # print([len(x) for x in t])
        #     bethtest3 = t
        # bethtest3 = len(bethtest3[0])
        # bethtest4 = np_bfs2(fi("A"), "3")
        # for _ in range(r):
        #     # print(_ + 1)
        #     t = []
        #     for num in bethtest4:
        #         num = "A" + num
        #         tmp = ""
        #         for a, b in zip(num, num[1:]):
        #             tmp += test[a][b] + "A"
        #         t.append(tmp)
        #     t = [x for x in t if len(x) ==  min(len(y) for y in t)]
        #     # print([len(x) for x in t])
        #     bethtest4 = t
        # bethtest4 = len(bethtest4[0])
        # print(bethtest1, bethtest2, bethtest3, bethtest4)
        # input()
        num_shortd1 = np_bfs2(fi("A"), line[0])
        print("zzzzzzzzzzzzzzz")
        # print(num_shortd1)
        first_min = 1e999
        for num in num_shortd1:
            num = "A" + num
            tmp = 0
            for a, b in zip(num, num[1:]):
                tmp += dfs2(a, b, r)
            first_min = min(first_min, tmp)

        print("first min: ", first_min)
        second_min = 1e999
        num_shortd2 = np_bfs2(fi(line[0]), line[1])
        for num in num_shortd2:
            num = "A" + num
            tmp = 0
            for a, b in zip(num, num[1:]):
                tmp += dfs2(a, b, r)
            second_min = min(second_min, tmp)
        third_min = 1e999
        num_shortd3 = np_bfs2(fi(line[1]), line[2])
        for num in num_shortd3:
            num = "A" + num
            tmp = 0
            for a, b in zip(num, num[1:]):
                tmp += dfs2(a, b, r)
            third_min = min(third_min, tmp)
        forth_min = 1e999
        num_shortd4 = np_bfs2(fi(line[2]), "A")
        for num in num_shortd4:
            num = "A" + num
            tmp = 0
            for a, b in zip(num, num[1:]):
                tmp += dfs2(a, b, r)
            forth_min = min(forth_min, tmp)
        # for _ in range(r):
        #     # print(_ + 1)
        #     t = []
        #     t2 = []
        #     for num in num_shortd1:
        #         num = "A" + num
        #         tmp = ""
        #         tmpz = ""
        #         for a, b in zip(num, num[1:]):
        #             tmp += test[a][b] + "A"
        #             g_seen.add((a, b))
        #             # tmpz += dfs2(a, b, 1)
        #         t.append(tmp)
        #         # t2.append(tmpz)
        #     t = [x for x in t if len(x) ==  min(len(y) for y in t)]
        #     # t2 = [x for x in t2 if len(x) ==  min(len(y) for y in t2)]
        #     num_shortd1 = t
        # print(num_shortd1)
        # print("first guy should expand to below")
        # print(len(num_shortd1[0]))
        # num_shortd1 = len(num_shortd1[0])
        # for _ in range(r):
        #     # print(_ + 1)
        #     t = []
        #     for num in num_shortd2:
        #         num = "A" + num
        #         tmp = ""
        #         for a, b in zip(num, num[1:]):
        #             tmp += test[a][b] + "A"
        #             g_seen.add((a, b))
        #         t.append(tmp)
        #     t = [x for x in t if len(x) ==  min(len(y) for y in t)]
        #     # print([len(x) for x in t])
        #     num_shortd2 = t
        # num_shortd2 = len(num_shortd2[0])
        # for _ in range(r):
        #     # print(_ + 1)
        #     t = []
        #     for num in num_shortd3:
        #         num = "A" + num
        #         tmp = ""
        #         for a, b in zip(num, num[1:]):
        #             tmp += test[a][b] + "A"
        #             g_seen.add((a, b))
        #         t.append(tmp)
        #     t = [x for x in t if len(x) ==  min(len(y) for y in t)]
        #     # print([len(x) for x in t])
        #     num_shortd3 = t
        # num_shortd3 = len(num_shortd3[0])
        # for _ in range(r):
        #     # print(_ + 1)
        #     t = []
        #     for num in num_shortd4:
        #         num = "A" + num
        #         tmp = ""
        #         for a, b in zip(num, num[1:]):
        #             tmp += test[a][b] + "A"
        #             g_seen.add((a, b))
        #         t.append(tmp)
        #     t = [x for x in t if len(x) ==  min(len(y) for y in t)]
        #     # print([len(x) for x in t])
        #     num_shortd4 = t
        # num_shortd4 = len(num_shortd4[0])
        # qqqqqqq = (num_shortd1 + num_shortd2 + num_shortd3 + num_shortd4) * int(line[:-1])
        please = (first_min + second_min + third_min + forth_min) * int(line[:-1])
        # ans2 += qqqqqqq
        ans += please
        # print("NEW ANS BELOW:")
        # print(qqqqqqq)
        print("BRAND ANS BELOW:")
        print(please)
        # print(num_shortd1, num_shortd2, num_shortd3, num_shortd4)
        # input()
        # print(line, num_short)
        # for _ in range(2):
        #     print(_ + 1)
        #     t = []
        #     for num in num_short:
        #         num = "A" + num
        #         tmp = ""
        #         for a, b in zip(num, num[1:]):
        #             tmp += test[a][b] + "A"
        #         t.append(tmp)
        #     t = [x for x in t if len(x) ==  min(len(y) for y in t)]
        #     print([len(x) for x in t])
        #     num_short = t
        #     # num_short = tmps
        # print(num_short)
        # t = [len(x) for x in num_short]
        # print(t)
        # m = min(t)
        # t = m * int(line[:-1])
        # print(t)
        # t = [len(x) for x in num_short]
        # m = min(t)
        # t = m * int(line[:-1])
        print("**************** back to real***************")
        # for _ in range(2):
        #     num_short = [arrow_dijk(x) for x in num_short]
        #     num_short = [x for x in num_short if len(x) ==  min(len(y) for y in num_short)]
        # print("LAST ROBOT")
        # print(num_short)
        # up_arror_short = [arrow_dijk(x) for x in num_short]
        # up_arror_short2 = [arrow_dijk(x) for x in up_arror_short]
        # t = [len(x) for x in up_arror_short2]
        # t = [len(x) for x in num_short]
        # print(t)
        # m = min(t)
        # t = m * int(line[:-1])
        # print(t)
        #
        # ans += m * int(line[:-1])

    g_potentials = set()
    for k, v in test.items():
        for k1, v1 in v.items():
            g_potentials.add((k, k1))
    print(g_potentials - g_seen)
    input()
    print(ans)
    # print(ans2)
    return ans

def part1(lines):
    ans = 0

    for yi, line in enumerate(lines):
        print("==========\n",line)
        num_short = np_bfs([x for x in line.strip()])
        # print(num_short)
        t = [len(x) for x in num_short]
        m = min(t)
        print("shortest path: ", m)
        num_short = [x for x in num_short if len(x) == m]
        new_tmp = []
        min_tmp = 1e99
        for z in num_short:
            tmp = len(z)
            for a, b in zip(z, z[1:]):
                if a == b:
                    tmp -= 1
            new_tmp.append((tmp, z))
            min_tmp = min(min_tmp, tmp)
        shortests =[x[1] for x in new_tmp if x[0] == min_tmp] 

        # print(min(len(x) for x in num_short))
        # print(len(num_short))
        # print(num_short)
        # print("shortest num_short: ", m)
        # print("len(num_short): ", len(set(num_short)))
        # up_arror_short = arrow_bfs(num_short, "A" + str(yi))
        up_arror_short = [arrow_bfs(x, "A" + str(yi)) for x in shortests]
        up_arror_short = [x for xs in up_arror_short for x in xs]
        new_tmp = []
        min_tmp = 1e99
        for z in up_arror_short:
            tmp = len(z)
            for a, b in zip(z, z[1:]):
                if a == b:
                    tmp -= 1
            new_tmp.append((tmp, z))
            min_tmp = min(min_tmp, tmp)
        shortests =[x[1] for x in new_tmp if x[0] == min_tmp] 
        # up_arror_short = [arrow_bfs(x, "A" + str(yi)) for x in num_short]
        up_arror_short = [x for xs in up_arror_short for x in xs]

        # print(up_arror_short)
        # print(len(up_arror_short))
        t = [len(x) for x in up_arror_short]
        # print(t)
        m = min(t)
        print("shortest path: ", m)
        # print(m)
        # print("shortest up_arror_short: ", m)
        # up_arror_short = list(set([x for x in up_arror_short if len(x) == m]))[0]
        print("len(up_arror_short): ", len(up_arror_short))
        print("len(shortest)", len(shortests))
        # print(len(up_arror_short))
        # up_arror_short2 = arrow_bfs(up_arror_short, "B" + str(yi))
        up_arror_short2 = [arrow_bfs(x, "B" + str(yi)) for x in shortests]
        up_arror_short2 = [x for xs in up_arror_short2 for x in xs]
        t = [len(x) for x in up_arror_short2]
        m = min(t)
        # # print("shortest up_arror_short2: ", m)
        up_arror_short2 = [x for x in up_arror_short2 if len(x) == m]
        print("len(up_arror_short2): ", len(up_arror_short2))
        print("shortest path: ", m)
        t = m * int(line[:-1])
        print(t)

        ans += m * int(line[:-1])

    return ans


def part2(lines):
    ans = 0

    for yi, line in enumerate(lines):
        print("==========\n",line)
        num_short = np_bfs([x for x in line.strip()])
        t = [len(x) for x in num_short]
        m = min(t)
        num_short = [x for x in num_short if len(x) == m]
        # print(min(len(x) for x in num_short))
        # print(len(num_short))
        # print(num_short)
        print("shortest num_short: ", m)
        print("len(num_short): ", len(set(num_short)))
        up_arror_short = [arrow_bfs(x) for x in num_short]
        up_arror_short = [x for xs in up_arror_short for x in xs]
        # print(up_arror_short)
        # print(len(up_arror_short))
        t = [len(x) for x in up_arror_short]
        # print(t)
        m = min(t)
        # print(m)
        print("shortest up_arror_short: ", m)
        print("len(up_arror_short): ", len(up_arror_short))
        up_arror_short = list(set([x for x in up_arror_short if len(x) == m]))
        print("len(up_arror_short): ", len(up_arror_short))
        # print(len(up_arror_short))
        up_arror_short2 = [arrow_bfs(x) for x in up_arror_short]
        up_arror_short2 = [x for xs in up_arror_short2 for x in xs]
        t = [len(x) for x in up_arror_short2]
        m = min(t)
        print("shortest up_arror_short2: ", m)
        up_arror_short2 = [x for x in up_arror_short2 if len(x) == m]
        print("len(up_arror_short2): ", len(up_arror_short2))
        up_arror_short3 = [arrow_bfs(x) for x in up_arror_short2]
        up_arror_short3 = [x for xs in up_arror_short3 for x in xs]
        t = [len(x) for x in up_arror_short3]
        m = min(t)
        print("shortest up_arror_short3: ", m)
        up_arror_short3 = [x for x in up_arror_short3 if len(x) == m]
        print("len(up_arror_short3): ", len(up_arror_short3))
        t = m * int(line[:-1])
        print(t)

        ans += m * int(line[:-1])

    return ans


print("ans pt1:", part1b(i))
print("***********part 2***************")
# print(part2(i))
