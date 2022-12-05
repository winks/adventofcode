use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() {
	let args: Vec<String> = env::args().collect();
    let filename = args[1].clone();
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(&file);

	let mut p1 = 0;
	let mut p2 = 0;
    for (_index, line) in reader.lines().enumerate() {
		let line = line.unwrap();
		let parts = line.split(",").collect::<Vec<&str>>();
		let lef = parts[0].split("-").collect::<Vec<&str>>();
		let rig = parts[1].split("-").collect::<Vec<&str>>();
		//println!("{:?} {:?}", lef, rig);

		let ll : i32 = lef[0].parse().unwrap();
		let lh : i32 = lef[1].parse().unwrap();
		let rl : i32 = rig[0].parse().unwrap();
		let rh : i32 = rig[1].parse().unwrap();

		if (rl >= ll && rh <= lh) || (ll >= rl && lh <= rh) {
			p1 += 1;
		}
		if (rl >= ll && rl <= lh) || (ll >= rl && ll <= rh) {
			p2 += 1;
		}
	}
	println!("p1: {}", p1);
	println!("p2: {}", p2);
}
