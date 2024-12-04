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
    part1(lines.clone());
    part2(lines.clone());
}
fn find(xi: i32, yi: i32, lines: Vec<String>) -> i32 {
    let mut c = 0;
    let directions = [
        (1i32, 0i32),
        (-1, 0),
        (0, 1),
        (0, -1),
        (1, 1),
        (1, -1),
        (-1, 1),
        (-1, -1),
    ];
    let max_y: i32 = lines.len() as i32 - 1;
    let max_x: i32 = lines[0].len() as i32 - 1;
    for (dx, dy) in directions {
        let mut sub_str = "X".to_string();
        let mut cx = xi;
        let mut cy = yi;
        for _ in 0..3 {
            cx += dx;
            cy += dy;
            if !((0i32 <= cx && cx <= max_x) && (0i32 <= cy && cy <= max_y)) {
                sub_str = "X".to_string();
                break;
            }
            sub_str.push(lines[cy as usize].chars().nth(cx as usize).unwrap());
        }
        if sub_str == "XMAS" {
            c += 1
        }
    }
    c
}
fn find2(xi: i32, yi: i32, lines: Vec<String>) -> i32 {
    let max_y: i32 = lines.len() as i32 - 1;
    let max_x: i32 = lines[0].len() as i32 - 1;

    if !(((0 <= (xi + 1)) && ((xi + 1) <= max_x)) && ((0 <= (xi - 1)) && ((xi - 1) <= max_x))) {
        return 0;
    }
    if !(((0 <= (yi + 1)) && ((yi + 1) <= max_y)) && ((0 <= (yi - 1)) && ((yi - 1) <= max_y))) {
        return 0;
    }

    let mut right_to_left = lines[(yi - 1) as usize]
        .chars()
        .nth((xi - 1) as usize)
        .unwrap()
        .to_string();
    right_to_left.push(
        lines[(yi + 1) as usize]
            .chars()
            .nth((xi + 1) as usize)
            .unwrap(),
    );
    let mut left_to_right = lines[(yi + 1) as usize]
        .chars()
        .nth((xi - 1) as usize)
        .unwrap()
        .to_string();
    left_to_right.push(
        lines[(yi - 1) as usize]
            .chars()
            .nth((xi + 1) as usize)
            .unwrap(),
    );
    if (right_to_left.eq("MS") || right_to_left.chars().rev().collect::<String>().eq("MS"))
        && (left_to_right.eq("MS") || left_to_right.chars().rev().collect::<String>().eq("MS"))
    {
        return 1;
    }
    0
}

fn part1(lines: Vec<String>) {
    let ans: i32 = lines
        .clone()
        .into_iter()
        .enumerate()
        .map(|(yi, line)| {
            line.chars()
                .enumerate()
                .map(|(xi, ch)| {
                    if ch == 'X' {
                        find(xi as i32, yi as i32, lines.clone())
                    } else {
                        0_i32
                    }
                })
                .sum::<i32>()
        })
        .sum();
    println!("pt1: {}", ans);
}
fn part2(lines: Vec<String>) {
    let ans: i32 = lines
        .clone()
        .into_iter()
        .enumerate()
        .map(|(yi, line)| {
            line.chars()
                .enumerate()
                .map(|(xi, ch)| {
                    if ch == 'A' {
                        find2(xi as i32, yi as i32, lines.clone())
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
