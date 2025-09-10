# -*- coding: utf-8 -*-
"""
Aitiana L. Mondragon
CS 4390
Dr. Moore
September 10, 2025
Exercise: Simple Dead Code Elimination
"""
import json
import sys

def eliminate(instructions):
    used = set()
    
    # Collect all used instructions
    for instr in instructions:
        for arg in instr.get('args', []):
            used.add(arg)
            
    # Remove dead code
    optimized_instrs = []
    for instr in instructions:
        dest = instr.get('dest')
        if dest and dest not in used:
            print("Instruction deleted: ", instr, file=sys.stderr)
        else:
            optimized_instrs.append(instr)
    
    return optimized_instrs
            
        

def my_dce():
    program = json.load(sys.stdin)
    for function in program['functions']:
        function['instrs'] = eliminate(function['instrs'])
    
    print(json.dumps(program, indent=2))

    

if __name__ == '__main__':
    my_dce()
