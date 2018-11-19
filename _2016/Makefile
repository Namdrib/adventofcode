# Makefile for adventofcode

CFLAGS = -std=gnu++11

%: %.cpp
	g++ -o a $^ $(CFLAGS)
	
clean:
	rm -f a
	
	
# Run tests like this:
# make dayxx && time for item in tests/dayxx_*.in ;do cat $item | ./a [optional args]; done