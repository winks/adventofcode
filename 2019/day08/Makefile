FILE ?= input.txt


help:
	@echo "# SBCL 1.4.5, 1+2: ~0.1s"
	@echo "FILE=... make run-cl"

bin/day08: day08.cl
	sbcl day08.cl
	-mkdir bin
	mv day08 bin/day08

run-cl:
	./bin/day08 ${FILE} 25 6

.PHONY: help run-cl
