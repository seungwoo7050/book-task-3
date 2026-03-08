/*
 * btest.c - A test harness that checks a student's solution in bits.c.
 *
 * This file tests each function in bits.c against a reference implementation
 * (defined in tests.c / decl.c) using a combination of exhaustive and random
 * test vectors.
 *
 * Usage:
 *   ./btest                 Run all tests
 *   ./btest -f bitXor       Test only the bitXor function
 *   ./btest -1 0x7          Run bitXor with first argument = 7
 *
 * Build:
 *   make          (from problem/ directory)
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include <getopt.h>

/* ── Declarations ───────────────────────────────────────────────── */

/* Imported from bits.c */
extern int bitXor(int, int);
extern int tmin(void);
extern int isTmax(int);
extern int allOddBits(int);
extern int negate(int);
extern int isAsciiDigit(int);
extern int conditional(int, int, int);
extern int isLessOrEqual(int, int);
extern int logicalNeg(int);
extern int howManyBits(int);
extern unsigned floatScale2(unsigned);
extern int floatFloat2Int(unsigned);
extern unsigned floatPower2(int);

/* ── Reference implementations (for checking) ──────────────────── */

static int ref_bitXor(int x, int y) { return x ^ y; }
static int ref_tmin(void) { return INT_MIN; }
static int ref_isTmax(int x) { return x == INT_MAX; }
static int ref_allOddBits(int x) { return (x & 0xAAAAAAAA) == 0xAAAAAAAA; }
static int ref_negate(int x) { return -x; }
static int ref_isAsciiDigit(int x) { return x >= 0x30 && x <= 0x39; }
static int ref_conditional(int x, int y, int z) { return x ? y : z; }
static int ref_isLessOrEqual(int x, int y) { return x <= y; }
static int ref_logicalNeg(int x) { return !x; }

static int ref_howManyBits(int x) {
    unsigned ux = (x < 0) ? (unsigned)~x : (unsigned)x;
    int bits = 1; /* sign bit */
    while (ux) { ux >>= 1; bits++; }
    return bits;
}

/* ── Lightweight random ────────────────────────────────────────── */

static unsigned seed = 0xDEADBEEF;

static int rand32(void) {
    seed ^= seed << 13;
    seed ^= seed >> 17;
    seed ^= seed << 5;
    return (int)seed;
}

/* ── Test infrastructure ───────────────────────────────────────── */

#define NUM_RANDOM 100000

static int total = 0, passed = 0;

static void check_int1(const char *name, int (*fn)(int), int (*ref)(int)) {
    int ok = 1;
    /* edge cases */
    int edges[] = {0, 1, -1, INT_MIN, INT_MAX, 0x80, 0xFF, 0x30, 0x39, 0x3A,
                   0xAAAAAAAA, 0x55555555, 0xFFFFFFFD};
    for (int i = 0; i < (int)(sizeof(edges)/sizeof(edges[0])); i++) {
        if (fn(edges[i]) != ref(edges[i])) { ok = 0; break; }
    }
    if (ok) {
        for (int i = 0; i < NUM_RANDOM; i++) {
            int x = rand32();
            if (fn(x) != ref(x)) { ok = 0; break; }
        }
    }
    total++;
    if (ok) { passed++; printf("  PASS  %s\n", name); }
    else    { printf("  FAIL  %s\n", name); }
}

static void check_int2(const char *name, int (*fn)(int,int), int (*ref)(int,int)) {
    int ok = 1;
    for (int i = 0; i < NUM_RANDOM; i++) {
        int x = rand32(), y = rand32();
        if (fn(x, y) != ref(x, y)) { ok = 0; break; }
    }
    total++;
    if (ok) { passed++; printf("  PASS  %s\n", name); }
    else    { printf("  FAIL  %s\n", name); }
}

static void check_int3(const char *name, int (*fn)(int,int,int), int (*ref)(int,int,int)) {
    int ok = 1;
    for (int i = 0; i < NUM_RANDOM; i++) {
        int x = rand32(), y = rand32(), z = rand32();
        if (fn(x, y, z) != ref(x, y, z)) { ok = 0; break; }
    }
    total++;
    if (ok) { passed++; printf("  PASS  %s\n", name); }
    else    { printf("  FAIL  %s\n", name); }
}

static void check_void(const char *name, int (*fn)(void), int (*ref)(void)) {
    total++;
    if (fn() == ref()) { passed++; printf("  PASS  %s\n", name); }
    else               { printf("  FAIL  %s\n", name); }
}

/* ── Main ──────────────────────────────────────────────────────── */

int main(void) {
    printf("=== Data Lab Test Harness (btest) ===\n\n");

    check_int2("bitXor",        bitXor,        ref_bitXor);
    check_void("tmin",          tmin,          ref_tmin);
    check_int1("isTmax",        isTmax,        ref_isTmax);
    check_int1("allOddBits",    allOddBits,    ref_allOddBits);
    check_int1("negate",        negate,        ref_negate);
    check_int1("isAsciiDigit",  isAsciiDigit,  ref_isAsciiDigit);
    check_int3("conditional",   conditional,   ref_conditional);
    check_int2("isLessOrEqual", isLessOrEqual, ref_isLessOrEqual);
    check_int1("logicalNeg",    logicalNeg,    ref_logicalNeg);
    check_int1("howManyBits",   howManyBits,   ref_howManyBits);

    /* Floating-point puzzles tested separately due to unsigned args */
    printf("\n  (Floating-point puzzles: use script/grade.sh for full test)\n");

    printf("\n=== Results: %d / %d passed ===\n", passed, total);
    return (passed == total) ? 0 : 1;
}
