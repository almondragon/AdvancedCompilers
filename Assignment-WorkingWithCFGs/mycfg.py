# -*- coding: utf-8 -*-
"""
Aitiana L. Mondragon
CS 4390
Dr. Moore
September 3, 2025
Assignment: Control Flow Graph (CFG) Program
"""

import json
import sys
import getopt
from collections import deque # for queue implementation

TERMS = 'jmp', 'br', 'ret' # terminators used to indicate a change of control flow

## FUNCTIONS for creating a control flow graph (CFG)

# The function basic_block_alg takes instructions and forms the basic blocks of the cfg
def basic_block_alg(instructions):
    block = []
    for i in instructions:
        if 'op' in i:
            block.append(i)
            if i['op'] in TERMS:
                yield block
                block = []
        else:
            yield block
            block = [i]
    
    yield block

# The function block_map maps out all the blocks of the cfg
def block_map(blocks):
    out = {}
    
    for block in blocks:
        if not block:
            continue
        first = block[0]
        if isinstance(first, dict) and 'label' in first:
            name = first['label']
        else:
            name = 'b{}'.format(len(out))
            
        out[name] = block
        
    return out

# The function cfg_alg takes the block_map and creates a cfg   
def cfg_alg(nameblock_map):
    cfg = {}
    names = list(nameblock_map.keys())
    for name, block in nameblock_map.items():
        last = block[-1]
        if last['op'] == 'jmp':
            cfg[name] = last['labels']
        elif last['op'] == 'br':
            cfg[name] = [last['labels'][0], last['labels'][1]]
        else:
            index = names.index(name)
            if index + 1 < len(names):
                next_block = names[index+1]
                cfg[name] = [next_block]
            else:
                cfg[name] = [] 
                
    return cfg


## FUNCTIONS for Working with CFGs assignment

# The function get_path_lengths serves to return the lengths of each path it takes to go to each node from the given entry point
def get_path_lengths(cfg, entry):
    
    path_lengths = {}
    visited = set()
    q = deque()
    
    q.append(entry)
    visited.add(entry)
    
    path_lengths[entry] = 0
    
    while q:
        current_node = q.popleft()
        successors = cfg[current_node]
        for succ in successors:
            if succ not in visited:
                visited.add(succ)
                q.append(succ)
                path_lengths[succ] = path_lengths[current_node] + 1
                
    return path_lengths
          
# The function reverse_postorder returns a list of nodes in reverse post order
def reverse_postorder(cfg, entry):
    
    visited = set()
    post_order = []
    
    def dfs_traversal(node):
        visited.add(node)
        successors = cfg[node]
        for succ in sorted(successors): 
            if succ not in visited:
                dfs_traversal(succ)
        post_order.append(node)
    dfs_traversal(entry)
    
    return list(reversed(post_order))
    


#The function find_back_edges returns a list of edges where one vertex is the ancestor of a current vertex in the recursion tree
def find_back_edges(cfg, entry):
    
    back_edges = []
    visited = set ()
    ancestors = set()
    
    def dfs_traversal(node):
        visited.add(node)
        ancestors.add(node)
        successors = cfg[node]
        for succ in sorted(successors): 
            if succ not in visited:
                dfs_traversal(succ)
            elif succ in ancestors:
                back_edges.append((node, succ))
        ancestors.remove(node)
    dfs_traversal(entry)
    
    if len(back_edges) == 0:
        return 'There are no back edges found in this CFG.'
    else:
        return back_edges
    
        
# The fuction is_reducible determines where a CFG is reducible or not  
def is_reducible(cfg, entry):    

    reduced_cfg = {}    
        
    # remove self-edges
    for node in cfg:
        reduced_successors = [succ for succ in cfg[node] if succ != node]
        reduced_cfg[node] = reduced_successors
        
    # merge with predecessor
    def compute_predecessors(cfg):
        predecessors = {node: set() for node in cfg}
        
        for src in cfg:
            for dest in cfg[src]:
                predecessors[dest].add(src)
                
        return predecessors
    
    predecessors = compute_predecessors(reduced_cfg)
    
    # reduce
    
    while True:
        modification = False 
        for node in list(reduced_cfg):
            if node == entry:
                continue 
            node_predeccesors = list(predecessors[node])
            if len(node_predeccesors) == 1:
                pred = node_predeccesors[0]
                
                # merge node successors into predeccessors successors
                
                for succ in reduced_cfg[node]:
                    if succ != pred and succ not in reduced_cfg[pred]:
                        reduced_cfg[pred].append(succ)
                        predecessors[succ].add(pred)
                    predecessors[succ].discard(node)
                    
                del reduced_cfg[node]
                del predecessors[node]
                
                if node in reduced_cfg[pred]:
                    reduced_cfg[pred].remove(node)
                
                modification = True
                break
            
        if not modification:
            break
        
    return len(reduced_cfg) == 1 and entry in reduced_cfg
                
                
                
def mycfg():
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "clpbr")
    except getopt.GetoptError as err:
        print(err)
        print("Usage: python3 mycfg.py [-c|-l|-p|-b|-r]")
        sys.exit(1)
        
    mode = opts[0][0]
    
    prog = json.load(sys.stdin)
    
    for func in prog['functions']:
        name_to_block = block_map(basic_block_alg(func['instrs']))
        cfg = cfg_alg(name_to_block)
        
        entry = list(name_to_block.keys())[0] # pulling the first block
        
        if mode == "-c":
            print('digraph {} {{'.format(func['name']))
            for name in name_to_block:
                print('  {};'.format(name))
            for name, succs in cfg.items():
                for succ in succs:
                    print ('  {} -> {};'.format(name,succ))
            print('}')
        elif mode == "-l":
            lengths = get_path_lengths(cfg, entry)
            print(json.dumps(lengths, indent=2))
        elif mode == "-p":
            order = reverse_postorder(cfg, entry)
            print("This is the reverse order: ", order)
        elif mode == "-b":
            back_edges = find_back_edges(cfg, entry)
            if back_edges:
                print(back_edges)
            else:
                print("No back edges were found in the given CFG.")
        elif mode == "-r":
            reducible = is_reducible(cfg, entry)
            if reducible:
                print("Reducible")
            else:
                print("Not reducible")
        else:
            print("Invalid mode. Use -c, -l, -p, -b, or -r.")
        
        
            
            
                     
        
                

if __name__ == '__main__':
    mycfg()


