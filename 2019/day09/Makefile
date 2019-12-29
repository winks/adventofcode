FILE ?= input.txt


help:
	@echo "# Java 1.8.0_222, 1+2: ~0.4s"
	@echo "FILE=... make run-java"

run-java: Day09.class VM.class
	java Day09 ${FILE}

Day09.class: day09.java
	javac day09.java

VM.class: vm.java
	javac vm.java

.PHONY: help run-java
