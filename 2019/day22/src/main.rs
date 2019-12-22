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

fn shuffle2(deck_size: u64, pos_orig: u64, steps: &Vec<Step>) -> u64 {
    let mut pos = pos_orig;
    let mut pos0 = pos_orig;

    for step in steps {
        if DEBUG {
            println!("Current step orig: {:?}", step);
        }
        pos0 = pos;
        let xarg: u64 = step.arg as u64;
        match step.action {
            Action::DealInc => {
                for i in 0..step.arg {
                let tmp_arg : u64 = xarg;
                //let tmp_arg : u64 = deck_size - xarg;
                pos = (pos * tmp_arg) % deck_size;
                }
            },
            Action::DealNew => {
                pos = deck_size - pos - 1;
            },
            Action::Cut => {
                if step.arg > 0  {
                    pos = (deck_size + pos + xarg) % deck_size;
                } else {
                    let parg = step.arg * -1;
                    pos = (deck_size + pos - parg as u64) % deck_size;
                }
            },
            Action::Nope => {
            },
        }
        println!("pos {} -> {}", pos0, pos);
    }

    return pos;
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

fn part1(deck: Vec<u32>) {
    ppf(&deck);
    if deck.len() > 2100 {
        let mut cnt = 1;
        for ii in (0..deck.len()-1).rev() {
            if deck[ii] == 2019 {
                println!("{:?} : {:?} => {:?}", ii, deck[ii], cnt);
            }
            println!("X {:?} : {:?} => {:?}", ii, deck[ii], cnt);
            cnt += 1;
        }
    }
}

fn part3(_deck: Vec<u32>, steps: &Vec<Step>) {
    let mut s2 = steps.clone();
    s2.reverse();
    let decksize: u64 = 10;

    let mut pos2 = 9;
    pos2 = shuffle2(decksize, pos2, &s2);
    println!("pos2 {}", pos2);
}

fn part2(_deck: Vec<u32>, steps: &Vec<Step>) {
    /*
    let mut i = 0;
    let mut deck_x = deck.clone();
    let s2 = steps.clone();
    while deck_x != deck || i == 0 {
        deck_x = shuffle(deck_x, &s2, false);
        i += 1;
        if i % 1000 == 0 {
            println!("loop {}", i);
        }
    }
    println!("fin {}", i);
    // 101741582076661 - (5003 * 20336114746) = 2423
    */
    let mut s2 = steps.clone();
    s2.reverse();
    //let pos0 = 2020;
    //let decksize: u64 = 119315717514047;
    let decksize: u64 = 10007;
    let pos0 = 6289;

    let mut pos = pos0;
    let mut i: u64 = 0;

    let mut pos2 = 6288;
    pos2 = shuffle2(decksize, pos2, &s2);
    println!("pos2 {}", pos2);
    pos2 = 0;
    pos2 = shuffle2(decksize, pos2, &s2);
    println!("pos2 {}", pos2);
    pos2 = 1;
    pos2 = shuffle2(decksize, pos2, &s2);
    println!("pos2 {}", pos2);
    pos2 = 10005;
    pos2 = shuffle2(decksize, pos2, &s2);
    println!("pos2 {}", pos2);
    pos2 = 10006;
    pos2 = shuffle2(decksize, pos2, &s2);
    println!("pos2 {}", pos2);
/*
    loop {
        pos = shuffle2(decksize, pos, &s2);
        i += 1;
        if i %  1000000 == 0 {
            println!("loop {}", i);
        }
        if pos == pos0 {
            println!("found {} at iter {}", pos, i);
            break;
        }
    }
    println!("pos {}", pos);
    */
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

    if part_num == 3 {
        part3(deck_cur, &steps);
    } else if part_num == 2 {
        part2(deck_cur, &steps);
    } else {
        let deck_s = shuffle(deck_cur, &steps, false);
        part1(deck_s);
    }
}
