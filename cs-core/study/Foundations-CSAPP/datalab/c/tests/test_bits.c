/*
 * test_bits.c - Data Lab 풀이를 위한 경계값 테스트.
 *
 * 빌드와 실행:
 *   gcc -O1 -Wall -Werror -o test_bits test_bits.c ../src/bits.c && ./test_bits
 *
 * 공식 btest가 놓치기 쉬운 경계 사례를 따로 확인한다.
 */

#include <stdio.h>
#include <limits.h>

/* bits.c에서 가져오는 함수 */
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

#define TEST(name, expr) do { \
    if (!(expr)) { printf("FAIL: %s — %s\n", name, #expr); fails++; } \
    else { passes++; } \
} while (0)

int main(void) {
    int passes = 0, fails = 0;

    /* ── bitXor ───────────────────────────────────────────────── */
    TEST("bitXor(4,5)",    bitXor(4, 5) == 1);
    TEST("bitXor(0,0)",    bitXor(0, 0) == 0);
    TEST("bitXor(-1,0)",   bitXor(-1, 0) == -1);
    TEST("bitXor(-1,-1)",  bitXor(-1, -1) == 0);

    /* ── tmin ─────────────────────────────────────────────────── */
    TEST("tmin", tmin() == INT_MIN);

    /* ── isTmax ───────────────────────────────────────────────── */
    TEST("isTmax(TMax)",   isTmax(INT_MAX) == 1);
    TEST("isTmax(-1)",     isTmax(-1) == 0);
    TEST("isTmax(0)",      isTmax(0) == 0);
    TEST("isTmax(TMin)",   isTmax(INT_MIN) == 0);

    /* ── allOddBits ───────────────────────────────────────────── */
    TEST("allOddBits(0xAAAAAAAA)", allOddBits(0xAAAAAAAA) == 1);
    TEST("allOddBits(0xFFFFFFFD)", allOddBits(0xFFFFFFFD) == 0);
    TEST("allOddBits(0xFFFFFFFF)", allOddBits(0xFFFFFFFF) == 1);
    TEST("allOddBits(0)",          allOddBits(0) == 0);

    /* ── negate ───────────────────────────────────────────────── */
    TEST("negate(1)",    negate(1) == -1);
    TEST("negate(-1)",   negate(-1) == 1);
    TEST("negate(0)",    negate(0) == 0);
    TEST("negate(TMin)", negate(INT_MIN) == INT_MIN);  /* 오버플로우 */

    /* ── isAsciiDigit ─────────────────────────────────────────── */
    TEST("isAsciiDigit(0x30)", isAsciiDigit(0x30) == 1);
    TEST("isAsciiDigit(0x39)", isAsciiDigit(0x39) == 1);
    TEST("isAsciiDigit(0x3A)", isAsciiDigit(0x3A) == 0);
    TEST("isAsciiDigit(0x2F)", isAsciiDigit(0x2F) == 0);
    TEST("isAsciiDigit(-1)",   isAsciiDigit(-1) == 0);

    /* ── conditional ──────────────────────────────────────────── */
    TEST("conditional(2,4,5)",  conditional(2, 4, 5) == 4);
    TEST("conditional(0,4,5)",  conditional(0, 4, 5) == 5);
    TEST("conditional(-1,4,5)", conditional(-1, 4, 5) == 4);

    /* ── isLessOrEqual ────────────────────────────────────────── */
    TEST("isLessOrEqual(4,5)",       isLessOrEqual(4, 5) == 1);
    TEST("isLessOrEqual(5,4)",       isLessOrEqual(5, 4) == 0);
    TEST("isLessOrEqual(5,5)",       isLessOrEqual(5, 5) == 1);
    TEST("isLessOrEqual(TMin,TMax)", isLessOrEqual(INT_MIN, INT_MAX) == 1);
    TEST("isLessOrEqual(TMax,TMin)", isLessOrEqual(INT_MAX, INT_MIN) == 0);

    /* ── logicalNeg ───────────────────────────────────────────── */
    TEST("logicalNeg(0)",    logicalNeg(0) == 1);
    TEST("logicalNeg(1)",    logicalNeg(1) == 0);
    TEST("logicalNeg(-1)",   logicalNeg(-1) == 0);
    TEST("logicalNeg(TMin)", logicalNeg(INT_MIN) == 0);

    /* ── howManyBits ──────────────────────────────────────────── */
    TEST("howManyBits(0)",    howManyBits(0) == 1);
    TEST("howManyBits(-1)",   howManyBits(-1) == 1);
    TEST("howManyBits(1)",    howManyBits(1) == 2);
    TEST("howManyBits(12)",   howManyBits(12) == 5);
    TEST("howManyBits(298)",  howManyBits(298) == 10);
    TEST("howManyBits(TMax)", howManyBits(INT_MAX) == 32);
    TEST("howManyBits(TMin)", howManyBits(INT_MIN) == 32);

    /* ── floatScale2 ──────────────────────────────────────────── */
    TEST("floatScale2(0)",        floatScale2(0x00000000u) == 0x00000000u);
    TEST("floatScale2(denorm)",   floatScale2(0x00000001u) == 0x00000002u);
    TEST("floatScale2(1.0)",      floatScale2(0x3F800000u) == 0x40000000u);
    TEST("floatScale2(+inf)",     floatScale2(0x7F800000u) == 0x7F800000u);
    TEST("floatScale2(NaN)",      floatScale2(0x7FC00000u) == 0x7FC00000u);

    /* ── floatFloat2Int ──────────────────────────────────────── */
    TEST("floatFloat2Int(1.0)",   floatFloat2Int(0x3F800000u) == 1);
    TEST("floatFloat2Int(-2.0)",  floatFloat2Int(0xC0000000u) == -2);
    TEST("floatFloat2Int(0.5)",   floatFloat2Int(0x3F000000u) == 0);
    TEST("floatFloat2Int(+inf)",  floatFloat2Int(0x7F800000u) == (int)0x80000000u);
    TEST("floatFloat2Int(NaN)",   floatFloat2Int(0x7FC00000u) == (int)0x80000000u);

    /* ── floatPower2 ──────────────────────────────────────────── */
    TEST("floatPower2(0)",   floatPower2(0) == 0x3F800000);   /* 1.0 */
    TEST("floatPower2(1)",   floatPower2(1) == 0x40000000);   /* 2.0 */
    TEST("floatPower2(128)", floatPower2(128) == 0x7F800000); /* 양의 무한대 */
    TEST("floatPower2(-150)",floatPower2(-150) == 0);          /* 표현 불가 */

    /* ── 요약 ─────────────────────────────────────────────────── */
    printf("\n=== %d / %d edge-case tests passed ===\n", passes, passes + fails);
    return fails ? 1 : 0;
}
