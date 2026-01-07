# Code Structure

## Python

### Solutions

The solution file for each day is split into three parts:
1. The **input parser**, which reads input from stdin, and returns formatted data;
2. The **solver**, which takes in the formatted data in the `__init__()` method; and
3. The **main method**, which orchestrates these

Each day's main should be the same - it should call the input parser, storing the return values, and then create a solver object, passing in the formatted data.
The input parser and solvers need to be tailored for each day's particular requirements.

The solver should return the solution, which main prints for human consumption (or, potentially in the future, for automated submission)

### Tests

By structuring the solution code this way, tests can be run either:

1. From the command line, redirecting the contents of each file as the input; or
2. As a unit test, passing in the required data directly to the solver object's `__init__()` method.
