FILE ?= input.txt
CRYSTAL ?= crystal


help:
	@echo "# Crystal 0.31.1, 1+2: ~0.01s"
	@echo "FILE=... make run-crystal"
	@echo
	@echo "# PowerShell, 1+2: ~0.03s"
	@echo "FILE=... make run-powershell"

bin/day01: day01.cr
	${CRYSTAL} build day01.cr
	-mkdir bin
	mv day01 bin/day01

run-crystal: bin/day01
	bin/day01 ${FILE}

run-python:
	Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
	# Measure-Command { ... }
	day01.ps1 ${FILE}

.PHONY: help run-crystal run-powershell
