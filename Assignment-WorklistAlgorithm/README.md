# Working with CFGs
**Due Date:** September 12, 2025

This folder of the repository contains a Python program for constructing control flow graphs (CFGs) for Bril programs. The code also implements additional functionality including computing path lengths, reverse post order traversal, back edge detection, as well as checking reducibility.

## Features
### CFG Construction
1. **basic_block_alg(instructions)** - takes a bril program's instructions and turns them into basic blocks

2. **block_map(blocks)** - maps basic blocks to names

3. **cfg_alg(nameblock_map)** - creates a CFG when given a map of named blocks.

### CFG Analysis
4. **get_path_lengths(cfg, entry)** - computes the shortest path length (in edges) from the entry node to each node in the CFG.

5. **reverse_postorder(cfg, entry)** - compute reverse postorder for a CFG.

6. **find_back_edges(cfg,entry)** - find back edges in a CFG using DFS.

7. **is_reducible(cfg, entry)** - determines whether a CFG is reducible.

## Usage
Please refer to the /AdvancedCompilers/README.md to view how to run all assignments, including Working with CFGs

**NOTE:** AdvancedCompilers Repository must be within the /bril directory as all test cases have been programmed considering said PATH. However, if you clone in a different directory, necessary edits must be made with certain programs.

### Modes
Arguments         | Functionality
------------- | -----------
-c            | creates a cfg and prints it
-l            | find the path lengths of a cfg
-p            | computes the reverse post order for a CFG
-b            | finds all the back edges within a CFG
-r            | determines where a CFG is reducible

### How to run each mode
Below is how to run each mode. Keep in mind that the provided [path] is subjective to which bril file you want to use and where it is located.

**-c**
```bash
bril2json < ../[path].bril | python3 mycfg.py -c
```

**-l**
```bash
bril2json < ../[path].bril | python3 mycfg.py -l
```

**-p**
```bash
bril2json < ../[path].bril | python3 mycfg.py -p
```

**-b**
```bash
bril2json < ../[path].bril | python3 mycfg.py -b
```

**-r**
```bash
bril2json < ../[path].bril | python3 mycfg.py -r
```
### Actual Example Runs
NOTE: To run the following, the path set up (e.g. where this repository is cloned) must be identical to what is specified in the usage instructions.

```bash
bril2json < ../../test/interp/core/jmp.bril | python3 mycfg.py -c
```

```bash
bril2json < ../../benchmarks/core/gcd.bril | python3 mycfg.py -l
```
### To run GraphViz
NOTE: To run the following, the path set up (e.g. where this repository is cloned) must be identical to what is specified in the usage instructions.
```bash
bril2json < ../../benchmarks/core/gcd.bril | python3 mycfg.py -c | dot -Tpdf -o cfg.pdf
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

1. figure8_back_edges.bril - tests the back_edge functionality
2. figure8_cfg.bril - test the cfg generation functionality
3. figure8_lengths.bril - test the get path lengths functionality
4. figure_reducible.bril - test whether the cfg is reducible functionality
5. figure_reverse_postorder.bril - test reverse post order functionality
6. gcd_back_edges.bril - tests the back_edge functionality
7. gcd_cfg.bril - test the cfg generation functionality 
8. gcd_lengths.bril - test the get path lengths functionality
9. gcd_reducible.bril - test whether the cfg is reducible functionality
10. gcd_reverse_postorder.bril - test reverse post order functionality
11. jmp_back_edges.bril - tests the back_edge functionality
12. jmp_cfg.bril - test the cfg generation functionality
13. jmp_lengths.bril - test the get path lengths functionality
14. jmp_reducible.bril - test whether the cfg is reducible functionality
15. jmp_reverse_postorder.bril - test reverse post order functionality

**Note:** For testing to work, the directory structure must be the same as stated in the AdvancedCompilers' README. 


