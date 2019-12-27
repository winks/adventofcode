FILE ?= input.txt


help:
	@echo "# D, 1+2: ~0.6s"
	@echo "FILE=... make run-d"
	@echo
	@echo "# Ruby, 1: ~45m"
	@echo "FILE=... make run-ruby-1"
	@echo
	@echo "# Ruby, 2: ~8.5s"
	@echo "FILE=... make run-d-ruby-2"

bin/day16:
	dmd day16.d -O -release -of=bin/day16

run-d: bin/day16
	./bin/day16 ${FILE} 100

run-ruby-1:
	ruby day16.rb ${FILE} 100

run-ruby-2:
	ruby day16.rb ${FILE} 100 2

.PHONY: help run-d run-ruby-1 run-ruby-2
