use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn series(upper: usize) -> i64 {
    let mut rv = 0;
    let base : i64 = 5;
    for i in 0..(upper+1) {
        rv += base.pow(i as u32) * 2;
    }
    rv
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let filename = args[1].clone();
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(&file);
    let mut p1d : i64 = 0;
    let base : i64 = 5;
    for (_index, line) in reader.lines().enumerate() {
        let line = line.unwrap();
        let mut pp : Vec<char> = line.chars().collect();
        pp.reverse();
        //println!("{:?}", pp);
        let mut step = 0;
        let mut num = 0;
        for p in pp {
            let mut val : i64 = 0;
            if p == '1' {
                val = 1;
            } else if p == '2' {
                val = 2;
            } else if p == '-' {
                val = -1;
            } else if p == '=' {
                val = -2;
            }
            if step == 0 {
                num += 1 * val;
            } else {
                num += base.pow(step) * val;
            }
            //println!("s: {} s: {} v: {} = {}", step, base.pow(step), val, num);
            step += 1;
        }
        //println!("{} = {}", line, num);
        p1d += num;
    }
    println!("p1: {}", p1d);
    let mut p1s = p1d;
    let mut p1 : Vec<i64> = Vec::new();
    for i in (0..25).rev() {
        //println!("\n___i: {} @ {} :: {} :: {} {} {}", i, p1s, p1s > half, base.pow(i), half, dbl);       
        let r = p1s / base.pow(i);
        if r > 0 || p1.len() > 0 {
            p1.push(r);
            p1s -= r * base.pow(i);
        }
        //println!("  5^{} = {} :: {} || {:?}", i, base.pow(i), p1s, p1);
    }
    for i in (1..p1.len()).rev() {
        //println!("{} {}", i , p1[i]);
        if p1[i] > 2 {
            p1[i] -= 5;
            p1[i-1] += 1;
        }
        //println!("{:?}", p1);
    }
    if p1[0] > 2 {
        p1[0] -= 5;
        p1.insert(0, 1);
    }
    println!("{:?} ", p1);
    println!("p1: ");
    for i in p1 {
        if i == -2 {
            print!("=");
        } else if i == -1 {
            print!("-");
        } else {
            print!("{}", i);
        }
    }
    println!("");
}
