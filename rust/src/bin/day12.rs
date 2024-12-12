use std::cmp;
use std::collections::HashMap;
use std::collections::HashSet;
use std::collections::VecDeque;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {
    let lines: Vec<String> = read_lines("../inputs/day12.txt")
        .unwrap()
        .map_while(Result::ok)
        .collect();
    part1(&lines);
    part2(&lines);
}
fn is_in_bounds(xi: i32, yi: i32, max_x: i32, max_y: i32) -> bool {
    (0 <= xi && xi <= max_x) && (0 <= yi && yi <= max_y)
}

fn part1(lines: &[String]) {
    let max_x = lines[0].len() - 1;
    let max_y = lines.len() - 1;
    let mut seen = HashSet::new();
    let mut l = Vec::new();
    let directions = [(1, 0), (-1, 0), (0, 1), (0, -1)];
    for (yi, line) in lines.iter().enumerate() {
        for (xi, ch) in line.chars().enumerate() {
            if seen.contains(&(xi as i32, yi as i32)) {
                continue;
            }
            let target = ch;
            seen.insert((xi as i32, yi as i32));
            let mut q = VecDeque::new();
            q.push_back((xi as i32, yi as i32));
            let mut perim = 0;
            let mut area = 0;
            while !q.is_empty() {
                let (cx, cy) = q.pop_front().unwrap();
                area += 1;
                let mut l_p = 4;

                for (dx, dy) in directions {
                    let px = dx + cx;
                    let py = dy + cy;
                    if is_in_bounds(px, py, max_x as i32, max_y as i32)
                        && lines[py as usize].chars().nth(px as usize).unwrap() == target
                    {
                        l_p -= 1;
                        if !seen.contains(&(px, py)) {
                            seen.insert((px, py));
                            q.push_back((px, py));
                        }
                    }
                }
                perim += l_p;
            }
            l.push(perim * area);
        }
    }
    println!("pt1: {}", l.iter().sum::<i32>());
}
fn part2(lines: &[String]) {
    let max_x = lines[0].len() - 1;
    let max_y = lines.len() - 1;
    let mut seen = HashSet::new();
    let mut l = Vec::new();
    let directions = [(1, 0), (-1, 0), (0, 1), (0, -1)];
    for (yi, line) in lines.iter().enumerate() {
        for (xi, ch) in line.chars().enumerate() {
            if seen.contains(&(xi as i32, yi as i32)) {
                continue;
            }
            let target = ch;
            seen.insert((xi as i32, yi as i32));
            let mut q = VecDeque::new();
            q.push_back((xi as i32, yi as i32));
            let mut area = 0;
            let mut points = HashSet::new();
            while !q.is_empty() {
                let (cx, cy) = q.pop_front().unwrap();
                points.insert((cx, cy));
                area += 1;

                for (dx, dy) in directions {
                    let px = dx + cx;
                    let py = dy + cy;
                    if is_in_bounds(px, py, max_x as i32, max_y as i32)
                        && lines[py as usize].chars().nth(px as usize).unwrap() == target
                    {
                        if !seen.contains(&(px, py)) {
                            seen.insert((px, py));
                            q.push_back((px, py));
                        }
                    }
                }
            }
            let mut corners = 0;
            for (xx, yy) in points.iter() {
                let x = *xx;
                let y = *yy;
                let left_and_up = if !points.contains(&(x - 1, y)) && !points.contains(&(x, y - 1))
                {
                    1
                } else {
                    0
                };
                let left_up_diag = if (points.contains(&(x - 1, y))
                    && points.contains(&(x, y - 1))
                    && !points.contains(&(x - 1, y - 1)))
                {
                    1
                } else {
                    0
                };
                let left_and_down =
                    if !points.contains(&(x - 1, y)) && !points.contains(&(x, y + 1)) {
                        1
                    } else {
                        0
                    };
                let left_down_diag = if (points.contains(&(x - 1, y))
                    && points.contains(&(x, y + 1))
                    && !points.contains(&(x - 1, y + 1)))
                {
                    1
                } else {
                    0
                };
                let right_and_up = if !points.contains(&(x + 1, y)) && !points.contains(&(x, y - 1))
                {
                    1
                } else {
                    0
                };
                let right_up_diag = if (points.contains(&(x + 1, y))
                    && points.contains(&(x, y - 1))
                    && !points.contains(&(x + 1, y - 1)))
                {
                    1
                } else {
                    0
                };
                let right_and_down =
                    if !points.contains(&(x + 1, y)) && !points.contains(&(x, y + 1)) {
                        1
                    } else {
                        0
                    };
                let right_down_diag = if (points.contains(&(x + 1, y))
                    && points.contains(&(x, y + 1))
                    && !points.contains(&(x + 1, y + 1)))
                {
                    1
                } else {
                    0
                };
                corners += (left_and_up
                    + left_up_diag
                    + left_and_down
                    + left_down_diag
                    + right_and_up
                    + right_up_diag
                    + right_and_down
                    + right_down_diag);
            }
            l.push(corners * area);
        }
    }
    println!("pt2: {}", l.iter().sum::<i32>());
}
fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
