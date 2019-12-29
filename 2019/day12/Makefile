FILE ?= input.txt
LUA ?= luajit


help:
	@echo "# Go 1.13, 1+2: ~0.04s"
	@echo "FILE=... make run-go"
	@echo
	@echo "# Lua 5.2, 1: ~0.01s"
	@echo "# Luajit 2.1.0-beta2, 1: ~0.01s"
	@echo "FILE=... make run-lua-1"
	@echo
	@echo "# Lua 5.2, 2: ~4.2s"
	@echo "# Luajit 2.1.0-beta2, 2: ~0.25s"
	@echo "FILE=... make run-lua-2"

bin/day12: day12.go
	-mkdir bin
	go build -f bin/day12

run-go: bin/day12
	./bin/day12 ${FILE}

run-lua-1:
	${LUA} day12.lua ${FILE}

run-lua-2:
	${LUA} day12.lua ${FILE} 2

.PHONY: help run-go run-lua-1 run-lua-2
