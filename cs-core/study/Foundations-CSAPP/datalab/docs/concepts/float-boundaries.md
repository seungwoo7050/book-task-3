# Float Puzzle Boundaries

## Why The Float Set Is Different

Puzzles 11~13 drop the "int-only" restriction but replace it with a stricter conceptual
challenge: reason about IEEE 754 layout directly from the bit pattern.

## Required Classification

Every float puzzle starts by classifying the input into one of these groups:

- `exp == 0xFF`: NaN or infinity
- `exp == 0`: denormalized or zero
- otherwise: normalized

That classification drives all later logic.

## Puzzle-Specific Focus

### `floatScale2`

- preserve NaN and infinity
- shift denormals left
- increment the exponent for normalized numbers

### `floatFloat2Int`

- detect overflow early
- return `0x80000000u` for NaN, infinity, or out-of-range values
- round toward zero by shifting the significand

### `floatPower2`

- normalized range: `-126 <= x <= 127`
- denormalized range: `-149 <= x < -126`
- underflow below `-149`
- infinity above `127`

## Boundary Cases Worth Remembering

- smallest denormal: `0x00000001`
- `1.0f`: `0x3F800000`
- `+inf`: `0x7F800000`
- quiet NaN example: `0x7FC00000`
- small positive fraction like `0.5f`: useful for truncation checks
