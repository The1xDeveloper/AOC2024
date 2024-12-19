use rayon::prelude::*;
use std::cmp;
use std::collections::HashMap;
use std::collections::HashSet;
use std::collections::VecDeque;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::sync::Mutex;
use std::time::Instant;
use std::usize;

fn main() {
    let lines: Vec<String> = read_lines("../inputs/day19.txt")
        .unwrap()
        .map_while(Result::ok)
        .collect();
    let start = Instant::now();
    part1(&lines);
    let duration = start.elapsed();
    println!(
        "Time taken no i/o: {} seconds and {} nanos and {} millis and {} micros",
        duration.as_secs(),
        duration.as_nanos(),
        duration.as_millis(),
        duration.as_micros()
    );
    let start = Instant::now();
    let duration = start.elapsed();
    println!(
        "Time taken no i/o: {} seconds and {} nanos and {} millis and {} micros",
        duration.as_secs(),
        duration.as_nanos(),
        duration.as_millis(),
        duration.as_micros()
    );
    let start = Instant::now();
    part2(&lines);
    let duration = start.elapsed();
    println!(
        "Time taken no i/o: {} seconds and {} nanos and {} millis and {} micros",
        duration.as_secs(),
        duration.as_nanos(),
        duration.as_millis(),
        duration.as_micros()
    );
    let start = Instant::now();
    let duration = start.elapsed();
    println!(
        "Time taken no i/o: {} seconds and {} nanos and {} millis and {} micros",
        duration.as_secs(),
        duration.as_nanos(),
        duration.as_millis(),
        duration.as_micros()
    )
}
fn is_in_bounds(xi: i32, yi: i32, max_x: i32, max_y: i32) -> bool {
    (0 <= xi && xi <= max_x) && (0 <= yi && yi <= max_y)
}
fn backtrack(word: &str, towels: &[String], cache: &Mutex<HashMap<String, i32>>) -> i32 {
    if word.is_empty() {
        return 1;
    }
    if let Some(&result) = cache.lock().unwrap().get(word) {
        return result;
    }
    for t in towels {
        if word.starts_with(t) {
            if backtrack(word.strip_prefix(t).unwrap(), towels, cache) == 1 {
                cache.lock().unwrap().insert(word.to_string(), 1);
                return 1;
            }
        }
    }
    cache.lock().unwrap().insert(word.to_string(), 0);
    0
}
fn backtrack_lame(word: &str, towels: &[String], cache: &mut HashMap<String, i32>) -> i32 {
    if word.is_empty() {
        return 1;
    }
    if let Some(&result) = cache.get(word) {
        return result;
    }
    for t in towels {
        if word.starts_with(t) {
            if backtrack_lame(word.strip_prefix(t).unwrap(), towels, cache) == 1 {
                cache.insert(word.to_string(), 1);
                return 1;
            }
        }
    }
    cache.insert(word.to_string(), 0);
    0
}
fn backtrack2_lame(word: &str, towels: &[String], cache: &mut HashMap<String, i64>) -> i64 {
    if word.is_empty() {
        return 1;
    }
    if let Some(&result) = cache.get(word) {
        return result;
    }
    let mut s = 0;
    for t in towels {
        if word.starts_with(t) {
            s += backtrack2_lame(word.strip_prefix(t).unwrap(), towels, cache);
        }
    }
    cache.insert(word.to_string(), s);
    s
}
fn backtrack2(word: &str, towels: &[String], cache: &Mutex<HashMap<String, i64>>) -> i64 {
    if word.is_empty() {
        return 1;
    }
    if let Some(&result) = cache.lock().unwrap().get(word) {
        return result;
    }
    let mut s = 0;
    for t in towels {
        if word.starts_with(t) {
            s += backtrack2(word.strip_prefix(t).unwrap(), towels, cache);
        }
    }
    cache.lock().unwrap().insert(word.to_string(), s);
    s
}
fn part1(lines: &[String]) {
    let towels: Vec<String> = lines
        .get(0)
        .unwrap()
        .split(",")
        .map(str::trim)
        .map(String::from)
        .collect();
    // let cache = Mutex::new(HashMap::new());
    let mut cache_lame: HashMap<String, i32> = HashMap::new();
    let ans: i32 = lines
        .into_iter()
        .enumerate()
        .map(|(i, line)| {
            if i < 2 {
                return 0;
            }
            // println!("line: {}", line);
            backtrack_lame(line.trim(), &towels, &mut cache_lame)
        })
        .sum();
    println!("Ans: {}", ans);
}
fn part2(lines: &[String]) {
    let towels: Vec<String> = lines
        .get(0)
        .unwrap()
        .split(",")
        .map(str::trim)
        .map(String::from)
        .collect();
    let cache = Mutex::new(HashMap::new());
    // let mut cache_lame: HashMap<String, i64> = HashMap::new();
    let ans: i64 = lines
        .into_iter()
        .enumerate()
        .map(|(i, line)| {
            if i < 2 {
                return 0;
            }
            // println!("line: {}", line);
            // backtrack2_lame(line.trim(), &towels, &mut cache_lame)
            backtrack2(line.trim(), &towels, &cache)
        })
        .sum();
    println!("Ans: {}", ans);
}
fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
