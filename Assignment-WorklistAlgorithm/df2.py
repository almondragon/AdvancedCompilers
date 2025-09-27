# -*- coding: utf-8 -*-
"""
Created on Sat Sep 27 14:38:12 2025

@author: almon
"""

import sys
import json
from collections import namedtuple

from form_blocks import form_blocks
import cfg

# A single dataflow analysis consists of:
# - forward: True for forward, False for backward.
# - init: Initial value.
# - merge: Combine list of values into one.
# - transfer: The transfer function.
Analysis = namedtuple("Analysis", ["forward", "init", "merge", "transfer"])


def union(sets):
    out = set()
    for s in sets:
        out.update(s)
    return out


def intersection(sets):
    if not sets:
        return set()
    result = None
    for s in sets:
        if result is None:
            result = set(s)
        else:
            result &= s
    return result if result is not None else set()


def df_worklist(blocks, analysis):
    """The worklist algorithm for iterating a data flow analysis to a fixed point."""
    preds, succs = cfg.edges(blocks)

    if analysis.forward:
        first_block = list(blocks.keys())[0]  # Entry block
        in_edges = preds
        out_edges = succs
    else:
        first_block = list(blocks.keys())[-1]  # Exit block
        in_edges = succs
        out_edges = preds

    # Initialize
    in_ = {first_block: analysis.init}
    out = {node: analysis.init for node in blocks}

    # Iterate
    worklist = list(blocks.keys())
    while worklist:
        node = worklist.pop(0)

        inval = analysis.merge(out[n] for n in in_edges[node])
        in_[node] = inval

        outval = analysis.transfer(blocks[node], inval, node)

        if outval != out[node]:
            out[node] = outval
            worklist += out_edges[node]

    if analysis.forward:
        return in_, out
    else:
        return out, in_


def fmt(val):
    """Pretty-print sets and dicts"""
    if isinstance(val, set):
        if val:
            return ", ".join(str(v) for v in sorted(val))
        else:
            return "∅"
    elif isinstance(val, dict):
        if val:
            return ", ".join(f"{k}: {v}" for k, v in sorted(val.items()))
        else:
            return "∅"
    else:
        return str(val)


def run_df(bril, analysis_name):
    for func in bril["functions"]:
        blocks = cfg.block_map(form_blocks(func["instrs"]))
        cfg.add_terminators(blocks)

        # Dynamic analyses
        if analysis_name == "reaching":
            analysis = make_reaching_defs(blocks)
        elif analysis_name == "avail":
            analysis = make_avail_exprs(blocks)
        else:
            analysis = ANALYSES[analysis_name]

        in_, out = df_worklist(blocks, analysis)
        for block in blocks:
            print(f"{block}:")
            print("  in: ", fmt(in_[block]))
            print("  out:", fmt(out[block]))


# Helpers

def gen(block):
    """Variables defined in the block."""
    return {i["dest"] for i in block if "dest" in i}


def use(block):
    """Variables read before written in block."""
    defined = set()
    used = set()
    for i in block:
        used.update(v for v in i.get("args", []) if v not in defined)
        if "dest" in i:
            defined.add(i["dest"])
    return used


# Constant Propagation
def cprop_transfer(block, in_vals, _=None):
    out_vals = dict(in_vals)
    for instr in block:
        if "dest" in instr:
            if instr["op"] == "const":
                out_vals[instr["dest"]] = instr["value"]
            else:
                out_vals[instr["dest"]] = "?"
    return out_vals


def cprop_merge(vals_list):
    out_vals = {}
    for vals in vals_list:
        for name, val in vals.items():
            if val == "?":
                out_vals[name] = "?"
            else:
                if name in out_vals:
                    if out_vals[name] != val:
                        out_vals[name] = "?"
                else:
                    out_vals[name] = val
    return out_vals


# Reaching Definitions
def rd_gen(block, label):
    return {(instr["dest"], label) for instr in block if "dest" in instr}


def rd_kill(block, label, all_defs):
    kill_set = set()
    for instr in block:
        if "dest" in instr:
            var = instr["dest"]
            kill_set |= {d for d in all_defs if d[0] == var and d[1] != label}
    return kill_set


def make_reaching_defs(blocks):
    all_defs = set()
    for label, block in blocks.items():
        for instr in block:
            if "dest" in instr:
                all_defs.add((instr["dest"], label))

    def transfer(block, in_vals, label):
        return rd_gen(block, label) | (in_vals - rd_kill(block, label, all_defs))

    return Analysis(
        True,              
        init=set(),
        merge=union,
        transfer=transfer,
    )


# Available Expressions
def expr_of(instr):
    if "dest" in instr and "args" in instr and instr["op"] in {"add", "sub", "mul", "div"}:
        return (instr["op"], tuple(instr["args"]))
    return None


def ae_gen(block):
    return {e for instr in block if (e := expr_of(instr))}


def ae_kill(block, universe):
    kill_set = set()
    for instr in block:
        if "dest" in instr:
            var = instr["dest"]
            kill_set |= {e for e in universe if var in e[1]}
    return kill_set


def make_avail_exprs(blocks):
    universe = set()
    for block in blocks.values():
        for instr in block:
            e = expr_of(instr)
            if e:
                universe.add(e)

    def transfer(block, in_vals, _=None):
        return ae_gen(block) | (in_vals - ae_kill(block, universe))

    def meet(vals):
        if not vals:
            return universe.copy()
        result = universe.copy()
        for v in vals:
            result &= v
        return result

    return Analysis(
        True,               # forward
        init=universe,
        merge=meet,
        transfer=transfer,
    )


# Built-in Analyses
ANALYSES = {
    "defined": Analysis(
        True,
        init=set(),
        merge=union,
        transfer=lambda block, in_, _: in_.union(gen(block)),
    ),
    "live": Analysis(
        False,
        init=set(),
        merge=union,
        transfer=lambda block, out, _: use(block).union(out - gen(block)),
    ),
    "cprop": Analysis(
        True,
        init={},
        merge=cprop_merge,
        transfer=cprop_transfer,
    ),
}


if __name__ == "__main__":
    bril = json.load(sys.stdin)
    run_df(bril, sys.argv[1])
