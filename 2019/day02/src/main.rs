extern crate intcode;

use intcode::VM;
use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};

static DEBUG: bool = false;


fn part1(ops: Vec<i64>) -> i64 {
    let inputs: Vec<i64> = Vec::new();
    let mut vm = VM::new(ops, inputs);
    if DEBUG { vm.pp(); }
    vm.run();
    if DEBUG { vm.pp(); }
    return vm.code()[0];
}

fn part2(ops: Vec<i64>) -> i64 {
    let inputs: Vec<i64> = Vec::new();
    let target = 19690720;

    for noun in 0..50 {
        for verb in 0..50 {
            let mut ops2 = ops.clone();
            ops2[1] = noun;
            ops2[2] = verb;
            let mut vm = VM::new(ops2, inputs.clone());
            vm.run();
            if vm.code()[0] == target {
                return 100 * noun + verb;
            }
        }
    }
    return 0;
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let program = args[0].clone();
    if args.len() < 2 {
        println!("Usage: {} /path/to/input", program);
        return;
    }
    let filename = args[1].clone();

    let mut part_num: usize = 1;
    if args.len() > 2 {
        let part = args[2].clone();
        part_num = part.parse().unwrap();
    }

    let file = File::open(filename).unwrap();
    let reader = BufReader::new(file);
    let mut line_iter = reader.lines().map(|l| l.unwrap());
    let line = line_iter.next().unwrap();
    let ops_s : Vec<&str> = line.split(",").collect();

    let mut ops : Vec<i64> = Vec::new();
    let mut op : i64;
    for s in ops_s {
            op = s.parse().unwrap();
            ops.push(op);
    }
    //println!("{:?}", ops);

    if part_num == 2 {
        let p2 = part2(ops);
        println!("Part 2: {}", p2);
    } else if part_num == 0 {
        let p1 = part1(ops);
        println!("Part 0: {}", p1);
    } else {
        ops[1] = 12;
        ops[2] = 2;
        let p1 = part1(ops);
        println!("Part 1: {}", p1);
    }
}
