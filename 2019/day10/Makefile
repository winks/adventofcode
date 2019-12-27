FILE ?= input.txt
JULIA ?= julia
PY ?= python3


help:
	@echo "# Python 3.6.8, 1+2: ~0.6s"
	@echo "FILE=... make run-python"
	@echo
	@echo "# Julia 1.3.0, 1+2: ~2s"
	@echo "FILE=... make run-julia"

run-julia:
	${JULIA} day10.jl ${FILE}

run-python:
	${PY} day10.py ${FILE}

.PHONY: help run-julia run-python
