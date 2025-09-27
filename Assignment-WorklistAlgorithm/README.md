# Worklist Algorithm
**Due Date:** October 1, 2025

This folder of the repository contains a Python program to perfrom data flow analyses on Bril programs. Supported analyses include defined variables, live variables, constant propagation, reaching definitions, and available expressions.

## Features
### Defined Variables
Identifies all variables that are defined at each block.
### Live Variables
Determines for each block, which variables are being read at a furter execution point.
### Constant Propagation
Tracks variables whose values are constants. If a variable holds a constant, the analysis propagates the value.
### Reaching Definitions
For each block, identifies which definitions reach the end of the block without being over written.
### Available Expressions
Finds expressions taht have already been computed and whose operands ahve not changed at a given block.

## Usage
Please refer to the /AdvancedCompilers/README.md to view how to run all assignments, including Worklist Algorithm

**NOTE:** AdvancedCompilers Repository must be within the /bril directory as all test cases have been programmed considering said PATH. However, if you clone in a different directory, necessary edits must be made with certain programs.

### Modes
Arguments     | Functionality
------------- | -----------
defined       | runs a defined variables data flow analysis
live          | runs a live variables data flow analysis
cprop         | runs a constant propagation data flow analysis
reaching      | runs a reaching defintions data flow analysis
available     | runs an available expressions data flow analysis

### How to run each mode
Below is how to run each mode. Keep in mind that the provided [path] is subjective to which bril file you want to use and where it is located.

**defined**
```bash
bril2json < ../[path].bril | python3 df.py defined
```

**live**
```bash
bril2json < ../[path].bril | python3 df.py live
```

**cprop**
```bash
bril2json < ../[path].bril | python3 df.py cprop
```

**reaching**
```bash
bril2json < ../[path].bril | python3 df.py reaching
```

**available**
```bash
bril2json < ../[path].bril | python3 df.py available
```
### Actual Example Runs
NOTE: To run the following, the path set up (e.g. where this repository is cloned) must be identical to what is specified in the usage instructions.

```bash
bril2json < ../../examples/test/df/cond.bril | python3 df.py available
```

```bash
bril2json < ../../examples/test/df/cond.bril | python3 df.py reaching
```

## Testing & Test Cases
All test cases are located in the /test subdirectory.

### Testing
Use the following command to enter the directory for testing:
```bash
cd test/
```
To run all test, use:
```bash
turnt *.bril
```

### Test Cases
Below are all the test cases and the functionality for which they test.

1. cond_available.bril - tests the available expressions dataflow analysis.
2. cond_reaching.bril - tests the reaching defintions dataflow analysis.
3. gcd_available.bril - tests the available expressions dataflow analysis.
4. gcd_reaching.bril - tests the reaching defintions dataflow analysis.
5. fact_available.bril - tests the available expressions dataflow analysis.
6. fact_reaching.bril - tests the reaching defintions dataflow analysis.

**Note:** For testing to work, the directory structure must be the same as stated in the AdvancedCompilers' README. 


