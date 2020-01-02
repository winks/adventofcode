#[derive(Debug, Clone)]
pub struct VM {
    status: i64,
    position: usize,
    code: Vec<i64>,
    inputs: Vec<i64>
}

impl VM {
    pub fn new(code: Vec<i64>, inputs: Vec<i64>) -> VM {
        VM {
            status: 0,
            position: 0,
            code: code,
            inputs: inputs,
        }
    }

    pub fn run(&mut self) {
        let mut finished = false;
        while !finished {
            //println!("pos: {} = {}", self.position, self.code[self.position]);
            if self.code[self.position] == 1 {
                //println!("{} {} {}", self.position+1, self.position+2, self.position+3);
                let a = self.code[self.position+1] as usize;
                let b = self.code[self.position+2] as usize;
                let pos_out = self.code[self.position+3] as usize;
                let val = self.code[a] + self.code[b];
                //println!("{} {} = {}", a, b, val);
                self.code[pos_out] = val;
            } else if self.code[self.position] == 2 {
                let a = self.code[self.position+1] as usize;
                let b = self.code[self.position+2] as usize;
                let pos_out = self.code[self.position+3] as usize;
                let val = self.code[a] * self.code[b];
                self.code[pos_out] = val;
            } else if self.code[self.position] == 99 {
                finished = true;
            } else {
                panic!("Unknown code {} at position {}", self.code[self.position], self.position);
            }
            self.position += 4;
        }
    }

    pub fn code(&mut self) -> Vec<i64> {
        return self.code.clone();
    }

    pub fn pp(&mut self) {
        println!("--------------------------");
        println!("status  : {:?}", self.status);
        println!("position: {:?}", self.position);
        println!("code[]: : {:?}", self.code.len());
        println!("code:   : {:?}", self.code);
    }
}
