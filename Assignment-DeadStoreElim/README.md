# Dead Store Elimination
**Due Date:** November 23, 2025

This folder of the repository contains two Passes: MemorySSA and Dead Store Elimination.
1. **MemorySSA Demo Pass** - build and prints MemorySSA information and generates a graphical DOT file of the MemorySSA graph.
2. **Dead Store Elimination (DSE)** - an intraprocedural dead store elimination pass built using MemorySSA.

Both passes operate on LLVM IR (.ll) files and are built as plugin passes for opt.


## Features
### MemorySSA Pass & Graph Construction
1. The pass iterates through each Basic Block and prints:
- MemoryUse
- MemoryDef
- MemoryPhi
2. Generates a DOT file named <function>_MemorySSA.dot
- Nodes represent MemoryAccesses
- Edges represent a defining-access relationship between nodes

### Dead Store Elimination (DSE) Pass
1. Implements a DSE Algorithm:
- Analyzes dead stores found in a function
- Eliminates dead stores found in a function


## Usage
Use the provided commands in order to run each respective pass and generate the proper .ll files.
**NOTE:** It is important to note that you might need to modify the commands based on where you are generating your files, what files you are testing, and what version of LLVM, clang, and opt you are using. 

### File Generation
**Compile into .ll files**
```bash
clang -O0 -Xclang -disable-O0-optnone -S -emit-llvm test_mssa/demo2.c -o test_mssa/demo2.ll
```
**Optimize the .ll files**
```bash
opt -passes=mem2reg test_mssa/demo2.ll -S -o test_mssa/demo2_simplified.ll
```
NOTE: Change test_[name] depending on the pass you are testing (i.e. test_mssa for MemorySSSA and test_dse for Dead Store Elimination).

### Building the Passes
Below is how to build each pass: MemorySSA and DeadStore Elim.

**Compiling MemorySSADemo.cpp**
```bash
clang++ -std=c++17 -fPIC -shared MemorySSADemo.cpp -o libMemorySSADemo.so $(llvm-config-21 --cxxflags --ldflags) -lLLVM
```

**Compiling DeadStoreElim.cpp**
```bash
clang++ -std=c++17 -fPIC -shared DeadStoreElim.cpp -o DeadStoreElim.so \
$(llvm-config-21 --cxxflags --ldflags --libs core analysis passes)
```

### Running the Passes
Below is how to run each pass and generate the graphical view of the MemorySSA.

**Run the MemorySSADemo.cpp pass**
```bash
opt-21 -load-pass-plugin=./libMemorySSADemo.so -passes=memssa-demo \
test_mssa/demo2_simplified.ll -disable-output
```

**Run the DeadStoreElim.cpp pass**
```bash
opt-21 -load-pass-plugin ./DeadStoreElim.so -passes=dead-store-elim test_dse/test_dse1_simp.ll -S -o output_dse/test_dse1_o.ll
```

**Generating the graph**
```bash
dot -Tpng [function_name]_MemorySSA.dot -o MemorySSA.png
```

## Testing & Test Cases
All test cases are located in the /test_dse subdirectory.

### Running Tests
Tests are .ll programs that exercise various DSE scenarios.

NOTE: That to test your own files, you must compile your .c file into LLVM and optimize.

Use the following command to test files in the subdirectory (post compiling and optimization). This can be done manually for each file:
```bash
opt-21 -load-pass-plugin ./DeadStoreElim.so -passes=dead-store-elim test_dse/demo2_simplified.ll -S -o output_dse/demo2_dse.ll
```

### Test Cases
Below are all the test cases and the functionality for which they test. 

1. test_dse1_simp.ll - tests a simple single store program
2. test_dse2_simp.ll - tests a store followed by a load
3. test_dse3_simp.ll - tests multiple pointers
4. test_dse4_simp.ll - tests a store in a loop
5. test_dse5_simp.ll - general testing

**Note:** For testing to work, the directory structure must be the same as stated in the AdvancedCompilers' README. 


