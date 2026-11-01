# Code Structure

## Python

### Solutions

The solution file for each day is split into three parts:

1. The **input parser**, which:
    1. Reads input from stdin
    2. Optionally applies post-processing to the input
    3. Stores the resulting data
2. The **solver**, uses the stored data to return answers
    - There is little consitency in how this is used across the solvers
    - Some solvers proceduraly update its internal data so that calling the same method may produce different results
    - Some are more functional, and may be called multiple times with consistent results
3. The **main method**, which orchestrates these, and prints the answer to the console
    - Potentially, in the future, these could be used for automated submission

Each day's main should be the same:

    - Construct a solver object
    - Call the object's input parser
    - Call the solver methods

The input parser and solvers need to be tailored for each day's particular requirements.

### Tests

By structuring the solution code this way, tests can be run either:

1. From the command line, redirecting the contents of each file as the input; or
2. As a unit test, passing in the required data directly to the solver object's `__init__()` method.
