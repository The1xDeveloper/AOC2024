use std::cmp;
use std::collections::HashMap;
use std::collections::HashSet;
use std::collections::VecDeque;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {
    let lines: Vec<String> = read_lines("../inputs/day6.txt")
        .unwrap()
        .map_while(Result::ok)
        .collect();
    part2(&lines);
}
fn is_in_bounds(xi: i32, yi: i32, max_x: i32, max_y: i32) -> bool {
    (0 <= xi && xi <= max_x) && (0 <= yi && yi <= max_y)
}
fn bfspt2(xi: i32, yi: i32, lines: &[String]) -> HashSet<(i32, i32)> {
    let mut dy = -1i32;
    let mut dx = 0i32;
    let max_y = (lines.len() - 1) as i32;
    let max_x = (lines[0].len() - 1) as i32;
    let mut seen: HashSet<(i32, i32)> = HashSet::new();
    let mut q = VecDeque::new();

    q.push_back((xi, yi));
    while !q.is_empty() {
        let (cx, cy) = q.pop_front().unwrap();
        let mut px = cx + dx;
        let mut py = cy + dy;
        seen.insert((cx, cy));
        if !((0i32 <= px && px <= max_x) && (0i32 <= py && py <= max_y)) {
            return seen;
        }
        while lines
            .get(py as usize)
            .unwrap()
            .chars()
            .nth(px as usize)
            .unwrap()
            == '#'
        {
            dy = -1 * dy;
            (dy, dx) = (dx, dy);
            px = cx + dx;
            py = cy + dy;
            if !((0i32 <= px && px <= max_x) && (0i32 <= py && py <= max_y)) {
                return seen;
            }
        }
        q.push_back((px, py));
    }
    seen
}
fn bfs_find_cycle(origin: (i32, i32), lines: &Vec<Vec<char>>) -> i32 {
    let mut dy = -1i32;
    let mut dx = 0i32;
    let max_y = (lines.len() - 1) as i32;
    let max_x = (lines[0].len() - 1) as i32;
    let mut seen: HashSet<(i32, i32, i32, i32)> = HashSet::new();
    let (xi, yi) = origin;
    let mut q = VecDeque::new();
    q.push_back((xi, yi));
    while !q.is_empty() {
        let (cx, cy) = q.pop_front().unwrap();
        if seen.contains(&(cx, cy, dx, dy)) {
            return 1;
        }
        seen.insert((cx, cy, dx, dy));
        let mut px = cx + dx;
        let mut py = cy + dy;
        if !((0 <= px && px <= max_x) && (0 <= py && py <= max_y)) {
            return 0;
        }

        while *lines.get(py as usize).unwrap().get(px as usize).unwrap() == '#' {
            dy = -1 * dy;
            (dy, dx) = (dx, dy);
            px = cx + dx;
            py = cy + dy;
            if !((0i32 <= px && px <= max_x) && (0i32 <= py && py <= max_y)) {
                return 0;
            }
        }
        q.push_back((px, py));
    }
    0
}
// def bfs_find_cycle(origin, lines):
// q = deque([(0, xi, yi)])
// while q:
// steps, curr_x, curr_y = q.popleft()
// if (curr_x, curr_y, dx, dy) in seen:
// return 1
// seen.add((curr_x, curr_y, dx, dy))
// px = curr_x + dx
// py = curr_y + dy
// if not ((0 <= px <= max_x) and (0 <= py <= max_y)):
// return 0
// while lines[py][px] == "#":
// dy = -1 * dy
// dy, dx = dx, dy
// px = curr_x + dx
// py = curr_y + dy
//
// if not ((0 <= px <= max_x) and (0 <= py <= max_y)):
// return 0
// q.append((steps + 1, px, py))
// return 0

fn part2(lines: &[String]) {
    let mut graph2: Vec<Vec<char>> = Vec::new();
    let mut potentials: HashSet<(i32, i32)> = HashSet::new();
    let mut origin: (i32, i32) = (1, 1);
    let mut ans: i32 = 0;

    lines.iter().for_each(|line| {
        let cs: Vec<char> = line.chars().collect();
        graph2.push(cs);
    });
    lines.iter().enumerate().for_each(|(yi, line)| {
        line.chars().enumerate().for_each(|(xi, c)| {
            if c == '^' {
                origin = (xi as i32, yi as i32);
                potentials = bfspt2(xi as i32, yi as i32, lines)
            }
        })
    });
    potentials.iter().for_each(|(ox, oy)| {
        if (*ox, *oy) != origin {
            {
                let mut t = graph2
                    .get_mut(*oy as usize)
                    .unwrap()
                    .get_mut(*ox as usize)
                    .unwrap();
                *t = '#';
            }
            ans += bfs_find_cycle(origin, &graph2);

            {
                let mut t = graph2
                    .get_mut(*oy as usize)
                    .unwrap()
                    .get_mut(*ox as usize)
                    .unwrap();
                *t = '.';
            }
        }
    });
    println!("pt2: {}", ans);
}
fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
