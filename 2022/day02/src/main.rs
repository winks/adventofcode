use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::collections::HashMap;

fn main() {
	let args: Vec<String> = env::args().collect();
    let filename = args[1].clone();
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(&file);

	let mut values = HashMap::new();
	values.insert("X", 1);
	values.insert("Y", 2);
	values.insert("Z", 3);

	values.insert("A Y", 6);
	values.insert("B Z", 6);
	values.insert("C X", 6);

	values.insert("A X", 3);
	values.insert("B Y", 3);
	values.insert("C Z", 3);

	values.insert("A Z", 0);
	values.insert("B X", 0);
	values.insert("C Y", 0);

	let mut score: i32 = 0;
	let mut score2: i32 = 0;

	let mut values2 = HashMap::new();
	values2.insert("A X", 3);
	values2.insert("B X", 1);
	values2.insert("C X", 2);

	values2.insert("A Y", 4);
	values2.insert("B Y", 5);
	values2.insert("C Y", 6);

	values2.insert("A Z", 8);
	values2.insert("B Z", 9);
	values2.insert("C Z", 7);

    for (index, line) in reader.lines().enumerate() {
        let line = line.unwrap();
		let mine = &line[2..3].to_string();
		if values.contains_key(&line as &str) {
			score += values[&line as &str];
		}
		if values.contains_key(&mine as &str) {
			score += values[&mine as &str];
		}
		let res = &line[2..3].to_string();
		println!("{}> [{}] {}", index+1, line.trim(), res);
		if values2.contains_key(&line as &str) {
			score2 += values2[&line as &str];
		}
    }
	
    println!("p1: {}", score);
	println!("p2: {}", score2);
}
