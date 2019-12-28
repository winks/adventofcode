CPPFLAGS ?= -Wall -std=c++17 -O2

SRCS = $(wildcard *.cpp)
OBJS = $(patsubst %.cpp,bin/%,$(SRCS))

all: $(OBJS)

bin/day%: day%.cpp
	$(CXX) $(CPPFLAGS) $< -o $@

.PHONY: clean

clean:
	rm -f bin/day*
