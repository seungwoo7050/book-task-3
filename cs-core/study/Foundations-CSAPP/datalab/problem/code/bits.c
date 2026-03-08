/*
 * bits.c - Data Lab Puzzle Implementations
 *
 * Each function has a maximum operator count (Max ops) and a set of
 * allowed operators listed in the comment header. You must implement
 * the function body using ONLY those operators and integer constants
 * in the range 0x00–0xFF.
 *
 * FLOAT PUZZLES (floatScale2, floatFloat2Int, floatPower2):
 *   - May use any integer/unsigned operators including ||, &&, if, while.
 *   - May NOT use float types, operations, or constants.
 *
 * FORBIDDEN (integer puzzles #1–#10):
 *   - Control flow (if, while, for, switch, ?:, ||, &&)
 *   - Casts, arrays, structs, unions, function calls
 *   - Types other than int
 *   - Constants outside 0x00–0xFF
 */

#if 0
/* 
 * Instructions to Students:
 *
 * STEP 1: Read the following instructions carefully.
 * STEP 2: Modify the body of each function below to implement the described behavior.
 * STEP 3: Run ./dlc bits.c to check for illegal operators.
 * STEP 4: Run make && ./btest to check correctness.
 */
#endif

/* ---------------------------------------------------------------------------
 * Puzzle 1: bitXor
 *   Compute x ^ y using only ~ and &.
 *   Example: bitXor(4, 5) = 1
 *   Allowed ops: ~ &
 *   Max ops: 14
 *   Rating: 1
 */
int bitXor(int x, int y) {
    return 2;  /* TODO: replace with your implementation */
}

/* ---------------------------------------------------------------------------
 * Puzzle 2: tmin
 *   Return the minimum two's complement integer.
 *   Allowed ops: ! ~ & ^ | + << >>
 *   Max ops: 4
 *   Rating: 1
 */
int tmin(void) {
    return 2;  /* TODO */
}

/* ---------------------------------------------------------------------------
 * Puzzle 3: isTmax
 *   Return 1 if x is the maximum two's complement integer, 0 otherwise.
 *   Allowed ops: ! ~ & ^ | +
 *   Max ops: 10
 *   Rating: 1
 */
int isTmax(int x) {
    return 2;  /* TODO */
}

/* ---------------------------------------------------------------------------
 * Puzzle 4: allOddBits
 *   Return 1 if all odd-numbered bits (bits 1,3,5,...,31) in x are set to 1.
 *   Examples: allOddBits(0xFFFFFFFD) = 0, allOddBits(0xAAAAAAAA) = 1
 *   Allowed ops: ! ~ & ^ | + << >>
 *   Max ops: 12
 *   Rating: 2
 */
int allOddBits(int x) {
    return 2;  /* TODO */
}

/* ---------------------------------------------------------------------------
 * Puzzle 5: negate
 *   Return -x.
 *   Example: negate(1) = -1
 *   Allowed ops: ! ~ & ^ | + << >>
 *   Max ops: 5
 *   Rating: 2
 */
int negate(int x) {
    return 2;  /* TODO */
}

/* ---------------------------------------------------------------------------
 * Puzzle 6: isAsciiDigit
 *   Return 1 if 0x30 <= x <= 0x39 (ASCII codes for '0'..'9').
 *   Examples: isAsciiDigit(0x35) = 1, isAsciiDigit(0x3a) = 0, isAsciiDigit(0x05) = 0
 *   Allowed ops: ! ~ & ^ | + << >>
 *   Max ops: 15
 *   Rating: 3
 */
int isAsciiDigit(int x) {
    return 2;  /* TODO */
}

/* ---------------------------------------------------------------------------
 * Puzzle 7: conditional
 *   Implement x ? y : z.
 *   Examples: conditional(2, 4, 5) = 4, conditional(0, 4, 5) = 5
 *   Allowed ops: ! ~ & ^ | + << >>
 *   Max ops: 16
 *   Rating: 3
 */
int conditional(int x, int y, int z) {
    return 2;  /* TODO */
}

/* ---------------------------------------------------------------------------
 * Puzzle 8: isLessOrEqual
 *   Return 1 if x <= y, 0 otherwise.
 *   Examples: isLessOrEqual(4, 5) = 1, isLessOrEqual(5, 4) = 0
 *   Allowed ops: ! ~ & ^ | + << >>
 *   Max ops: 24
 *   Rating: 3
 */
int isLessOrEqual(int x, int y) {
    return 2;  /* TODO */
}

/* ---------------------------------------------------------------------------
 * Puzzle 9: logicalNeg
 *   Implement !x without using the ! operator.
 *   Examples: logicalNeg(3) = 0, logicalNeg(0) = 1
 *   Allowed ops: ~ & ^ | + << >>
 *   Max ops: 12
 *   Rating: 4
 */
int logicalNeg(int x) {
    return 2;  /* TODO */
}

/* ---------------------------------------------------------------------------
 * Puzzle 10: howManyBits
 *   Return the minimum number of bits required to represent x in two's complement.
 *   Examples: howManyBits(12) = 5, howManyBits(298) = 10,
 *             howManyBits(-1) = 1, howManyBits(0) = 1
 *   Allowed ops: ! ~ & ^ | + << >>
 *   Max ops: 90
 *   Rating: 4
 */
int howManyBits(int x) {
    return 0;  /* TODO */
}

/* ---------------------------------------------------------------------------
 * Puzzle 11: floatScale2
 *   Return bit-level equivalent of expression 2*f for floating point argument f.
 *   Both the argument and result are passed as unsigned int's, but they are to be
 *   interpreted as the bit-level representation of single-precision floating point values.
 *   When argument is NaN, return argument.
 *   Allowed ops: Any integer/unsigned ops including ||, &&, if, while
 *   Max ops: 30
 *   Rating: 4
 */
unsigned floatScale2(unsigned uf) {
    return 2;  /* TODO */
}

/* ---------------------------------------------------------------------------
 * Puzzle 12: floatFloat2Int
 *   Return bit-level equivalent of expression (int) f for floating point argument f.
 *   Argument is passed as unsigned int, but it is to be interpreted as the bit-level
 *   representation of a single-precision floating point value. Round toward zero.
 *   Returns 0x80000000u when out of range (including NaN and ±infinity).
 *   Allowed ops: Any integer/unsigned ops including ||, &&, if, while
 *   Max ops: 30
 *   Rating: 4
 */
int floatFloat2Int(unsigned uf) {
    return 2;  /* TODO */
}

/* ---------------------------------------------------------------------------
 * Puzzle 13: floatPower2
 *   Return bit-level equivalent of the expression 2.0^x (2.0 raised to the power x)
 *   for any 32-bit integer x.
 *   The unsigned value that is returned should have the identical bit representation
 *   as the single-precision floating-point number 2.0^x.
 *   If the result is too small to be represented as a denorm, return 0.
 *   If too large, return +INF.
 *   Allowed ops: Any integer/unsigned ops including ||, &&, if, while
 *   Max ops: 30
 *   Rating: 4
 */
unsigned floatPower2(int x) {
    return 2;  /* TODO */
}
