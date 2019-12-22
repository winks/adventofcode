use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};
use regex::Regex;

#[derive(Debug)]
enum Action { Nope, DealNew, Cut, DealInc }

#[derive(Debug)]
pub struct Step {
    action: Action,
    arg: i32,
}

fn parse(s: &str) -> Step {
    let re_deal_new = Regex::new(r"^deal into new stack$").unwrap();
    let re_deal_inc = Regex::new(r"^deal with increment (\d+)$").unwrap();
    let re_cut = Regex::new(r"^cut (\d+)$").unwrap();
    if re_deal_new.is_match(s) {
        Step {
            action: Action::DealNew,
            arg: 0
        }
    } else if re_deal_inc.is_match(&s) {
        let m = re_deal_inc.captures(&s).unwrap();
        let num = m.get(1).map_or("", |m| m.as_str());
        let num2: i32 = num.parse().unwrap();
        Step {
            action: Action::DealInc,
            arg: num2,
        }
    } else if re_cut.is_match(&s) {
        let m = re_cut.captures(&s).unwrap();
        let num = m.get(1).map_or("", |m| m.as_str());
        let num2: i32 = num.parse().unwrap();
        Step {
            action: Action::Cut,
            arg: num2,
        }
    } else {
        Step {
            action: Action::Nope,
            arg: 0
        }
    }
}

fn main() {
    println!("Hello, world!");
    let args: Vec<String> = env::args().collect();
    let program = args[0].clone();
    if args.len() < 3 {
        println!("Usage: {} /path/to/input deck_size", program);
    }
    let filename = args[1].clone();
    let size = args[2].clone();
    let deck_size: usize = size.parse().unwrap();

    let file = File::open(filename).unwrap();
    let reader = BufReader::new(file);

    let mut steps: Vec<Step> = Vec::new();

    for (index, line) in reader.lines().enumerate() {
        let line = line.unwrap();
        println!("{}> {}", index+1, line.trim());
        let step = parse(line.trim());
        println!("{:?}", step);
        steps.push(step);
    }

    let mut deck_orig: Vec<u32> = Vec::with_capacity(deck_size);
    let mut deck: Vec<u32> = Vec::with_capacity(deck_size);
    let mut decks: Vec<Vec<u32>> = Vec::new();
    for i in 0..deck_size {
        deck_orig.push(i as u32);
    }
}
