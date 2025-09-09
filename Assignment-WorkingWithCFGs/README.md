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

## Testing
All test cases are located in the /test subdirectory.

To run all test, use:
```bash
turnt *.bril
```
**Note:** For testing to work, the directory structure must be the same as stated in the AdvancedCompilers' README. 