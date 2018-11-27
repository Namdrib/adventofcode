# Advent of Code

## Directory sturcture
```
adventofcode/Makefile (file)
adventofcode/_year
adventofcode/_year/tests
adventofcode/util
```

The underscore allows the year to be used as a code organiser (e.g. valid Java package identifier)

## `adventofcode/_year`
in the year folder, `dayxx.extension` is my solution to `dayxx`

## `adventofcode/_year/tests`
contains test cases for each of the corresponding solutions, formatted as such:
```
	dayxx_nn.in
	dayxx_nn.out // May not be present for all test cases
```
Should use `*_00.txt` for the example small input/solution set and `*_01.in` for the actual input

NOTE: Some cases will be handled by `lbTest.h` if easily applicable

## `adventofcode/util`
contains helper functions/classes/etc. for all languages
