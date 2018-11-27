# Makefile for adventofcode

CFLAGS = -std=gnu++11 -O2 -Wall
JFLAGS = -Xlint

%.bin: %.cpp
	g++ -o $@ $^ $(CFLAGS)

%.class: %.java
	javac $^ $(JFLAGS)

clean:
	find ./ -type f \( -iname a -o -iname \*.class -o -iname \*.exe -o -name \*.bin \) -delete

# Run tests like this:
# make dayxx && time for item in tests/dayxx_*.in ;do cat $item | ./a [optional args]; done
