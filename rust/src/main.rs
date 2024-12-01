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
    let ans = "hello";
    println!("Ans pt1: {}", ans);
}
fn part2(lines: Vec<String>) {
    let ans = "hello";
    println!("Ans pt2: {}", ans);
}
fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
