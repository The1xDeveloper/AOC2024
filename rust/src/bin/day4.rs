use std::cmp;
use std::collections::HashMap;
use std::collections::HashSet;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {
    let lines: Vec<String> = read_lines("../inputs/day4.txt")
        .unwrap()
        .map_while(Result::ok)
        .collect();
    part1(&lines);
    part2(&lines);
}
fn is_in_bounds(xi: i32, yi: i32, max_x: i32, max_y: i32) -> bool {
    (0 <= xi && xi <= max_x) && (0 <= yi && yi <= max_y)
}
fn find(xi: i32, yi: i32, lines: &[String]) -> i32 {
    let directions = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1),
        (1, 1),
        (1, -1),
        (-1, 1),
        (-1, -1),
    ];
    let max_y = lines.len() as i32 - 1;
    let max_x = lines[0].len() as i32 - 1;
    directions
        .iter()
        .filter_map(|&(dx, dy)| {
            let mut cx = xi;
            let mut cy = yi;
            let mut sub_str = String::from("X");
            for _ in 0..3 {
                cx += dx;
                cy += dy;
                if !((0 <= cx && cx <= max_x) && (0 <= cy && cy <= max_y)) {
                    return None;
                }
                sub_str.push(lines[cy as usize].chars().nth(cx as usize).unwrap());
            }
            if sub_str == "XMAS" {
                Some(1)
            } else {
                None
            }
        })
        .sum()
}
fn find2(xi: i32, yi: i32, lines: &[String]) -> i32 {
    let max_y = lines.len() as i32 - 1;
    let max_x = lines[0].len() as i32 - 1;
    if !(is_in_bounds(xi + 1, yi + 1, max_x, max_y) && is_in_bounds(xi - 1, yi - 1, max_x, max_y)) {
        return 0;
    }

    let mut diagonals = Vec::with_capacity(2);

    diagonals.push((
        lines[(yi - 1) as usize]
            .chars()
            .nth((xi - 1) as usize)
            .unwrap(),
        lines[(yi + 1) as usize]
            .chars()
            .nth((xi + 1) as usize)
            .unwrap(),
    ));
    diagonals.push((
        lines[(yi + 1) as usize]
            .chars()
            .nth((xi - 1) as usize)
            .unwrap(),
        lines[(yi - 1) as usize]
            .chars()
            .nth((xi + 1) as usize)
            .unwrap(),
    ));

    if diagonals.iter().all(|&(a, b)| {
        let s: String = vec![a, b].into_iter().collect();
        let reversed: String = s.chars().rev().collect();
        s == "MS" || reversed == "MS"
    }) {
        1
    } else {
        0
    }
}

fn part1(lines: &[String]) {
    let ans: i32 = lines
        .iter()
        .enumerate()
        .map(|(yi, line)| {
            line.chars()
                .enumerate()
                .map(|(xi, ch)| {
                    if ch == 'X' {
                        find(xi as i32, yi as i32, lines)
                    } else {
                        0
                    }
                })
                .sum::<i32>()
        })
        .sum();
    println!("pt1: {}", ans);
}
fn part2(lines: &[String]) {
    let ans: i32 = lines
        .iter()
        .enumerate()
        .map(|(yi, line)| {
            line.chars()
                .enumerate()
                .map(|(xi, ch)| {
                    if ch == 'A' {
                        find2(xi as i32, yi as i32, lines)
                    } else {
                        0_i32
                    }
                })
                .sum::<i32>()
        })
        .sum();
    println!("pt2: {}", ans);
}
fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
