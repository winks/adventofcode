FILE ?= input.txt


help:
	@echo "# Java 1.8.0_222, 1+2: ~0.36s"
	@echo "FILE=... make run-java"

run-java: Day23.class
	java Day23 ${FILE}

Day23.class: day23.java
	javac day23.java

#VM.class: vm.java
#	javac vm.java

.PHONY: help run-java
