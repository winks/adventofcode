FILE ?= input.txt
PERL ?= perl
PY ?= python3


help:
	@echo "# Python 3.6.8, 1: ~0.15s"
	@echo "FILE=... make run-python"
	@echo
	@echo "# Perl 5.26.1, 1+2: ~0.04s"
	@echo "FILE=... make run-julia"

run-perl:
	${PERL} day14.pl ${FILE} 1

run-python:
	${PY} day14.py ${FILE}

.PHONY: help run-perl run-python
