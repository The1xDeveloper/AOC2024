import re
import heapq
from collections import deque, defaultdict, Counter


input = open("../../inputs/day5.txt").readlines()


def part1(lines):
    ans = 0
    in_degrees = defaultdict(set)
    games = []
    for line in lines:
        if "|" in line:
            a, b = line.split("|")
            in_degrees[int(b)].add(int(a))
        elif "," in line:
            games.append([int(x) for x in line.split(",")])
        else:
            pass
    for game in games:
        game_set = set(game)
        for num in game:
            game_set.remove(num)
            t = in_degrees.get(num, set())
            if game_set.intersection(t):
                break
        else:
            ans += game[len(game) // 2]

    return ans


def part2(lines):
    ans = 0
    in_degrees = defaultdict(set)
    graph = defaultdict(list)
    games = []
    for line in lines:
        if "|" in line:
            a, b = line.split("|")
            in_degrees[int(b)].add(int(a))
            graph[a].append(b)
            graph[b].append(a)
        elif "," in line:
            games.append([int(x) for x in line.split(",")])
        else:
            pass
    for game in games:
        game_set = set(game)
        must_fix = False
        for num in game:
            game_set.remove(num)
            t = in_degrees.get(num, set())
            if game_set.intersection(t):
                must_fix = True
                break
        if must_fix:
            game_set = set(game)
            l = {a: game_set.intersection(in_degrees.get(a, set())) for a in game_set}
            # should always be just one zero or else isnt unique, but maybe middle elm is always unique? idk
            zeros = deque([a for a, b in l.items() if b == set()])
            new_game = []
            while zeros:
                c = zeros.popleft()

                new_game.append(c)
                new_zeros = deque([])
                for nei in graph[c]:
                    if nei in game_set and c in l[nei]:
                        l[nei].remove(c)
                        if l[nei] == set():
                            new_zeros.append(nei)
                zeros = new_zeros
            ans += new_game[len(new_game) // 2]

    return ans


print(part1(input))
print("***********part 2***************")
print(part2(input))
