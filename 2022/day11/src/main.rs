use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};

#[derive(Debug, Clone)]
struct Op {
	infix: String,
	operand: u32,
	square: bool,
}

#[derive(Debug, Clone)]
struct Monkey {
	id: u32,
	items: Vec<u32>,
	op: Op,
	test: u32,
	t: u32,
	f: u32,
	insp: u32,
}

fn fx(monkeys: Vec<Monkey>) -> Vec<u32> {
	let mut mx : Vec<u32> = Vec::new();
	for mo in &monkeys {
		mx.push(mo.insp);
	}
	mx
}

fn main() {
	let args: Vec<String> = env::args().collect();
    let filename = args[1].clone();
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(&file);

	let mut monkeys : Vec<Monkey> = Vec::new();
	let mut monkey = Monkey{ id: 0, items: Vec::new(), test: 0, t: 0, f: 0, insp: 0, op: Op {infix: String::new(),operand: 0, square: false} };
	let mut maxid : u32 = 0;

    for (index, line) in reader.lines().enumerate() {
        let line = line.unwrap();
		if line.len() < 1 {
			continue;
		}
		let parts = line.split(" ").collect::<Vec<&str>>();
		//println!("p {:?}", parts);
		if parts[0] == "Monkey" && index > 1 {
			let v2 = monkey.items.clone();
			let m2 = Monkey { id: monkey.id, t: monkey.t, f: monkey.f, items: v2, test: monkey.test, insp: 0, op: Op {infix: monkey.op.infix.clone(), operand: monkey.op.operand, square: monkey.op.square}};
			if monkey.id > maxid {
				maxid = monkey.id;
			}
			monkeys.push(m2);
			//println!("Ms {:?}", monkeys);
			
			let idx = parts[1].split(":").collect::<Vec<&str>>();
			let id : u32 = idx[0].parse().unwrap();
			monkey.id = id;
		} else if parts.len() > 3 && parts[2] == "Starting" {
			let r = line.split(":").collect::<Vec<&str>>();
			let r2 = r[1].replace(" ", "");
			let ix = r2.split(",").collect::<Vec<&str>>();
			//println!("X {:?}", ix);
			monkey.items.clear();
			for i in ix {
				let id : u32 = i.parse().unwrap();
				monkey.items.push(id);
			}
		} else if parts.len() > 3 && parts[2] == "Operation:" {
			let o1 = line.split("new = old ").collect::<Vec<&str>>();
			//println!("__ {:?}", o1);
			let o2 = o1[1].split(" ").collect::<Vec<&str>>();
			let mut sq = false;
			let mut o3 : u32 = 0;
			if o2[1] == "old" {
				sq = true;
			} else {
				o3 = o2[1].parse().unwrap();
			}
			monkey.op = Op { infix: o2[0].to_string(), operand: o3, square: sq};
			//println!("__ {:?}", monkey);
		} else if parts.len() > 3 && parts[2] == "Test:" {
			let div : u32 = parts[5].parse().unwrap();
			monkey.test = div;
		} else if parts.len() > 5 && parts[5] == "true:" {
			let t : u32 = parts[9].parse().unwrap();
			monkey.t = t;
		} else if parts.len() > 5 && parts[5] == "false:" {
			let f : u32 = parts[9].parse().unwrap();
			monkey.f = f;
		}
		//println!("  M {:?}", monkey);
	}
	let m2 = Monkey { id: monkey.id, t: monkey.t, f: monkey.f, items: monkey.items.clone(), test: monkey.test, insp: 0, op: Op {infix: monkey.op.infix.clone() ,operand: monkey.op.operand, square: monkey.op.square}};
	if monkey.id > maxid {
		maxid = monkey.id;
	}
	monkeys.push(m2);
	for mo in &monkeys {
		println!("Ms {:?}", mo);
	}
	println!("===========================");

	for _i in 0..20 {
		for mid in 0..maxid+1 {
			//println!("# {}", mid);
			let mut insp: u32 = 0;
			let monk = &monkeys[mid as usize].clone();
			for it in (monk.items.clone()).drain(..) {
				//println!(" #  {}", it);
				insp += 1;
				let mut it2 : u32 = it;
				//let mut p2override = false;
				if monk.op.square {
					it2 = it2*it2;
				} else if &monk.op.infix == "+" {
					it2 += monk.op.operand;
				} else if &monk.op.infix == "*" {
					it2 *= monk.op.operand;
				}
				it2 = it2 / 3;
				if it2 % monk.test == 0 {
					monkeys[monk.t as usize].items.push(it2);
				} else {
					monkeys[monk.f as usize].items.push(it2);
				}
			}
			let mmonk = &mut monkeys[mid as usize];
			mmonk.items = Vec::new();
			mmonk.insp += insp;
		}

		let mut mx : Vec<u32> = Vec::new();
		for mo in &monkeys {
			mx.push(mo.insp);
		}
		//println!("TMP Ms {:?}", mx);
	}
	//println!("===========================");
	let mut mx = fx(monkeys);
	mx.sort();
	//println!("Ms {:?}", mx);
	println!("p1: {}", mx[mx.len()-1] * mx[mx.len()-2]);
}
