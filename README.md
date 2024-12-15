# Advent of Code

## Running days
To run a day (c++ only) with main input, use:
```
a="src/main/_2020/day01.bin"
make "$a" && time ./$a < $(echo "${a%*.*}_00.in" | sed 's/main/test/')
```

Some java files are hardcoded to run with the main input already
Otherwise, anything that expects input to come from stdin, can be done similarly

## Directory sturcture
```
adventofcode/Makefile (file)
adventofcode/src/{main,test}/{_year,template,util}
```

The underscore allows the year to be used as a code organiser (e.g. valid Java package identifier)

### `adventofcode/src/main`
#### `_year`
contains solutions for a given day xx in the form of `dayxx.ext`

#### `template`
contains templates for java and c++ solutions

quite sparse right now

#### `util`
contains helper functions/classes/etc. to be used by the daily solutions for all languages

### `adventofcode/src/test`
contains test cases for each of the corresponding solutions, formatted as such:
```
	dayxx_nn.in
```
where xx is the day, and nn is the test case for that day

Should use `*_00.txt` for the actual input/solution set and `*_0[1-9].in` for smaller test inputs

Later, I'll move all my unit testing into here under `TestDayXX.java` (probably c++ too, but not sure how yet)


## Commit messages
- refer to the days with padded numbers (e.g. day01, day10)
- refer to the years without underscores (e.g. 2017, 2018)
- refer to year/day combinations as year/day (e.g. 2018/day01)

- where possible, commit with the year/day combination to be as explicit as possible
	- this avoids unwanted confusion with mixing up the years

