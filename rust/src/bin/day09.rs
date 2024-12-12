use rayon::prelude::*;
use regex::Regex;
use std::cmp;
use std::collections::HashMap;
use std::collections::HashSet;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::time::Instant;
use std::usize;

fn main() {
    let lines: Vec<String> = read_lines("../inputs/day9.txt")
        .unwrap()
        .map_while(Result::ok)
        .collect();
    let start = Instant::now();
    part1(&lines);
    part2(&lines);
    let duration = start.elapsed();
    println!(
        "Time taken no i/o: {} seconds and {} nanos and {} millis and {} micros",
        duration.as_secs(),
        duration.as_nanos(),
        duration.as_millis(),
        duration.as_micros()
    )
}

fn is_in_bounds(xi: i64, yi: i64, max_x: i64, max_y: i64) -> bool {
    (0 <= xi && xi <= max_x) && (0 <= yi && yi <= max_y)
}
fn part1(lines: &[String]) {
    let line = lines.first().unwrap();
    let mut t: Vec<Option<i64>> = Vec::new();
    let mut c = 0;
    line.chars().enumerate().for_each(|(i, ch)| {
        let can = ch.to_digit(10).unwrap();
        if i % 2 == 0 {
            for _ in 0..can {
                t.push(Some(c))
            }
            c += 1
        } else {
            for _ in 0..can {
                t.push(None)
            }
        }
    });

    let mut r = t.len() - 1;
    while t[r].is_none() {
        r -= 1;
    }
    for i in 0..t.len() {
        if t[i].is_none() {
            t.swap(i, r);
            while t[r].is_none() {
                r -= 1;
            }
        }
        if i >= r {
            break;
        }
    }
    let mut ans = 0;
    t.iter().enumerate().for_each(|(i, el)| {
        if el.is_none() {
            let u = 1;
        } else {
            ans += i as i64 * el.unwrap();
        }
    });
    println!("pt1: {}", ans);
}
fn part2(lines: &[String]) {
    let line = lines.first().unwrap();
    let mut t: Vec<(i64, Option<i64>)> = Vec::new();
    let mut c = 0;
    line.chars().enumerate().for_each(|(i, ch)| {
        let can = ch.to_digit(10).unwrap() as i64;
        if i % 2 == 0 {
            if can != 0 {
                t.push((can, Some(c)));
            }
            c += 1
        } else {
            t.push((can, None));
        }
    });
    let mut l = 0i64;
    for (i, el) in t.iter().enumerate() {
        if el.1.is_none() {
            l = i as i64;
            break;
        }
    }

    let mut r = 0i64;
    for (i, el) in t.iter().enumerate() {
        if el.1.is_some() {
            r = i as i64;
        }
    }
    let mut first_empty = l;
    while r > 0 {
        if first_empty >= t.len() as i64 {
            break;
        }
        if t[r as usize].1.is_none() {
            r -= 1;
            continue;
        }
        for l in first_empty..r {
            if t[l as usize].1.is_none() && t[l as usize].0 >= t[r as usize].0 {
                if t[l as usize].0 > t[r as usize].0 {
                    let tmp = ((t[l as usize].0 - t[r as usize].0) as i64, None);
                    t.insert((l + 1) as usize, tmp);
                    t.swap(l as usize, (r + 1) as usize);
                    t[(r + 1) as usize] = (t[l as usize].0, None);
                    if l == first_empty {
                        while t[first_empty as usize].1.is_some() {
                            first_empty += 1;
                        }
                    }
                    break;
                } else {
                    t.swap(l as usize, r as usize);
                    if l == first_empty {
                        while t[first_empty as usize].1.is_some() {
                            first_empty += 1;
                        }
                    }
                    break;
                }
            }
        }
        r -= 1;
    }
    let mut ans = 0;
    let mut c = 0;
    t.iter().enumerate().for_each(|(i, el)| {
        for _ in 0..el.0 {
            if el.1.is_none() {
                let u = 1;
            } else {
                ans += c * el.1.unwrap();
            }
            c += 1;
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
