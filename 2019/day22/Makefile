FILE ?= input.txt
CARGO ?= CARGO

CFLAGS ?= -Wall -std=c99 -O2
SRCS = $(wildcard *.c)
OBJS = $(patsubst %.c,bin/%,$(SRCS))


help:
	@echo "# Rust 1.38.0, 1: ~0.1s "
	@echo "# Rust 1.38.0, 2: ~0.05s"
	@echo "FILE=... make run-rust"
	@echo
	@echo "# C ~ GCC 7.4.0, 1: ~0.1s"
	@echo "# C ~ GCC 7.4.0, 2: ~0.01s"
	@echo "FILE=... make run-c"

all: $(OBJS)

bin/day%: day%.c
	$(CC) $(CFLAGS) $< -o $@

target/release/day22: src/main.rs
	${CARGO} build --release

run-c: run-c-1 run-c-2

run-rust: run-rust-1 run-rust-2

run-c-1: bin/day22
	./bin/day22 ${FILE} 10007 1

run-c-2: bin/day22
	./bin/day22 ${FILE} 10 2

run-rust-1: target/release/day22
	target/release/day22 ${FILE} 10007 1

run-rust-2: target/release/day22
	target/release/day22 ${FILE} 10 2

.PHONY: help run-rust run-c-1 run-c-2 run-c
