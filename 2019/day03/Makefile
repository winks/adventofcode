FILE ?= input.txt
BASH ?= bash


help:
	@echo "# Bash 4.4.20, 1+2: ~46s"
	@echo "FILE=... make run-bash"
	@echo
	@echo "# Nim 1.0.4, 1+2: ~0.01s"
	@echo "FILE=... make run-nim"

bin/day03: day03.nim
	nim compile -d:release day03.nim
	-mkdir bin
	mv day03 bin/day03

run-bash:
	${BASH} day03.sh ${FILE}

run-nim: bin/day03
	./bin/day03 ${FILE}

.PHONY: help run-bash run-nim
