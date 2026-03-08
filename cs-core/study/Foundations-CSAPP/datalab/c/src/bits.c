/*
 * bits.c — Fresh C solutions for the migrated Data Lab project.
 *
 * Integer puzzles keep the original bit-manipulation contract.
 * Floating-point puzzles work on unsigned bit patterns only.
 */

int bitXor(int x, int y) {
    return ~(~(x & ~y) & ~(~x & y));
}

int tmin(void) {
    return 1 << 31;
}

int isTmax(int x) {
    int y = x + 1;
    return !(~(x + y)) & !!y;
}

int allOddBits(int x) {
    int mask = (0xAA << 8) | 0xAA;
    mask = (mask << 16) | mask;
    return !((x & mask) ^ mask);
}

int negate(int x) {
    return ~x + 1;
}

int isAsciiDigit(int x) {
    int lower = x + (~0x30 + 1);
    int upper = 0x39 + (~x + 1);
    return !((lower >> 31) | (upper >> 31));
}

int conditional(int x, int y, int z) {
    int mask = (!!x << 31) >> 31;
    return (mask & y) | (~mask & z);
}

int isLessOrEqual(int x, int y) {
    int sx = x >> 31;
    int sy = y >> 31;
    int diff_sign = sx ^ sy;
    int diff = y + (~x + 1);
    int diff_nonneg = !(diff >> 31);
    return (diff_sign & !!sx) | ((!diff_sign) & diff_nonneg);
}

int logicalNeg(int x) {
    return ((x | (~x + 1)) >> 31) + 1;
}

int howManyBits(int x) {
    int sign = x >> 31;
    int b16;
    int b8;
    int b4;
    int b2;
    int b1;
    int b0;

    x = x ^ sign;

    b16 = !!(x >> 16) << 4;
    x >>= b16;
    b8 = !!(x >> 8) << 3;
    x >>= b8;
    b4 = !!(x >> 4) << 2;
    x >>= b4;
    b2 = !!(x >> 2) << 1;
    x >>= b2;
    b1 = !!(x >> 1);
    x >>= b1;
    b0 = x >> 0;

    return b16 + b8 + b4 + b2 + b1 + b0 + 1;
}

unsigned floatScale2(unsigned uf) {
    unsigned sign = uf & 0x80000000u;
    unsigned exp = (uf >> 23) & 0xFFu;
    unsigned frac = uf & 0x7FFFFFu;

    if (exp == 0xFFu) {
        return uf;
    }
    if (exp == 0u) {
        return sign | (frac << 1);
    }
    exp += 1u;
    if (exp == 0xFFu) {
        return sign | (0xFFu << 23);
    }
    return sign | (exp << 23) | frac;
}

int floatFloat2Int(unsigned uf) {
    int sign = uf >> 31;
    int exp = ((uf >> 23) & 0xFF) + (~127 + 1);
    int frac = (uf & 0x7FFFFF) | 0x800000;

    if (((uf >> 23) & 0xFF) == 0xFF) {
        return 0x80000000u;
    }
    if (exp < 0) {
        return 0;
    }
    if (exp > 30) {
        return 0x80000000u;
    }
    if (exp > 23) {
        frac = frac << (exp + (~23 + 1));
    } else {
        frac = frac >> (23 + (~exp + 1));
    }
    return sign ? (~frac + 1) : frac;
}

unsigned floatPower2(int x) {
    if (x < -149) {
        return 0u;
    }
    if (x < -126) {
        return 1 << (x + 149);
    }
    if (x > 127) {
        return 0x7F800000u;
    }
    return (x + 127) << 23;
}
