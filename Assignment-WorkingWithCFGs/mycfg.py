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
    

'''

def find_back_edges(cfg, entry):

"""
Find back edges in a CFG using DFS.

    Parameters:

        cfg(dict): mapping {node: [successors]}

        entry(str): starting node

    Returns: list of edges (u,v) where u->v is a back edge

"""


def is_reducible(cfg, entry):

"""
Determine whether a CFG is reducible.

    Parameters:

        cfg(dict): mapping {node: [successors]}

        entry(str): starting node

    Returns: True if the CFG is reducible or False if the CFG is irreducible
"""
'''
                
def mycfg():
    prog = json.load(sys.stdin)
    for func in prog['functions']:
        name_to_block = block_map(basic_block_alg(func['instrs']))
        cfg = cfg_alg(name_to_block)
        
        print('cfg here below')
        print(cfg)
        print('reverse post order below')
        
        print(reverse_postorder(cfg, 'b0'))
             
        print('digraph {} {{'.format(func['name']))
        for name in name_to_block:
            print('  {};'.format(name))
        for name, succs in cfg.items():
            for succ in succs:
                print ('  {} -> {};'.format(name,succ))
        print('}')
                

if __name__ == '__main__':
    mycfg()


