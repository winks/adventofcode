use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::cmp::Ordering;
use serde_json::{Value, json};

struct Data {
    tp: char,
    intval: u32,
    list: String,
}

fn cmp(lv: &Value, rv: &Value) -> bool {
    if lv == rv {
        return true
    }

    if !lv.is_array() || !rv.is_array() {
        panic!("asdf");
    }
    let la = lv.as_array().unwrap();
    let ll = la.len();

    let ra = rv.as_array().unwrap();
    let rl = ra.len();
    println!("L:[{}] {:?}", ll, lv);
    println!("R:[{}] {:?}", rl, rv);

    if ll == 0 {
        return true
    }
    for i in 0..ll {
        if i >= ra.len() {
            println!(". no more");
            return false;
        }
        println!(".  {:?} | {:?} | {:?}", la[i], ra[i], la[i] == ra[i]);
        if la[i] == ra[i] {
            println!(". ceq");
            continue
        } else if ra[i].is_number() && la[i].is_array() {
            let x = json!([ra[i].as_i64().unwrap()]);
            if x == la[i] {
                continue
            }
            println!("D2: {}", x);
            let r = cmp(&la[i], &x);
            if !r {
                return false;
            }
            return true;
        } else if la[i].is_number() && ra[i].is_array() {
            let x = json!([la[i].as_i64().unwrap()]);
            if x == ra[i] {
                continue
            }
            println!("D1: {}", x);
            let r = cmp(&x, &ra[i]);
            if !r {
                return false;
            }
            return true;
        } else if la[i].is_null() || ra[i].is_null() {
            println!("N1: {}", la[i]);
        } else if la[i].is_array() || ra[i].is_array() {
            println!("A1:");
            let r = cmp(&la[i], &ra[i]);
            if !r {
                return false;
            }
            return true;
        } else if ra[i].as_i64().unwrap() == la[i].as_i64().unwrap() {
            println!(". equal");
            continue;
        } else if ra[i].as_i64().unwrap() < la[i].as_i64().unwrap() {
            println!(". right smaller");
            return false;
        } else if ra[i].as_i64().unwrap() > la[i].as_i64().unwrap() {
            println!(". left smaller");
            return true;
        }
    }
    return true
}

fn main() {
	let args: Vec<String> = env::args().collect();
    let filename = args[1].clone();
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(&file);
    let lines : Vec<_> = reader.lines().collect();
    let mut is_left = true;
    let mut last_line = String::new();
    let mut pair_idx : usize = 1;
    let mut p1 : usize = 0;
    let mut p2 : usize = 1;

    let mut lines2 : Vec<String> = Vec::new();
    for (index, line) in lines.into_iter().enumerate() {
        let line = line.unwrap();
        if line.len() > 0 {
            lines2.push(line.to_string());
        }
        println!(": {}", line);
        if index > 1 && line.len() < 1 {
            is_left = true;
            pair_idx += 1;
            continue
        }
        if is_left {
            last_line = line.to_string();
            is_left = false;
        } else {
            println!("--------------");
            let lv: Value = serde_json::from_str(&last_line).unwrap();
            let rv: Value = serde_json::from_str(&line).unwrap();
            let ok = cmp(&lv, &rv);
            println!("C: {:?}", ok);
            if ok {
                p1 += pair_idx;
            }
            is_left = true;
        }
	}

    //println!("XXX p1 {:?}", p1);
    lines2.push("[[2]]".to_string());
    lines2.push("[[6]]".to_string());
    //println!("XXX {:?}", lines2);
    lines2.sort_by(|a,b| {
        let lv: Value = serde_json::from_str(&a).unwrap();
        let rv: Value = serde_json::from_str(&b).unwrap();
        if cmp(&lv, &rv) {
            return Ordering::Less;
        } else {
            return Ordering::Greater;
        }
    });
    //println!("XXX {:?}", lines2);
    let mut idx = 1;
    for x in lines2 {
        //println!("_ {} __ {}", x, idx);
        if x == "[[2]]" || x == "[[6]]" {
            p2 *= idx;
        }
        idx += 1;
    }
    println!("p1 {:?}", p1);
    println!("p2 {:?}", p2);
}
