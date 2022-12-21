use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::collections::HashMap;

#[derive(Debug, Clone)]
struct Phrase {
    ok: bool,
    num: i32,
    op: String,
    lo: String,
    ro: String,
}

fn resolve(op: &String, left: i32, right: i32) -> i32 {
    let rv : i32;
    //println!("RES {} {} {}", left, op, right);
    if op == "+" {
        rv = left + right;
    } else if op == "-" {
        rv = left - right;
    } else if op == "*" {
        rv = left * right;
    } else if op == "/" {
        rv = left / right;
    } else {
        panic!("{}", op);
    }
    rv
}

fn main() {
	let args: Vec<String> = env::args().collect();
    let filename = args[1].clone();
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(&file);

    let mut todo : HashMap<String, Phrase> = HashMap::new();
    let mut done : HashMap<String, Phrase> = HashMap::new();
    for (_index, line) in reader.lines().enumerate() {
        let line = line.unwrap();
        let parts = line.split(": ").collect::<Vec<&str>>();
        let term = parts[1].split(" ").collect::<Vec<&str>>();
        let name = parts[0].to_string();
        if term.len() < 2 {
            let num : i32 = term[0].parse().unwrap();
            done.insert(name, Phrase{ok: true, num: num,
                op: String::new(), lo: String::new(), ro: String::new()});
        } else {
            todo.insert(name, Phrase{ok: false, num: 0,
                op: term[1].to_owned(),
                lo: term[0].to_owned(), ro: term[2].to_owned()});
        }
	}
    // for k in done.keys() {
        // println!("M {} {:?}", k, done.get(k).unwrap());
    // }
    // for k in todo.keys() {
        // println!("M {} {:?}", k, todo.get(k).unwrap());
    // }
    // println!("# {}/{}", done.len(), todo.len()+done.len());
    // println!("==============");
    let mut running = true;
    loop {
        if !running {
            break;
        }

        let tx = todo.keys();
        let mut tt : Vec<String> = Vec::new();
        for t in tx {
            tt.push(t.clone());
        }
        for t in tt {
            let v0 = todo.get(&t).unwrap();
            if v0.ok {
                continue
            }
            let lm = &v0.lo;
            let rm = &v0.ro;
            //println!("cur: {:?}", v0);
            if done.contains_key(lm) && done.contains_key(rm) {
                let left = &done.get(lm).unwrap();
                let right = &done.get(rm).unwrap();
                //println!("found {} {:?}\n      {} {:?}", lm, left, rm, right);
                if left.ok && right.ok {
                    let res = resolve(&v0.op, left.num, right.num);
                    if t == "root" {
                        running = false;
                        println!("p1: {}", res);
                        break
                    }
                    let v = Phrase{ok: true, num: res,
                        op: String::new(), lo: String::new(), ro: String::new()};
                    done.insert(t.to_owned(), v);
                    todo.remove(&t);
                    break
                }
                continue
            }
        }
    }
}
