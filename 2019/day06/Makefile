FILE ?= input.txt
LEIN ?= lein
JAVA ?= java
PY ?= python3

CFLAGS ?= -Wall -std=c99 -O2
SRCS = $(wildcard *.c)
OBJS = $(patsubst %.c,bin/%,$(SRCS))

all: $(OBJS)

bin/day%: day%.c
	$(CC) $(CFLAGS) $< -o $@

help:
	@echo "# Python 3.6.8, 1+2: ~0.09s"
	@echo "FILE=... make run-python"
	@echo
	@echo "# Clojure 1.10.1, 1+2: ~7.7"
	@echo "FILE=... make run-clojure"
	@echo "# C ~ GCC 7.4.0, 1+2: ~0.03s"
	@echo "FILE=... make run-c"
	@echo

bin/day06.jar: clojure/src/day06/core.clj
	cd clojure && ${LEIN} uberjar
	-mkdir bin
	mv clojure/target/day06-0.1.0-SNAPSHOT-standalone.jar bin/day06.jar

run-clojure: bin/day06.jar
	${JAVA} -jar bin/day06.jar -i ${FILE}

run-python:
	${PY} day06.py ${FILE}

run-c: bin/day06
	./bin/day06 ${FILE}

.PHONY: help run-clojure run-python run-c
