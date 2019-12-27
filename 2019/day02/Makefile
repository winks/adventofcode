TSC ?= ./node_modules/.bin/tsc --esModuleInterOp
NODE ?= node

help:
	@echo "# TypeScript 3.7.3, 1+2: ~0.07s"
	@echo "FILE=... make run-ts"

day02.js: day02.ts
	${TSC} day02.ts

run-ts: day02.js
	${NODE} day02.js ${FILE} 12 2

.PHONY: help run-ts
