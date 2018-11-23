# Makefile for adventofcode

CFLAGS = -std=gnu++11 -O2
JFLAGS = -Xlint

%.bin: %.cpp
	g++ -o $@ $^ $(CFLAGS)

%.class: %.java
	javac $^ $(JFLAGS)

clean:
	rm -rf a *.class *.exe *.bin

# Run tests like this:
# make dayxx && time for item in tests/dayxx_*.in ;do cat $item | ./a [optional args]; done
