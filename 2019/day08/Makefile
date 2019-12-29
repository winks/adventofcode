FILE ?= input.txt


help:
	@echo "# SBCL 1.4.5, 1+2: ~0.1s"
	@echo "FILE=... make run-cl"
	@echo
	@echo "# C++, 1+2: ~0.1s"
	@echo "FILE=... make run-cpp"
	@echo
	@echo "# D, 1: ~0.003s"
	@echo "# D, 2: ~0.004s"
	@echo "FILE=... make run-d"

run-cpp:
	../bin/day08 ${FILE}

bin/day08: day08.cl
	sbcl --load day08.cl
	-mkdir bin
	mv day08 bin/day08

run-cl:
	./bin/day08 ${FILE} 25 6

bin/day08d: day08.d
	dmd day08.d
	-mkdir bin
	mv day08 bin/day08d

run-d:
	./bin/day08d ${FILE} 25 6 1
	./bin/day08d ${FILE} 25 6 2

.PHONY: help run-cl run-cpp run-d
