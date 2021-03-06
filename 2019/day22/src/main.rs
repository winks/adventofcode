use std::env;
use std::convert::TryInto;
use std::fs::File;
use std::io::{BufRead, BufReader};
use regex::Regex;

static DEBUG: bool = true;

#[derive(Debug, Clone, Copy)]
enum Action { Nope, DealNew, Cut, DealInc }

#[derive(Debug, Clone, Copy)]
pub struct Step {
    action: Action,
    arg: i32,
}

fn parse(s: &str) -> Step {
    let re_deal_new = Regex::new(r"^deal into new stack$").unwrap();
    let re_deal_inc = Regex::new(r"^deal with increment (\d+)$").unwrap();
    let re_cut = Regex::new(r"^cut (-?\d+)$").unwrap();
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

fn ppf(v: &Vec<u32>) {
    println!("  cur BOTTOM {:?} TOP", v);
}

fn pp(v: &Vec<u32>) {
    if !DEBUG {
        return;
    }
    if v.len() < 20 {
        //println!("  cur BOTTOM {:?} TOP", v);
        ppf(&v);
    } else {
        println!("  cur BOTTOM [{:?}, {:?}, ... {:?}, {:?}] TOP", v[0], v[1], v[v.len()-2], v[v.len()-1]);
    }
}

fn mod_exp(base: i128, exponent: i128, modulus: i128) -> i128 {
    let mut result = 1;
    let mut base = base % modulus;
    let mut exponent = exponent;

    loop {
        if exponent <= 0 {
            break result;
        }
        if exponent % 2 == 1 {
            result = (result * base) % modulus;
        }
        exponent = exponent >> 1;
        base = (base * base) % modulus;
    }
}

fn shuffle2(pos_orig: u64, steps: &Vec<Step>) {
    let len   : i128 = 119315717514047;
    let times : i128 = 101741582076661;
    let pos : i128 = pos_orig as i128;
    let mut off : i128 = 0;
    let mut inc : i128 = 1;

    for step in steps {
        if DEBUG {
            println!("Current step orig: {:?}", step);
        }
        match step.action {
            Action::DealInc => {
                inc = inc * mod_exp(step.arg as i128, len - 2, len);
            },
            Action::DealNew => {
                off = off - inc;
                inc = -inc;
            },
            Action::Cut => {
                off = off + inc * step.arg as i128;
            },
            Action::Nope => {
            },
        }
        off = off % len;
        inc = inc % len;
    }
    let incr : i128 = mod_exp(inc, times, len);
    let offs : i128 = off * (1 - mod_exp(inc, times, len)) % len;
    let offs = offs * mod_exp(1 - inc, len - 2, len) % len;
    let r : i128 = (offs + incr * pos) % len;
    println!("Part 2: {} -> {}", pos, r);
}

fn shuffle(deck_orig: Vec<u32>, steps: &Vec<Step>, reverse: bool) -> Vec<u32> {
    let deck_size: usize = deck_orig.len();
    let mut deck_cur = deck_orig.clone();

    for step in steps {
        if DEBUG {
            println!("Current step: {:?}", step);
        }
        match step.action {
            Action::DealInc => {
                let mut deck: Vec<u32> = Vec::with_capacity(deck_size);
                for _i in 0..deck_size {
                    deck.push(0);
                }
                let mut i = 0;
                let stepsize: usize = match reverse {
                    false => step.arg.try_into().unwrap(),
                    true => {
                        let ss: usize = step.arg.try_into().unwrap();
                        deck_size - ss
                    }
                };
                while deck_cur.len() > 0 {
                    //println!("i {:?}", i);
                    if i >= deck_orig.len() {
                        i -= deck_size;
                    }
                    //println!("i {:?}", i);
                    let n = deck_cur.pop().unwrap();
                    deck[i] = n;
                    i += stepsize;
                    //println!("dc {:?}", deck_cur);
                    //println!("d {:?}", deck);
                }
                deck.reverse();
                deck_cur = deck;
                pp(&deck_cur);
            },
            Action::DealNew => {
                let mut deck = deck_cur.clone();
                deck.reverse();
                //println!("d: {:?}", deck);
                deck_cur = deck;
                pp(&deck_cur);
            },
            Action::Cut => {
                let mut deck : Vec<u32> = Vec::with_capacity(deck_size);

                if step.arg > 0 {
                    let cut_size: usize = step.arg.try_into().unwrap();
                    let rest_size: usize = match reverse {
                        false => {
                            deck_size - cut_size
                        },
                        true => {
                            cut_size
                        }
                    };
                    let (orig, cut) = deck_cur.split_at(rest_size);
                    //println!("dc {:?}", cut);
                    //println!("dc {:?}", orig);
                    for n in orig {
                        deck.push(*n);
                    }
                    for i in 0..cut.len() {
                        deck.insert(i, cut[i]);
                    }
                } else {
                    let tmp = (step.arg * -1) as usize;
                    let cut_size: usize = match reverse {
                        false => tmp.try_into().unwrap(),
                        true => {
                            deck_size - tmp
                        }
                    };
                    //println!("{:?} {:?}", step.arg, cut_size);
                    let (orig, cut) = deck_cur.split_at(cut_size);
                    //println!("dc {:?}", cut);
                    //println!("dc {:?}", orig);
                    for n in orig {
                        deck.push(*n);
                    }
                    for i in 0..cut.len() {
                        deck.insert(i, cut[i]);
                    }
                }
                deck_cur = deck;
                pp(&deck_cur);
            },
            Action::Nope => {
            },
        }
    }
    pp(&deck_cur);

    return deck_cur;
}

fn part1(deck: Vec<u32>) -> u32 {
    ppf(&deck);
    if deck.len() > 2100 {
        let mut cnt = 1;
        for ii in (0..deck.len()-1).rev() {
            if deck[ii] == 2019 {
                println!("{:?} : {:?} => {:?}", ii, deck[ii], cnt);
                return cnt;
            }
            //println!("X {:?} : {:?} => {:?}", ii, deck[ii], cnt);
            cnt += 1;
        }
    }
    return 0;
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let program = args[0].clone();
    if args.len() < 3 {
        println!("Usage: {} /path/to/input deck_size [2]", program);
    }
    let filename = args[1].clone();
    let size = args[2].clone();
    let deck_size: usize = size.parse().unwrap();

    let mut part_num: usize = 1;
    if args.len() > 3 {
        let part = args[3].clone();
        part_num = part.parse().unwrap();
    }

    let file = File::open(filename).unwrap();
    let reader = BufReader::new(file);

    let mut steps: Vec<Step> = Vec::new();

    for (index, line) in reader.lines().enumerate() {
        let line = line.unwrap();
        println!("{}> {}", index+1, line.trim());
        let step = parse(line.trim());
        //println!("{:?}", step);
        steps.push(step);
    }

    let mut deck_orig: Vec<u32> = Vec::with_capacity(deck_size);
    for i in 0..deck_size {
        deck_orig.push(i as u32);
    }
    deck_orig.reverse();
    let deck_cur = deck_orig.clone();
    //println!("do {:?}", deck_orig);
    println!("------------------");
    pp(&deck_cur);
    println!("------------------");

    if part_num == 2 {
        shuffle2(2020, &steps);
    } else {
        let deck_s = shuffle(deck_cur, &steps, false);
        println!("Part 1: {}", part1(deck_s));
    }
}
