# Reverse-Engineering Workflow

## Goal

Bomb Lab is solved by reducing an unknown binary into a sequence of smaller claims:

1. how input is parsed
2. what values are compared
3. what control-flow shape appears
4. what data structure is being traversed
5. what final invariant must hold

## Default Loop

### 1. Install a safety brake

- Set `break explode_bomb` first.
- If the bomb is hostile to repeated explosions, also keep an answers file for already solved phases.

### 2. Confirm the input contract

Before reverse-engineering the phase body, determine:

- how many arguments are read
- whether they are integers or strings
- whether range checks happen before the core logic

This avoids building the wrong mental model around the wrong input shape.

### 3. Classify the control-flow pattern

Common patterns:

- direct string compare
- counted loop or recurrence
- jump table or switch
- recursion over a numeric interval
- lookup table indexed by masked bytes
- pointer chasing through a linked structure

### 4. Translate to pseudocode

The important artifact is not the raw assembly dump. The important artifact is a small pseudocode
model that preserves the branch conditions and invariants.

### 5. Verify with one phase-sized claim at a time

- validate the parsing claim
- validate the next comparison or branch target
- only then write the candidate answer

## Why The Companion Mini-Bomb Exists

The official bomb binary is an external course asset. This study migration therefore uses a second
deliverable: a fresh C/C++ companion bomb that mirrors the same phase families and keeps the
repository executable, testable, and publishable.
