# Phase Patterns

## What The Official Lab Teaches

The reference Bomb Lab is not really six unrelated puzzles. It is a catalog of recurring low-level
patterns.

| Phase family | What to recognize | Companion track analogue |
|---|---|---|
| direct string comparison | address-loaded string followed by equality check | exact phrase validation |
| numeric recurrence | loop-carried dependence over parsed integers | doubling sequence |
| jump table | indexed dispatch into case-specific constants | switch-based value mapping |
| recursive interval search | midpoint recursion and encoded return path | `func4`-style path check |
| nibble lookup table | `input[i] & 0xf` feeding a static table | 6-char masked lookup |
| linked-list reorder | pointer chasing and post-relink invariant | `7 - x` reorder and descending check |
| secret BST walk | hidden entry plus tree-path encoding | `fun7`-style tree traversal |

## Public Explanation Boundary

This repository can publish:

- the pattern names
- the analysis order
- the invariant each family enforces
- the fact that companion implementations cover the same families

This repository should avoid publishing:

- official raw answer strings for a specific bomb
- full official disassembly annotated line by line
- copied private course assets

## Companion Answers Used For Verification

The study-owned mini-bomb accepts these valid phase inputs:

- Phase 1: `Assembly reveals intent.`
- Phase 2: `1 2 4 8 16 32`
- Phase 3: any valid `(index, value)` pair from the local switch table, such as `1 311`
- Phase 4: `6 6`
- Phase 5: `01234.`
- Phase 6: `4 6 2 3 5 1`
- Secret: `35`

These are answers for the companion implementation only. They are not claimed to match any
official course bomb instance.
