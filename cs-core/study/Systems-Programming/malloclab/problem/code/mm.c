/*
 * Starter allocator.
 *
 * This file exists only to define the problem contract and compile.
 * The completed implementations live in ../c and ../cpp.
 */

#include <stddef.h>

#include "memlib.h"
#include "mm.h"

int mm_init(void)
{
    /* TODO: initialize your heap layout and free-list metadata. */
    return 0;
}

void *mm_malloc(size_t size)
{
    (void)size;
    /* TODO: find or create a suitably aligned block. */
    return NULL;
}

void mm_free(void *ptr)
{
    (void)ptr;
    /* TODO: mark the block free and coalesce with neighbours. */
}

void *mm_realloc(void *ptr, size_t size)
{
    (void)ptr;
    (void)size;
    /* TODO: preserve the old payload prefix when the block must move. */
    return NULL;
}
