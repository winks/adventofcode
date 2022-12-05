use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() {
	let args: Vec<String> = env::args().collect();
    let filename = args[1].clone();
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(file);

	let mut packs: Vec<i32> = Vec::new();
	let mut cur: i32 = 0;
    for (index, line) in reader.lines().enumerate() {
        let line = line.unwrap();
        println!("{}> [{}]", index+1, line.trim());
		if line.len() < 1 {
			packs.push(cur);
			cur = 0;
			continue;
		}
		let m: i32 = line.parse().unwrap();
		cur += m;
    }
	packs.push(cur);

	let mut max: i32 = 0;
    for pack in &packs {
        println!("{}", pack);
		if pack > &max {
			max = *pack;
		}
	}
    println!("p1: {}", max);
	packs.sort();
	let last = packs.len();
	println!("p2: {}", packs[last-1] + packs[last-2] + packs[last-3]);
}
