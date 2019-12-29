FILE ?= input.txt


help:
	@echo "# Java 1.8.0_222, 1: ~0.35s"
	@echo "FILE=... make run-java"
	@echo "FILE=... make run-play"

run-java: Day25.class Point.class
	java Day25 ${FILE} auto

run-play: Day25.class Point.class
	java Day25 ${FILE}

Day25.class: day25.java
	javac day25.java

Point.class: point.java
	javac point.java

#VM.class: vm.java
#	javac vm.java

.PHONY: help run-java run-play
