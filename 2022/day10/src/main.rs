use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::collections::HashMap;

#[derive(Debug)]
enum Inst {
	Noop,
	Addx
}

#[derive(Debug)]
struct Cmd {
	op: Inst,
	cycles: usize,
	value: i32,
}

fn main() {
	let args: Vec<String> = env::args().collect();
    let filename = args[1].clone();
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(&file);

	let mut clock : HashMap<usize, Vec<Cmd>> = HashMap::new();
	let mut i : usize = 1;
	let mut j : usize = 1;
	let mut x : i32 = 1;
	let mut step : usize;
	let mut p1 : i32 = 0;
	let mut crt = String::new();

    for (_index, line) in reader.lines().enumerate() {
        let line = line.unwrap();
		let parts = line.split(" ").collect::<Vec<&str>>();

		println!("");
		println!("# clock: {}", i);
		if parts[0] == "noop" {
			let cmd1 = Cmd{op: Inst::Noop, cycles: 1, value: 0};
			println!("! {:?}", cmd1);
			step = 1;
		} else {
			let val : i32 = parts[1].parse().unwrap();
			let cmd1 = Cmd{op: Inst::Addx, cycles: 2, value: val};
			println!("! {:?}", cmd1);
			let cmd2 = Cmd{op: Inst::Addx, cycles: 2, value: val};
			let next = i+1;
			clock.entry(next).and_modify(|v| v.push(cmd1)).or_insert(vec![cmd2]);
			println!("  :: {:?}", clock);
			step = 2;
		}
		j = i;

		// calc
		let mut li : usize = i;
		if li == 20 || li % 40 == 20 {
			println!("XXX i= {} x= {} s= {}", li, x, (li as i32)*x);
			p1 += (li as i32) * x;
		}
		let ci = i % 40;
		println!("__{} {} {}", i, ci, x);
		if ci as i32 == x
			|| (ci > 0 && (ci-1) as i32 == x)
		 	|| (ci > 1 && (ci-2) as i32 == x) {
			crt.push_str("#");
		} else {
			crt.push_str(".");
		}
		//println!("CRT1: [{}]", crt);

		// resolve
		if clock.contains_key(&li) {
			let ve = clock.remove(&li).unwrap();
			println!(" resolve : x={} {:?}", x, ve);
			for cmd in ve {
				x += cmd.value;
			}
			println!(" resolved: x={}", x);
		}
		if step > 1 {
			// calc
			li = i+1;
			if li == 20 || li % 40 == 20 {
				println!("XXX i= {} x= {} s= {}", li, x, (li as i32)*x);
				p1 += (li as i32) * x;
			}

			//println!("__{} {} {}", i, ci, x);
			if (ci+1) as i32 == x
				|| ci as i32 == x
				|| (ci > 0 && (ci-1) as i32 == x) {
				crt.push_str("#");
			} else {
				crt.push_str(".");
			}
			//println!("CRT2: [{}]", crt);
			// resolve
			if clock.contains_key(&li) {
				let ve = clock.remove(&li).unwrap();
				println!(" resolve : x={} {:?}", x, ve);
				for cmd in ve {
					x += cmd.value;
				}
				println!(" resolved: x={}", x);
			}
		}

		i += step;
		//println!("__  x={} i {} j {}", x, i, j);
	}
	if i-1 <= j {
		// resolve
		if clock.contains_key(&i) {
			let ve = clock.get(&i).unwrap();
			println!("");
			println!("post     : x={} {:?}", x, ve);
			for cmd in ve {
				x += cmd.value;
			}
			println!("  post: x={}", x);
		}
	}
	println!("  x={}", x);
	println!("p1: {}", p1);
	println!("");
	println!("{}", &crt[0..40]);
	println!("{}", &crt[40..80]);
	println!("{}", &crt[80..120]);
	println!("{}", &crt[120..160]);
	println!("{}", &crt[160..200]);
	println!("{}", &crt[200..]);

}
