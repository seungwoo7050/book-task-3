# Integer Puzzle Patterns

## Why The Integer Set Matters

Puzzles 1~10 force the same habit repeatedly: stop thinking in source-level intent and start
thinking in bit patterns, sign propagation, and operator substitution.

## Repeated Patterns

### 1. Boolean To Mask

- pattern: `(!!x << 31) >> 31`
- use: branchless selection
- appears in: `conditional`

### 2. Subtraction By Two's Complement

- pattern: `x + (~y + 1)`
- use: range checks and comparisons without `-`
- appears in: `isAsciiDigit`, `isLessOrEqual`

### 3. Sign-Bit Reasoning

- pattern: `x >> 31`
- use: distinguish negative from non-negative values
- appears in: `isAsciiDigit`, `isLessOrEqual`, `howManyBits`

### 4. Dense Mask Construction

- pattern: build `0xAAAAAAAA` from `0xAA`
- use: satisfy the small-constant rule while still testing full-width bit structure
- appears in: `allOddBits`

### 5. MSB Search By Binary Splitting

- pattern: probe `16 -> 8 -> 4 -> 2 -> 1`
- use: find representation width without loops in the integer puzzle subset
- appears in: `howManyBits`

## Boundary Cases Worth Remembering

- `0`: often the only value with a missing high bit effect
- `-1`: common false positive in maximum-value checks
- `INT_MIN`: exposes asymmetric two's-complement behavior
- `INT_MAX`: validates positive-edge comparisons

## Verification Focus

- range checks: test just below and above the allowed boundary
- comparison logic: test same-sign and different-sign inputs
- representation-width logic: test `0`, `-1`, `INT_MIN`, `INT_MAX`
