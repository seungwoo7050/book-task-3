#include "mini_attacklab.h"

#include <ctype.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum {
    BUFFER_SIZE = 40
};

static const uint64_t TOUCH1 = 0x4017c0ULL;
static const uint64_t TOUCH2 = 0x4017ecULL;
static const uint64_t TOUCH3 = 0x4018faULL;
static const uint64_t BUFFER_START = 0x5561dc78ULL;
static const uint64_t PHASE3_STRING_ADDR = 0x5561dca8ULL;
static const uint64_t GADGET_POP_RAX = 0x4019ccULL;
static const uint64_t GADGET_MOV_RAX_RDI = 0x4019a2ULL;
static const uint64_t GADGET_MOV_RSP_RAX = 0x4019d0ULL;
static const uint64_t GADGET_POP_RSI = 0x401a10ULL;
static const uint64_t GADGET_LEA_RDI_RSI_RAX = 0x401a20ULL;
static const uint64_t COOKIE = 0x1a2b3c4dULL;
static const unsigned char COOKIE_ASCII[] = {'1', 'a', '2', 'b', '3', 'c', '4', 'd', '\0'};

static int hex_value(int ch)
{
    if ('0' <= ch && ch <= '9') {
        return ch - '0';
    }
    if ('a' <= ch && ch <= 'f') {
        return ch - 'a' + 10;
    }
    if ('A' <= ch && ch <= 'F') {
        return ch - 'A' + 10;
    }
    return -1;
}

static uint64_t read_u64_le(const unsigned char *bytes)
{
    uint64_t value = 0;
    int index;

    for (index = 7; index >= 0; --index) {
        value = (value << 8) | bytes[index];
    }
    return value;
}

static int matches_u64_le(const unsigned char *bytes, uint64_t expected)
{
    return read_u64_le(bytes) == expected;
}

int parse_hex_string(const char *text, unsigned char *buffer, size_t capacity, size_t *out_len)
{
    size_t index = 0;

    while (*text != '\0') {
        while (isspace((unsigned char)*text)) {
            ++text;
        }
        if (*text == '#') {
            while (*text != '\0' && *text != '\n') {
                ++text;
            }
            continue;
        }
        if (*text == '\0') {
            break;
        }
        if (text[0] == '\0' || text[1] == '\0') {
            return 0;
        }
        if (index >= capacity) {
            return 0;
        }

        {
            int high = hex_value(text[0]);
            int low = hex_value(text[1]);

            if (high < 0 || low < 0) {
                return 0;
            }
            buffer[index++] = (unsigned char)((high << 4) | low);
        }
        text += 2;

        if (*text != '\0' && !isspace((unsigned char)*text) && *text != '#') {
            return 0;
        }
    }

    *out_len = index;
    return 1;
}

int load_hex_file(const char *path, unsigned char *buffer, size_t capacity, size_t *out_len)
{
    FILE *file = fopen(path, "rb");
    long size;
    char *text;
    int ok;

    if (file == NULL) {
        return 0;
    }
    if (fseek(file, 0, SEEK_END) != 0) {
        fclose(file);
        return 0;
    }
    size = ftell(file);
    if (size < 0 || fseek(file, 0, SEEK_SET) != 0) {
        fclose(file);
        return 0;
    }

    text = (char *)malloc((size_t)size + 1);
    if (text == NULL) {
        fclose(file);
        return 0;
    }
    if (fread(text, 1, (size_t)size, file) != (size_t)size) {
        free(text);
        fclose(file);
        return 0;
    }
    text[size] = '\0';
    fclose(file);

    ok = parse_hex_string(text, buffer, capacity, out_len);
    free(text);
    return ok;
}

int attacklab_phase_1(const unsigned char *bytes, size_t len)
{
    return len == 48 && matches_u64_le(bytes + BUFFER_SIZE, TOUCH1);
}

int attacklab_phase_2(const unsigned char *bytes, size_t len)
{
    static const unsigned char prefix[] = {
        0x48, 0xc7, 0xc7, 0x4d, 0x3c, 0x2b, 0x1a,
        0x68, 0xec, 0x17, 0x40, 0x00, 0xc3
    };

    return len == 48 &&
           memcmp(bytes, prefix, sizeof(prefix)) == 0 &&
           matches_u64_le(bytes + BUFFER_SIZE, BUFFER_START);
}

int attacklab_phase_3(const unsigned char *bytes, size_t len)
{
    static const unsigned char prefix[] = {
        0x48, 0xc7, 0xc7, 0xa8, 0xdc, 0x61, 0x55,
        0x68, 0xfa, 0x18, 0x40, 0x00, 0xc3
    };

    return len == 57 &&
           memcmp(bytes, prefix, sizeof(prefix)) == 0 &&
           matches_u64_le(bytes + BUFFER_SIZE, BUFFER_START) &&
           memcmp(bytes + 48, COOKIE_ASCII, sizeof(COOKIE_ASCII)) == 0 &&
           PHASE3_STRING_ADDR == BUFFER_START + 48;
}

int attacklab_phase_4(const unsigned char *bytes, size_t len)
{
    return len == 72 &&
           matches_u64_le(bytes + 40, GADGET_POP_RAX) &&
           matches_u64_le(bytes + 48, COOKIE) &&
           matches_u64_le(bytes + 56, GADGET_MOV_RAX_RDI) &&
           matches_u64_le(bytes + 64, TOUCH2);
}

int attacklab_phase_5(const unsigned char *bytes, size_t len)
{
    return len == 105 &&
           matches_u64_le(bytes + 40, GADGET_MOV_RSP_RAX) &&
           matches_u64_le(bytes + 48, GADGET_MOV_RAX_RDI) &&
           matches_u64_le(bytes + 56, GADGET_POP_RSI) &&
           matches_u64_le(bytes + 64, 48ULL) &&
           matches_u64_le(bytes + 72, GADGET_LEA_RDI_RSI_RAX) &&
           matches_u64_le(bytes + 80, GADGET_MOV_RAX_RDI) &&
           matches_u64_le(bytes + 88, TOUCH3) &&
           memcmp(bytes + 96, COOKIE_ASCII, sizeof(COOKIE_ASCII)) == 0;
}

int attacklab_validate_phase(int phase, const unsigned char *bytes, size_t len)
{
    switch (phase) {
    case 1:
        return attacklab_phase_1(bytes, len);
    case 2:
        return attacklab_phase_2(bytes, len);
    case 3:
        return attacklab_phase_3(bytes, len);
    case 4:
        return attacklab_phase_4(bytes, len);
    case 5:
        return attacklab_phase_5(bytes, len);
    default:
        return 0;
    }
}

const char *attacklab_phase_name(int phase)
{
    switch (phase) {
    case 1:
        return "return-address overwrite";
    case 2:
        return "code injection with cookie register setup";
    case 3:
        return "code injection with cookie string placement";
    case 4:
        return "ROP chain for touch2";
    case 5:
        return "ROP chain for touch3 with relative string addressing";
    default:
        return "unknown";
    }
}
