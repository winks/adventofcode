use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() {
	let args: Vec<String> = env::args().collect();
    let filename = args[1].clone();
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(&file);

	let mut cnt = 0;
	let mut cnt2 = 0;
	let mut li0 = String::new();
	let mut li1 = String::new();
	let mut li2 = String::new();
    for (index, line) in reader.lines().enumerate() {
        let line = line.unwrap();
		if index % 3 == 2 {
			li2 = line.clone();
		} else if index % 3 == 1 {
			li1 = line.clone();
		} else {
			if index == 0 {
			    li0 = line.clone();
			} else {
				let ii = p2x(&li0, &li1, &li2);
				//println!(">> {}", &li0[ii..ii+1]);
				let x3 = &li0[ii..ii+1].chars().next().unwrap();
				let x4: u32 = *x3 as u32;
				let x5 = p1x(x4);
				cnt2 += x5;
			    li0 = line.clone();
			}
		}
		let lenx = line.len();
		print!("{} {}", lenx, line);
		let c1 = &line[0..(lenx/2)];
		let c2 = &line[(lenx/2)..];
		print!(" :: {} {}", c1.len(), c1);
		println!(" - {} {}", c2.len(), c2);

		'outer: for i in 0..(c1.len()) {
			for j in 0..(c2.len()) {
				if &c1[i..i+1] == &c2[j..j+1] {
					let x3 = &c2[j..j+1].chars().next().unwrap();
					let x4: u32 = *x3 as u32;
					//print!("{} {}", &c1[i..i+1], &c2[j..j+1]);
					let mut x5 = x4;
					if x4 > 96 {
						x5 -= 96;
					} else {
						x5 -= 64;
						x5 += 26;
					}
					//println!(" - {} {}", x4, x5);
					cnt += x5;
					break 'outer;
				}
			}
		}
	}
	let ii = p2x(&li0, &li1, &li2);
	let x3 = &li0[ii..ii+1].chars().next().unwrap();
	let x4: u32 = *x3 as u32;
	let x5 = p1x(x4);
	cnt2 += x5;
	//println!(">> {}", &li0[ii..ii+1]);
	println!("p1: {}", cnt);
	println!("p2: {}", cnt2);
}

fn p1x(x4: u32) -> u32 {
	let mut x5 = x4;
	if x4 > 96 {
		x5 -= 96;
	} else {
		x5 -= 64;
		x5 += 26;
	}
	//println!("__ {} {}", x4, x5);
	return x5;
}

fn p2x(li0: &str, li1: &str, li2: &str) -> usize {
	for i in 0..li0.len() {
		for j in 0..li1.len() {
			for k in 0..li2.len() {
				if &li0[i..i+1] == &li1[j..j+1] && &li0[i..i+1] == &li2[k..k+1] {
					//println!(">> {} {} {}", li0, li1, li2);
					return i;
				}
			}
		}
	}
	return 0;
}
