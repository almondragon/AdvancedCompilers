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

TERMS = 'jmp', 'br', 'ret'

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


                
def mycfg():
    prog = json.load(sys.stdin)
    for func in prog['functions']:
        name_to_block = block_map(basic_block_alg(func['instrs']))
        cfg = cfg_alg(name_to_block)
        
        print('digraph {} {{'.format(func['name']))
        for name in name_to_block:
            print('  {};'.format(name))
        for name, succs in cfg.items():
            for succ in succs:
                print ('  {} -> {};'.format(name,succ))
        print('}')
        
        

if __name__ == '__main__':
    mycfg()


