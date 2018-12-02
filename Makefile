# Makefile for adventofcode

CFLAGS = -std=gnu++11 -O2 -Wall
JFLAGS = -Xlint

%.bin: %.cpp
	g++ -o $@ $^ $(CFLAGS)

%.class: %.java
	javac $^ $(JFLAGS)

clean:
	find ./ -type f \( -iname a -o -iname \*.class -o -iname \*.exe -o -name \*.bin \) -print0 -delete

# Run tests like this:
# a="_2018/day01.bin"; make "$a" && ./"$a" < _2018/tests/day01_01.in # cpp
# a="_2018/day01"; make "$a.class" && ./"$a" < _2018/tests/day01_01.in # java
