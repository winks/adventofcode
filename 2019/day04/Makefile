FILE ?= input.txt
PHP ?= php
TCL ?= tclsh
PY ?= python3


help:
	@echo "# Python 3.6.8, 1+2: ~0.04s"
	@echo "FILE=... make run-python"
	@echo
	@echo "# PHP 7.2.24, 1+2: ~0.04s"
	@echo "FILE=... make run-php"
	@echo
	@echo "# Tcl 8.6.8, 1: ~0.9s"
	@echo "# Tcl 8.6.8, 2: ~1.0s"
	@echo "FILE=... make run-tcl"

run-php:
	${PHP} day04.php ${FILE}

run-python:
	${PY} day04.py ${FILE}

run-tcl:
	${TCL} day04.tcl ${FILE}

.PHONY: help run-php run-python run-tcl
