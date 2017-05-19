Note from me to future me

Directory sturcture is as follows:
```
adventofcode/year
adventofcode/year/tests
adventofcode/year/Makefile (file)
```

Within `adventofcode/year`, there will be `dayxx.extension`, which is my solution to `dayxx`

Within `adventofcode/year/tests`, there will be test cases for each of the corresponding solutions, formatted as such:
```
	dayxx_nn.in
	dayxx_nn.out // May not be present for all test cases
```

NOTE: Some cases will be handled by `lbTest.h` if easily applicable