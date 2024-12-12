use rayon::prelude::*;
use std::cmp;
use std::collections::HashMap;
use std::collections::HashSet;
use std::collections::VecDeque;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {
    let lines: Vec<String> = read_lines("../inputs/day10.txt")
        .unwrap()
        .map_while(Result::ok)
        .collect();
    println!("{}", part1(&lines));
    println!("{}", part2(&lines));
}
fn is_in_bounds(xi: i32, yi: i32, max_x: i32, max_y: i32) -> bool {
    (0 <= xi && xi <= max_x) && (0 <= yi && yi <= max_y)
}
fn part1(lines: &[String]) -> i64 {
    let mut ans = 0;
    for (yi, line) in lines.iter().enumerate() {
        for (xi, ch) in line.chars().enumerate() {
            if ch == '0' {
                ans += bfs(xi as i32, yi as i32, lines)
            }
        }
    }
    ans
}

fn part2(lines: &[String]) -> i64 {
    let mut ans = 0;
    for (yi, line) in lines.iter().enumerate() {
        for (xi, ch) in line.chars().enumerate() {
            if ch == '0' {
                ans += bfs2(xi as i32, yi as i32, lines)
            }
        }
    }
    ans
}

fn bfs(xi: i32, yi: i32, lines: &[String]) -> i64 {
    let directions = [(1, 0), (-1, 0), (0, -1), (0, 1)];

    let max_y = (lines.len() - 1) as i32;
    let max_x = (lines[0].len() - 1) as i32;
    let mut seen: HashSet<(i32, i32)> = HashSet::new();
    let mut nines: HashSet<(i32, i32)> = HashSet::new();
    let mut q = VecDeque::new();

    q.push_back((0, xi, yi));
    while !q.is_empty() {
        let (steps, cx, cy) = q.pop_front().unwrap();
        for (dx, dy) in directions {
            let px = dx + cx;
            let py = dy + cy;
            if !seen.contains(&(px, py)) && is_in_bounds(px, py, max_x, max_y) {
                let p = lines
                    .get(py as usize)
                    .unwrap()
                    .chars()
                    .nth(px as usize)
                    .unwrap()
                    .to_digit(10)
                    .unwrap();
                let c = lines
                    .get(cy as usize)
                    .unwrap()
                    .chars()
                    .nth(cx as usize)
                    .unwrap()
                    .to_digit(10)
                    .unwrap();

                let is_p_inc = p == (c + 1);
                if is_p_inc {
                    if p == 9 {
                        nines.insert((px, py));
                    } else {
                        q.push_back((steps + 1, px, py));
                    }
                    seen.insert((px, py));
                }
            }
        }
    }
    nines.len() as i64
}
fn bfs2(xi: i32, yi: i32, lines: &[String]) -> i64 {
    let directions = [(1, 0), (-1, 0), (0, -1), (0, 1)];

    let max_y = (lines.len() - 1) as i32;
    let max_x = (lines[0].len() - 1) as i32;
    let mut q = VecDeque::new();

    q.push_back((0, xi, yi));
    let mut ans = 0;
    while !q.is_empty() {
        let (steps, cx, cy) = q.pop_front().unwrap();
        for (dx, dy) in directions {
            let px = dx + cx;
            let py = dy + cy;
            if is_in_bounds(px, py, max_x, max_y) {
                let p = lines
                    .get(py as usize)
                    .unwrap()
                    .chars()
                    .nth(px as usize)
                    .unwrap()
                    .to_digit(10)
                    .unwrap();
                let c = lines
                    .get(cy as usize)
                    .unwrap()
                    .chars()
                    .nth(cx as usize)
                    .unwrap()
                    .to_digit(10)
                    .unwrap();

                let is_p_inc = p == c + 1;
                if !is_p_inc {
                    continue;
                }
                if p == 9 {
                    ans += 1;
                } else {
                    q.push_back((steps + 1, px, py));
                }
            }
        }
    }
    ans
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
