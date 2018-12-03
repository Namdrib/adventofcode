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
## compile
# a = "src/main/java/_2018/day01(.bin)" # .bin if c++

## run
# ./"$a" < src/test/java/_2018/day01_01.in
