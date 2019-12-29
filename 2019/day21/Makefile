FILE ?= input.txt


help:
	@echo "# Java 1.8.0_222, 1+2: ~0.48s"
	@echo "FILE=... make run-java"

run-java: Day21.class
	java Day21 ${FILE}

Day21.class: day21.java
	javac day21.java

#VM.class: vm.java
#	javac vm.java

.PHONY: help run-java
