use std::cmp;
use std::collections::HashMap;
use std::collections::HashSet;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {
    let lines: Vec<String> = read_lines("../inputs/day11.txt")
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
    println!("hasfd");
    let mut stones: Vec<i64> = lines
        .first()
        .unwrap()
        .split_whitespace()
        .map(|s| s.parse::<i64>().unwrap())
        .collect();
    for _ in 0..25 {
        let mut new_stones = Vec::new();
        for stone in stones.iter() {
            if *stone == 0 {
                new_stones.push(1);
            } else if stone.to_string().len() % 2 == 0 {
                let str_stone = stone.to_string();
                let (a, b) = str_stone.split_at(str_stone.len() / 2);
                new_stones.push(a.parse().unwrap());
                new_stones.push(b.parse().unwrap());
            } else {
                new_stones.push(*stone * 2024);
            }
        }
        stones = new_stones;
    }
    println!("pt1: {}", stones.len());
}
fn part2(lines: &[String]) {
    let mut stones: Vec<i64> = lines
        .first()
        .unwrap()
        .split_whitespace()
        .map(|s| s.parse::<i64>().unwrap())
        .collect();
    let mut m: HashMap<i64, i64> = HashMap::new();
    for stone in stones {
        *m.entry(stone).or_insert(0) += 1;
    }
    let z = (0..75).fold(m, |acc, i| {
        let mut new_stones: HashMap<i64, i64> = HashMap::new();
        for (stone, num) in acc.iter() {
            if *stone == 0 {
                *new_stones.entry(1).or_insert(0) += num;
            } else if stone.to_string().len() % 2 == 0 {
                let str_stone = stone.to_string();
                let (a, b) = str_stone.split_at(str_stone.len() / 2);
                let x = a.parse().unwrap();
                let y = b.parse().unwrap();
                *new_stones.entry(x).or_insert(0) += num;
                *new_stones.entry(y).or_insert(0) += num;
            } else {
                let y = *stone * 2024;
                *new_stones.entry(y).or_insert(0) += num;
            }
        }
        new_stones
    });
    println!("pt2: {}", z.values().sum::<i64>());
}
fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
