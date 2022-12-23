use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::collections::HashMap;

#[derive(Debug)]
struct Pos {
    y: usize,
    x: usize,
    dir: String,
}

#[derive(Debug)]
struct Pos2 {
    y: i32,
    x: i32,
    dir: String,
}

#[derive(Debug)]
struct Way {
    len: usize,
    dir: String,
}

fn pp(map: &Vec<String>, cur: &Pos) {
    for y in 0..map.len() {
        for x in 0..map[y].len() {
            if y == cur.y && x == cur.x {
                print!("{}", cur.dir);
            } else {
                print!("{}", &map[y][x..x+1]);
            }
        }
        println!("");
    }
}

fn ppt(_tile: &Vec<Vec<char>>) {

}

fn turn(cur: &String, next: &str) -> String {
    let turns = "RDLU";
    let i = turns.find(cur).unwrap();
    let mut j = i;
    if next == "R" {
        j += 1;
        if j >= turns.len() {
            j = 0;
        }
    } else {
        if i > 0 {
            j -= 1;
        } else {
            j = turns.len()-1;
        }
    }
    turns[j..j+1].to_string()
}

fn rot_r(v: &Vec<Vec<char>>) -> Vec<Vec<char>> {
    let mut rv : Vec<Vec<char>> = Vec::new();
    for _y in 0..v.len() {
        rv.push(Vec::new());
    }
    for y in (0..v.len()).rev() {
        for x in 0..v.len() {
            rv[x].push(v[y][x]);
        }
    }
    rv
}

fn project(v: &Vec<Vec<char>>, x: usize, y: usize, dir: String) -> Pos {
    for yy in 0..v.len() {
        for xx in 0..v[0].len() {
            if v[yy][xx] == '@' {
                return Pos{y: yy + y, x: xx + x, dir: dir.clone()}
            }
        }
    }
    return Pos{y:0, x:0, dir: String::new()}
}

fn project2(v: &Vec<Vec<char>>, x: i32, y: i32, dir: String) -> Pos2 {
    for yy in 0..v.len() {
        for xx in 0..v[0].len() {
            if v[yy][xx] == '@' {
                return Pos2{y: yy as i32 + y, x: xx as i32 + x, dir: dir.clone()}
            }
        }
    }
    return Pos2{y:0, x:0, dir: String::new()}
}

fn is_void(map: &Vec<String>, x: i32, y: i32) -> bool {
    x < 0 ||
    y < 0 ||
    y >= map.len() as i32 ||
    x >= map[0].len() as i32 ||
    ( &map[y as usize][x as usize..x as usize+1] != "." && &map[y as usize][x as usize..x as usize+1] != "#" )
}

fn gn(cur: &Pos, map: &Vec<String>, lol: &HashMap<String, String>, layout: &Vec<Vec<usize>>) -> Pos {
    let rv = Pos{x:0, y: 0, dir: String::new()};
    let mut side_len = 4;
    if map.len() > 20 {
        side_len = 50;
    }
    let x = cur.x / side_len;
    let y = cur.y / side_len;
    let la = layout[y][x];
    //println!("GN cur: {},{} {},{} > {} [len:{}]", cur.y, cur.x, y, x, side_len, la);
    let k = format!("{}{}", la, cur.dir);
    println!("GN {:?} ({},{}) = {} | {}", cur, y, x, la, k);
    let cu = lol.get(&k).unwrap();
    println!("GN {:?} ({},{}) = {} | {} {} {}", cur, y, x, la, k, cu, side_len);
    let n : usize = cu[0..1].parse().unwrap();
    //let nd = &cu[1..2];
    let mut nx : usize = 0;
    let mut ny : usize = 0;
    for yy in 0..layout.len() {
        for xx in 0..layout[0].len() {
            if layout[yy][xx] == n {
                nx = xx;
                ny = yy;
                break;
            }
        }
    }
    let mut tile : Vec<Vec<char>> = Vec::new();
    for yy in 0..side_len {
        let mut row : Vec<char> = Vec::new();
        let ty = y * side_len + yy;
        //println!("GNX {},{} {},{}",y,x,ty,tx);
        for xx in 0..side_len {
            let tx = x * side_len + xx;
            let tt = &map[ty][tx..tx+1].chars().next().unwrap();
            if ty == cur.y && tx == cur.x {
                row.push('@');
            } else {
                row.push(*tt);
            }
        }
        tile.push(row);
    }
    //println!("TT {:?}", tile);
    let dy = (y as i32 - ny as i32).abs();
    let dx = (x as i32 - nx as i32).abs();
    println!("shapes: dy:{} dx:{}", dy, dx);
    // chevron-shaped
    if dy == 1 && dx == 1 {
        if &cur.dir == "R" {
            if !is_void(&map, cur.x as i32 + side_len as i32, cur.y as i32 + side_len as i32) {
                // down right
                let rr = rot_r(&tile);
                let new_pos = project(&rr, (x+1) * side_len, y * side_len + 1, "D".to_string());
                println!("R:DR TT {:?} {:?}", ppt(&rr), new_pos);
                return new_pos
            } else if !is_void(&map, cur.x as i32 + side_len as i32, cur.y as i32 - side_len as i32) {
                // up right
                let rr = rot_r(&rot_r(&rot_r(&tile)));
                let new_pos = project(&rr, (x+1) * side_len, y * side_len - 1, "U".to_string());
                println!("R:UR TT {:?} {:?}", ppt(&rr), new_pos);
                return new_pos
            } else {
                println!("NOPE chevron R");
            }
        } else if &cur.dir == "L" {
            if !is_void(&map, cur.x as i32 - side_len as i32, cur.y as i32 + side_len as i32) {
                // down left
                let rr = rot_r(&rot_r(&rot_r(&tile)));
                let new_pos = project(&rr, (x-1) * side_len, y * side_len + 1, "D".to_string());
                println!("L:DL TT {:?} {:?}", ppt(&rr), new_pos);
                return new_pos
            } else if !is_void(&map, cur.x as i32 + side_len as i32, cur.y as i32 - side_len as i32) {
                // up left
                let rr = rot_r(&tile);
                let new_pos = project(&rr, (x-1) * side_len, y * side_len - 1, "U".to_string());
                println!("L:UL TT {:?} {:?}", ppt(&rr), new_pos);
                return new_pos
            } else {
                println!("NOPE chevron L");
            }
        } else if &cur.dir == "D" {
            if !is_void(&map, cur.x as i32 - side_len as i32, cur.y as i32 + side_len as i32) {
                // down left
                let rr = rot_r(&tile);
                let new_pos = project(&rr, x * side_len - 1, (y+1) * side_len, "L".to_string());
                println!("D:LD TT {:?} {:?}", ppt(&rr), new_pos);
                return new_pos
            } else if !is_void(&map, cur.x as i32 + side_len as i32, cur.y as i32 - side_len as i32) {
                // down right
                let rr = rot_r(&rot_r(&rot_r(&tile)));
                let new_pos = project(&rr, x * side_len + 1, (y+1) * side_len, "R".to_string());
                println!("D:DL TT {:?} {:?}", ppt(&rr), new_pos);
                return new_pos
            } else {
                println!("NOPE chevron D");
            }
        } else if &cur.dir == "U" {
            if !is_void(&map, cur.x as i32 - side_len as i32, cur.y as i32 - side_len as i32) {
                // up left
                let rr = rot_r(&rot_r(&rot_r(&tile)));
                let new_pos = project(&rr, x * side_len - 1, (y-1) * side_len, "L".to_string());
                println!("U:LD TT {:?} {:?}", ppt(&rr), new_pos);
                return new_pos
            } else if !is_void(&map, cur.x as i32 + side_len as i32, cur.y as i32 - side_len as i32) {
                // up right
                let rr = rot_r(&tile);
                let new_pos = project(&rr, x * side_len + 1, (y-1) * side_len, "R".to_string());
                println!("U:UR TT {:?} {:?}", ppt(&rr), new_pos);
                return new_pos
            } else {
                println!("NOPE chevron U");
            }
        }
    } else if ( dy == 1 && dx == 2 ) || ( dy == 2 && dx == 1 ) {
        // L-shaped
        if &cur.dir == "R" {
            if !is_void(&map, cur.x as i32 + side_len as i32, cur.y as i32 + 2 * side_len as i32) {
                // down,down,right
                let rr = rot_r(&rot_r(&tile));
                let new_pos = project(&rr, (x+2) * side_len, (y+2) * side_len - 1, "L".to_string());
                println!("RR:DDR TT {:?} {:?}", ppt(&rr), new_pos);
                return new_pos
            } else if !is_void(&map, cur.x as i32 - side_len as i32, cur.y as i32 - 2 * side_len as i32) {
                // up,up,left
                let rr = rot_r(&rot_r(&tile));
                let new_pos = project(&rr, x * side_len - 1, (y-2) * side_len, "L".to_string());
                println!("RR:UUL TT {:?} {:?}", ppt(&rr), new_pos);
                return new_pos
            } else if !is_void(&map, cur.x as i32 + side_len as i32, cur.y as i32 - 2 * side_len as i32) {
                // up,up,right
                let rr = rot_r(&rot_r(&tile));
                let new_pos = project(&rr, (x+2) * side_len - 1, (y-2) * side_len, "L".to_string());
                println!("RR:UUR TT {:?} {:?}", ppt(&rr), new_pos);
                return new_pos
            } else if !is_void(&map, cur.x as i32 - side_len as i32, cur.y as i32 + 2 * side_len as i32) {
                // down,down,left
                let rr = rot_r(&rot_r(&tile));
                let new_pos = project(&rr, x * side_len - 1, (y+2) * side_len, "L".to_string());
                println!("RR:DDL TT {:?} {:?}", ppt(&rr), new_pos);
                return new_pos
            } else {
                println!("NOPE Ls R");
            }
        } else if &cur.dir == "L" {
            if !is_void(&map, cur.x as i32 - side_len as i32, cur.y as i32 + 2 * side_len as i32) {
                // down,down,left
                let rr = rot_r(&rot_r(&tile));
                let mut mx : i32 = x as i32;
                mx = (mx-2) * side_len as i32 + 1;
                if mx < 0 {
                    let new_pos = project2(&rr, mx, (y as i32+2) * side_len as i32, "R".to_string());
                    return Pos{y: new_pos.y as usize, x: 0, dir: new_pos.dir}
                } else {
                    let new_pos = project(&rr, (x-2) * side_len + 1, (y+2) * side_len, "R".to_string());
                    println!("LL:DDL TT {:?} {:?}", ppt(&rr), new_pos);
                    return new_pos
                }
            } else if !is_void(&map, cur.x as i32 + side_len as i32, cur.y as i32 - 2 * side_len as i32) {
                // up,up,right
                let rr = rot_r(&rot_r(&tile));
                let new_pos = project(&rr, x * side_len + 1, (y-2) * side_len, "R".to_string());
                println!("LL:UUR TT {:?} {:?}", ppt(&rr), new_pos);
                return new_pos
            } else {
                println!("NOPE Ls L");
            }
        } else if &cur.dir == "D" {
            if !is_void(&map, cur.x as i32 - 2 * side_len as i32, cur.y as i32 - side_len as i32) {
                // up,left,left
                let rr = rot_r(&rot_r(&tile));
                let new_pos = project(&rr, (x-2) * side_len, y * side_len - 1, "U".to_string());
                println!("DD:ULL TT {:?} {:?}", ppt(&rr), new_pos);
                return new_pos
            } else if !is_void(&map, cur.x as i32 + 2 * side_len as i32, cur.y as i32 - side_len as i32) {
                // up,right,right
                let rr = rot_r(&rot_r(&tile));
                let new_pos = project(&rr, (x+2) * side_len, y * side_len - 1, "U".to_string());
                println!("DD:URR TT {:?} {:?}", ppt(&rr), new_pos);
                return new_pos
            } else {
                println!("NOPE Ls D");
            }
        } else if &cur.dir == "U" {
            if !is_void(&map, cur.x as i32 - 2 * side_len as i32, cur.y as i32 - side_len as i32) {
                // down,left,left
                let rr = rot_r(&rot_r(&tile));
                let new_pos = project(&rr, (x-2) * side_len , y * side_len + 1, "D".to_string());
                println!("UU:DLL TT {:?} {:?}", ppt(&rr), new_pos);
                return new_pos
            } else if !is_void(&map, cur.x as i32 + 2 * side_len as i32, cur.y as i32 - side_len as i32) {
                // down,right,right
                let rr = rot_r(&rot_r(&tile));
                let new_pos = project(&rr, (x+2) * side_len, y * side_len + 1, "D".to_string());
                println!("UU:DL TT {:?} {:?}", ppt(&rr), new_pos);
                return new_pos
            } else {
                println!("NOPE Ls U");
            }
        }
    } else if ( dy == 1 && dx == 3 ) || ( dy == 3 && dx == 1 ) {
        // the long s shape
        if &cur.dir == "R" {
            if !is_void(&map, cur.x as i32 + side_len as i32, cur.y as i32 + 2 * side_len as i32) {
                // down,down,right
                let rr = rot_r(&rot_r(&tile));
                let new_pos = project(&rr, (x+2) * side_len, (y+2) * side_len - 1, "L".to_string());
                println!("!!!RR:DDR TT {:?} {:?}", ppt(&rr), new_pos);
                return new_pos
            } else if !is_void(&map, cur.x as i32 - side_len as i32, cur.y as i32 - 2 * side_len as i32) {
                // up,up,left
                let rr = rot_r(&rot_r(&tile));
                let new_pos = project(&rr, x * side_len - 1, (y-2) * side_len, "L".to_string());
                println!("!!!RR:UUR TT {:?} {:?}", ppt(&rr), new_pos);
                return new_pos
            } else {
                println!("NOPE S R");
            }
        } else if &cur.dir == "L" {
            if !is_void(&map, cur.x as i32 + side_len as i32, cur.y as i32 - 3 * side_len as i32) {
                // up,up,up,right
                let rr = rot_r(&rot_r(&rot_r(&tile)));
                let mut mx : i32 = x as i32;
                mx = (mx+1) * side_len as i32;
                let mut my : i32 = y as i32;
                my = (my-4) * side_len as i32 + 1;
                println!("FOO1 {} {}", my, mx);
                if mx < 0 || my < 0 {
                    let new_pos = project2(&rr, mx, my, "d".to_string());
                    println!("~LLL:UUUR TT {:?} {:?}", ppt(&rr), new_pos);
                    return Pos{y: 0, x: new_pos.x as usize, dir: new_pos.dir}
                } else {
                    let new_pos = project(&rr, (x+1) * side_len + 1, (y-4) * side_len - 1, "D".to_string());
                    println!("LLL:UUUR TT {:?} {:?}", ppt(&rr), new_pos);
                    return new_pos
                }
            } else if !is_void(&map, cur.x as i32 + 3 * side_len as i32, cur.y as i32 - side_len as i32) {
                // down,right,right,right
                let rr = rot_r(&tile);
                let new_pos = project(&rr, (x+3) * side_len, (y+2) * side_len - 1, "U".to_string());
                println!("LLL:URRR TT {:?} {:?}", ppt(&rr), new_pos);
                return new_pos
            } else {
                println!("NOPE S L");
            }
        } else if &cur.dir == "D" {
            if !is_void(&map, cur.x as i32 - 3 * side_len as i32, cur.y as i32 - side_len as i32) {
                // up,left,left,left
                let rr = rot_r(&rot_r(&rot_r(&tile)));
                let new_pos = project(&rr, (x-4) * side_len, y * side_len - 1, "U".to_string());
                println!("DDD:ULLL TT {:?} {:?}", ppt(&rr), new_pos);
                return new_pos
            } else if !is_void(&map, cur.x as i32 - 3 * side_len as i32, cur.y as i32 - side_len as i32) {
                // up,up,up,right NOPOOOO
                let rr = rot_r(&rot_r(&tile));
                let new_pos = project(&rr, (x+2) * side_len, y * side_len - 1, "U".to_string());
                println!("!!!!!DD:URR TT {:?} {:?}", ppt(&rr), new_pos);
                return new_pos
            } else {
                println!("NOPE S D");
            }
        } else if &cur.dir == "U" {
            if !is_void(&map, cur.x as i32 - side_len as i32, cur.y as i32 + 3 * side_len as i32) {
                // down,down,down,left
                let rr = &rot_r(&tile);
                let mut mx : i32 = x as i32;
                mx = (mx-2) * side_len as i32 + 1;
                if mx < 0 {
                    let new_pos = project2(&rr, mx, (y as i32+3) * side_len as i32, "R".to_string());
                    println!("UUU:DDDL TT {:?} {:?}", ppt(&rr), new_pos);
                    return Pos{y: new_pos.y as usize, x: 0, dir: new_pos.dir}
                } else {
                    let new_pos = project(&rr, (x-2) * side_len + 1, (y+3) * side_len, "R".to_string());
                    println!("UUU:DDDL TT {:?} {:?}", ppt(&rr), new_pos);
                    return new_pos
                }
            } else if !is_void(&map, cur.x as i32 + 2 * side_len as i32, cur.y as i32 - side_len as i32) {
                // down,right,right
                let rr = rot_r(&rot_r(&tile));
                let new_pos = project(&rr, (x+2) * side_len, y * side_len + 1, "D".to_string());
                println!("!!UU:DL TT {:?} {:?}", ppt(&rr), new_pos);
                return new_pos
            } else {
                println!("NOPE S U");
            }
        }
    } else if ( dy == 2 && dx == 3 ) || ( dy == 3 && dx == 2 ) {
        // the weird m shape
        if &cur.dir == "U" {
            if !is_void(&map, cur.x as i32 - 2 * side_len as i32, cur.y as i32 + 3 * side_len as i32) {
                // down,down,down,left,left
                let rr = rot_r(&rot_r(&rot_r(&rot_r(&tile))));
                let new_pos = project(&rr, (x-2) * side_len, (y+4) * side_len - 1, "U".to_string());
                println!("UUUU:DDDLL TT {:?} {:?}", ppt(&rr), new_pos);
                return new_pos
            } else {
                println!("NOPE M U");
            }
        } else if &cur.dir == "D" {
            if !is_void(&map, cur.x as i32 + 2 * side_len as i32, cur.y as i32 - 3 * side_len as i32) {
                // up,up,up,right,right
                let rr = rot_r(&rot_r(&rot_r(&rot_r(&tile))));
                println!("FOO1 {} ", (x+2) * side_len);
                let mut my : i32 = y as i32;
                my = (my-4) * side_len as i32 + 1;
                println!("FOO2 {} ", my);
                if my < 0 {
                    let new_pos = project2(&rr, (x as i32+2) * side_len as i32, (y as i32-4) * side_len as i32 + 1, "d".to_string());
                    println!("DDDD:UUULL TT {:?} {:?}", ppt(&rr), new_pos);
                    return Pos{y:0, x: new_pos.x as usize, dir: new_pos.dir}
                } else {
                    let new_pos = project(&rr, (x+2) * side_len, (y-4) * side_len + 1, "D".to_string());
                    println!("DDDD:UUULL TT {:?} {:?}", ppt(&rr), new_pos);
                    return new_pos
                }
            }
            else {
                println!("NOPE M D");
            }
        }
    }

    println!("GN fail {} ({},{}) {:?}", n, ny, nx, rv);
    rv
}

fn p1(map: &Vec<String>, curx: &Pos, inst: &Vec<Way>) -> usize {
    let mut cur = Pos{y: curx.y, x: curx.x, dir: curx.dir.clone()};
    for i in 0..inst.len() {
        //println!("CUR {:?}", cur);
        println!("NOW {:?}", inst[i]);
        for _s in 0..inst[i].len {
            if cur.dir == "R" {
                let mut next = " ";
                if cur.x + 2 <= map[cur.y].len() {
                    next = &map[cur.y][cur.x+1..cur.x+2];
                }
                //println!("next R: {} ({},{})", next, cur.y, cur.x);
                if next == "." {
                    cur.x += 1;
                } else if next == "#" {
                    break;
                } else if next == " " {
                    //println!("overflow");
                    let pos_floor = map[cur.y].find(".").unwrap();
                    let pos_wall  = map[cur.y].find("#").unwrap();
                    if pos_floor < pos_wall {
                        cur.x = pos_floor;
                    }
                } else {
                    panic!("aaa");
                }
            } else if cur.dir == "L" {
                let mut next = " ";
                if cur.x >= 1 {
                    next = &map[cur.y][cur.x-1..cur.x];
                }
                //println!("next L: {}", next);
                if next == "." {
                    cur.x -= 1;
                } else if next == "#" {
                    break;
                } else if next == " " {
                    //println!("overflow");
                    let pos_floor = map[cur.y].rfind(".").unwrap();
                    let pos_wall  = map[cur.y].rfind("#").unwrap();
                    if pos_floor > pos_wall {
                        cur.x = pos_floor;
                    }
                } else {
                    panic!("aaa");
                }
            } else if cur.dir == "D" {
                let mut next = " ";
                if cur.y + 1 < map.len() {
                    next = &map[cur.y+1][cur.x..cur.x+1];
                }
                //println!("next D: {} ({},{})", next, cur.y, cur.x);
                if next == "." {
                    cur.y += 1;
                } else if next == "#" {
                    break;
                } else if next == " " {
                    //println!("overflow");
                    let mut tmp_row = String::new();
                    for y in 0..cur.y+1 {
                        let cx = &map[y][cur.x..cur.x+1].chars().next().unwrap();
                        tmp_row.push(*cx);
                    }
                    //println!("T|{}|", tmp_row);
                    let pos_floor = tmp_row.find(".").unwrap();
                    let pos_wall  = tmp_row.find("#").unwrap();
                    if pos_floor < pos_wall {
                        cur.y = pos_floor;
                    }
                } else {
                    panic!("aaa");
                }
            } else if cur.dir == "U" {
                let mut next = " ";
                if cur.y >= 1 {
                    next = &map[cur.y-1][cur.x..cur.x+1];
                }
                //println!("next U: {} ({},{})", next, cur.y, cur.x);
                if next == "." {
                    cur.y -= 1;
                } else if next == "#" {
                    break;
                } else if next == " " {
                    //println!("overflow");
                    let mut tmp_row = String::new();
                    for y in 0..map.len() {
                        let cx = &map[y][cur.x..cur.x+1].chars().next().unwrap();
                        tmp_row.push(*cx);
                    }
                    //println!("T|{}|", tmp_row);
                    let pos_floor = tmp_row.rfind(".").unwrap();
                    let pos_wall  = tmp_row.rfind("#").unwrap();
                    if pos_floor > pos_wall {
                        cur.y = pos_floor;
                    }
                } else {
                    panic!("aaa");
                }
            }
        }
        let nd = turn(&cur.dir, &inst[i].dir);
        if &inst[i].dir != "" {
            cur.dir = nd;
        }
        println!("CUR {:?}", cur);
        //println!("");
        //pp(&map, &cur);
    }
    let mut f = 0;
    if cur.dir == "D" {
        f = 1;
    } else if cur.dir == "L" {
        f = 2;
    } else if cur.dir == "U" {
        f = 3;
    }
    println!("p1: {}", 1000 * (cur.y+1) + 4 * (cur.x+1) + f);
    1000 * (cur.y+1) + 4 * (cur.x+1) + f
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let filename = args[1].clone();
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(&file);

    let mut map : Vec<String> = Vec::new();
    for (_index, line) in reader.lines().enumerate() {
        let line = line.unwrap();
        if line.len() < 1 {
            continue
        }
        map.push(line);
    }
    let ins = map.pop().unwrap();
    // 2L
    //let ins = "2R4R4L1R7".to_string();
    // 4R
    //let ins = "2R5L4".to_string();
    let mut llen = map[0].len();
    for y in 0..map.len() {
        if map[y].len() > llen {
            llen = map[y].len();
        }
    }
    for y in 0..map.len() {
        if map[y].len() < llen {
            for _x in 0..(llen-map[y].len()) {
                map[y].push(' ');
            }
        }
    }

    let mut inst : Vec<Way> = Vec::new();
    let mut i = 1;
    let mut last = 0;
    while i < ins.len() {
        let c = &ins[i..i+1];
        if c == "R" || c == "D" || c == "L" || c == "U" {
            let len : usize = ins[last..i].parse().unwrap();
            let w = Way{len: len, dir: c.to_string()};
            inst.push(w);
            i += 2;
            last = i-1;
            continue
        }
        i += 1;
    }
    let epos = ins.rfind(&inst[inst.len()-1].dir).unwrap();
    //let end = &ins[epos+1..ins.len()];
    let end : usize = ins[epos+1..ins.len()].parse().unwrap();
    //println!("{} {}", epos, end);
    inst.push(Way{len: end, dir: String::new()});
    //println!("I {}", ins);
    //println!("I {:?}", inst);
    //println!("{:?}", map);

    let mut cur = Pos{y: 0, x: 0, dir: "R".to_owned() };
    'start: for y in 0..map.len() {
        if map[y].contains(".") {
            for x in 0..map[y].len() {
                if &map[y][x..x+1] == "." {
                    cur.y = y;
                    cur.x = x;
                    break 'start;
                }
            }
        }
    }
    let cur0 = Pos{x: cur.x, y: cur.y, dir: cur.dir.clone()};
    pp(&map, &cur);
    let p1r = p1(&map, &cur, &inst);

    let layout : Vec<Vec<usize>>;
    let mut lol2 = HashMap::new();
    if map.len() < 20  {
        layout = vec![
            vec![0,0,1,0],
            vec![2,3,4,0],
            vec![0,0,5,6],
        ];
        // 1 U = 2 U
        // 1 L = 3 U
        // 1 R = 6 R
            // 2 U = 1 U
        // 2 L = 6 D
        // 2 D = 5 D
            // 3 U = 1 L
        // 3 D = 5 L
        // 4 R = 6 U
            // 5 L = 3 D
            // 5 D = 2 D
            // 6 U = 4 R
            // 6 R = 1 R
            // 6 D = 2 L
        lol2.insert("1U".to_string(), "2U".to_string());
        lol2.insert("1L".to_string(), "3U".to_string());
        lol2.insert("1R".to_string(), "6R".to_string());
        lol2.insert("2L".to_string(), "6D".to_string());
        lol2.insert("2D".to_string(), "5D".to_string());
        lol2.insert("3D".to_string(), "5L".to_string());
        lol2.insert("4R".to_string(), "6U".to_string());
    } else {
        // 1 U = 6 L
        // 1 L = 4 L
        // 2 U = 6 D
        // 2 R = 5 R
        // 2 D = 3 R
        // 3 L = 4 U
            // 3 R = 2 D
            // 4 U = 3 L
            // 4 L = 1 L
            // 5 R = 2 R
        // 5 D = 6 R
        layout = vec![
            vec![0,1,2],
            vec![0,3,0],
            vec![4,5,0],
            vec![6,0,0],
        ];
        lol2.insert("1U".to_string(), "6L".to_string());
        lol2.insert("1L".to_string(), "4L".to_string());
        lol2.insert("2U".to_string(), "6D".to_string());
        lol2.insert("2R".to_string(), "5R".to_string());
        lol2.insert("2D".to_string(), "3R".to_string());
        lol2.insert("3L".to_string(), "4U".to_string());
        lol2.insert("5D".to_string(), "6R".to_string());
    }
    let kk = lol2.clone();
    for k in kk.keys() {
        let v = lol2.get(k).unwrap().clone();
        lol2.insert(v, k.clone());
    }
    //// p2
    cur = cur0;
    for i in 0..inst.len() {
        println!("STEP {}/{} {:?}", i+1, inst.len(), inst[i]);
        println!("CUR {:?}", cur);
        println!("CUR2 {} {} {}", cur.x, cur.y, cur.dir);
        for _s in 0..inst[i].len {
            let mut next = " ";
            if cur.dir == "R" {
                if cur.x + 2 <= map[cur.y].len() {
                    next = &map[cur.y][cur.x+1..cur.x+2];
                }
                println!("next R: {} ({},{})", next, cur.y, cur.x);
                if next == "." {
                    cur.x += 1;
                } else if next == "#" {
                    break;
                } else if next == " " {
                    let mut g = gn(&cur, &map, &lol2, &layout);
                    if g.dir == "r" {
                        g.x = 0;
                        g.dir = "R".to_string();
                    }
                    println!("overflow, {:?}", g);
                    if &map[g.y][g.x..g.x+1] == "#" {
                        println!("o wall {:?}", cur);
                    } else {
                        cur = g;
                    }
                    continue
                }
            } else if cur.dir == "L" {
                if cur.x >= 1 {
                    next = &map[cur.y][cur.x-1..cur.x];
                }
                println!("next L: {}", next);
                if next == "." {
                    cur.x -= 1;
                } else if next == "#" {
                    break;
                } else if next == " " {
                    let mut g = gn(&cur, &map, &lol2, &layout);
                    if g.dir == "d" {
                        //cur.x = 0;
                        g.y = 0;
                        g.dir = "D".to_string();
                    }
                    println!("overflow, {:?}", g);
                    if &map[g.y][g.x..g.x+1] == "#" {
                        println!("o wall {:?}", cur);
                    } else {
                        cur = g;
                    }
                    continue
                }
            } else if cur.dir == "D" {
                if cur.y + 1 < map.len() {
                    next = &map[cur.y+1][cur.x..cur.x+1];
                }
                println!("next D: {} ({},{})", next, cur.y, cur.x);
                if next == "." {
                    cur.y += 1;
                } else if next == "#" {
                    break;
                } else if next == " " {
                    let g = gn(&cur, &map, &lol2, &layout);
                    println!("overflow, {:?}", g);
                    if &map[g.y][g.x..g.x+1] == "#" {
                        println!("o wall {:?}", cur);
                    } else {
                        cur = g;
                        if cur.dir == "d" {
                            cur.y = 0;
                            cur.dir = "D".to_string();
                        }
                    }
                    continue
                }
            } else if cur.dir == "U" {
                if cur.y >= 1 {
                    next = &map[cur.y-1][cur.x..cur.x+1];
                }
                println!("next U: {} ({},{})", next, cur.y, cur.x);
                if next == "." {
                    cur.y -= 1;
                } else if next == "#" {
                    break;
                } else if next == " " {
                    let mut g = gn(&cur, &map, &lol2, &layout);
                    if g.dir == "r" {
                        //cur.x = 0;
                        g.x = 0;
                        g.dir = "R".to_string();
                    }
                    println!("overflow, {:?}", g);
                    if &map[g.y][g.x..g.x+1] == "#" {
                        println!("o wall {:?}", cur);
                    } else {
                        cur = g;
                    }
                    continue
                }
            }
        }
        let nd = turn(&cur.dir, &inst[i].dir);
        if i < inst.len() - 1 {
            cur.dir = nd;
        }
        //println!("CUR {:?}", cur);
        //println!("");
        //pp(&map, &cur);
    }
    let mut f = 0;
    if cur.dir == "D" {
        f = 1;
    } else if cur.dir == "L" {
        f = 2;
    } else if cur.dir == "U" {
        f = 3;
    }
    println!("p1: {}", p1r);
    println!("p2: {}", 1000 * (cur.y+1) + 4 * (cur.x+1) + f);
    //println!("{} {} {} {}", cur.y, cur.x, f, cur.dir);
    // 131279 too high
}
