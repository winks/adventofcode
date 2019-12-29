FILE ?= input.txt


help:
	@echo "# Java 1.8.0_222, 1+2: ~0.4s"
	@echo "FILE=... make run-java"
	@echo
	@echo "# C++, 1+2: TBD"
	@echo "FILE=... make run-cpp"

run-java: Day09.class VM.class
	java Day09 ${FILE}

Day09.class: day09.java
	javac day09.java

VM.class: vm.java
	javac vm.java

run-cpp:
	../bin/day09 ${FILE}

.PHONY: help run-java run-cpp
