use std::cmp;
use std::collections::HashMap;
use std::collections::HashSet;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {
    let lines: Vec<String> = read_lines("../inputs/day1.txt")
        .unwrap()
        .map_while(Result::ok)
        .collect();
    part1(lines.clone());
    part2(lines.clone());
    println!("Hello, world!");
}
fn part1(lines: Vec<String>) {
    let mut A = Vec::new();
    let mut B = Vec::new();
    for line in lines {
        let mut split = line.split_whitespace();
        A.push(split.next().unwrap().parse::<i32>().unwrap());
        B.push(split.next().unwrap().parse::<i32>().unwrap());
    }
    A.sort();
    B.sort();
    let ans: i32 = A
        .into_iter()
        .zip(B.into_iter())
        .map(|(a, b)| (a - b).abs())
        .sum();

    println!("Ans pt1: {}", ans);
}
fn part2(lines: Vec<String>) {
    let mut A = Vec::new();
    let mut B: HashMap<i32, i32> = HashMap::new();
    for line in lines {
        let mut split = line.split_whitespace();
        A.push(split.next().unwrap().parse::<i32>().unwrap());
        let b = split.next().unwrap().parse::<i32>().unwrap();
        if B.contains_key(&b) {
            B.insert(b, B.get(&b).unwrap() + 1);
        } else {
            B.insert(b, 1);
        }
    }
    let ans: i32 = A
        .into_iter()
        .map(|a| match B.get(&a) {
            Some(b) => b * a,
            None => 0,
        })
        .sum();
    println!("Ans pt2: {}", ans);
}
fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
