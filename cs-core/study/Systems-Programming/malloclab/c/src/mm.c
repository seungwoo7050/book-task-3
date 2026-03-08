#include <stddef.h>
#include <stdint.h>
#include <string.h>

#include "memlib.h"
#include "mm.h"

#define ALIGNMENT 16
#define WORD_SIZE 8
#define DOUBLE_WORD 16
#define MIN_BLOCK_SIZE 32
#define DEFAULT_CHUNK_SIZE (1 << 12)

static char *heap_start = NULL;
static void *free_list_head = NULL;

static size_t align_size(size_t size)
{
    return (size + (ALIGNMENT - 1)) & ~(size_t)(ALIGNMENT - 1);
}

static size_t pack(size_t size, int allocated)
{
    return size | (size_t)allocated;
}

static size_t load_word(const void *address)
{
    return *(const size_t *)address;
}

static void store_word(void *address, size_t value)
{
    *(size_t *)address = value;
}

static size_t block_size(const void *header)
{
    return load_word(header) & ~(size_t)0xf;
}

static int is_allocated(const void *header)
{
    return (int)(load_word(header) & (size_t)0x1);
}

static void *header_of(void *block)
{
    return (char *)block - WORD_SIZE;
}

static void *footer_of(void *block)
{
    return (char *)block + block_size(header_of(block)) - DOUBLE_WORD;
}

static void *next_block(void *block)
{
    return (char *)block + block_size(header_of(block));
}

static void *previous_block(void *block)
{
    return (char *)block - block_size((char *)block - DOUBLE_WORD);
}

static void **next_free_slot(void *block)
{
    return (void **)block;
}

static void **prev_free_slot(void *block)
{
    return (void **)((char *)block + WORD_SIZE);
}

static void add_to_free_list(void *block)
{
    *next_free_slot(block) = free_list_head;
    *prev_free_slot(block) = NULL;

    if (free_list_head != NULL) {
        *prev_free_slot(free_list_head) = block;
    }
    free_list_head = block;
}

static void remove_from_free_list(void *block)
{
    void *prev = *prev_free_slot(block);
    void *next = *next_free_slot(block);

    if (prev != NULL) {
        *next_free_slot(prev) = next;
    } else {
        free_list_head = next;
    }

    if (next != NULL) {
        *prev_free_slot(next) = prev;
    }
}

static void *coalesce(void *block)
{
    int prev_alloc = is_allocated(footer_of(previous_block(block)));
    int next_alloc = is_allocated(header_of(next_block(block)));
    size_t size = block_size(header_of(block));

    if (prev_alloc && next_alloc) {
        store_word(header_of(block), pack(size, 0));
        store_word(footer_of(block), pack(size, 0));
    } else if (prev_alloc && !next_alloc) {
        void *next = next_block(block);
        size += block_size(header_of(next));
        remove_from_free_list(next);
        store_word(header_of(block), pack(size, 0));
        store_word(footer_of(block), pack(size, 0));
    } else if (!prev_alloc && next_alloc) {
        void *prev = previous_block(block);
        size += block_size(header_of(prev));
        remove_from_free_list(prev);
        store_word(header_of(prev), pack(size, 0));
        store_word(footer_of(block), pack(size, 0));
        block = prev;
    } else {
        void *prev = previous_block(block);
        void *next = next_block(block);
        size += block_size(header_of(prev)) + block_size(header_of(next));
        remove_from_free_list(prev);
        remove_from_free_list(next);
        store_word(header_of(prev), pack(size, 0));
        store_word(footer_of(next), pack(size, 0));
        block = prev;
    }

    add_to_free_list(block);
    return block;
}

static void *extend_heap(size_t bytes)
{
    size_t size = align_size(bytes);
    char *block;

    if (size < MIN_BLOCK_SIZE) {
        size = MIN_BLOCK_SIZE;
    }

    block = (char *)mem_sbrk((int)size);
    if (block == (void *)-1) {
        return NULL;
    }

    store_word(block - WORD_SIZE, pack(size, 0));
    store_word(block + size - DOUBLE_WORD, pack(size, 0));
    store_word(block + size - WORD_SIZE, pack(0, 1));
    return coalesce(block);
}

static void place_block(void *block, size_t size)
{
    size_t current_size = block_size(header_of(block));
    size_t remainder = current_size - size;

    remove_from_free_list(block);

    if (remainder >= MIN_BLOCK_SIZE) {
        void *split = (char *)block + size;
        store_word(header_of(block), pack(size, 1));
        store_word(footer_of(block), pack(size, 1));

        store_word(header_of(split), pack(remainder, 0));
        store_word(footer_of(split), pack(remainder, 0));
        add_to_free_list(split);
    } else {
        store_word(header_of(block), pack(current_size, 1));
        store_word(footer_of(block), pack(current_size, 1));
    }
}

static void *find_fit(size_t size)
{
    void *block;

    for (block = free_list_head; block != NULL; block = *next_free_slot(block)) {
        if (block_size(header_of(block)) >= size) {
            return block;
        }
    }
    return NULL;
}

int mm_init(void)
{
    heap_start = (char *)mem_sbrk(4 * WORD_SIZE);
    if (heap_start == (void *)-1) {
        return -1;
    }

    store_word(heap_start, 0);
    store_word(heap_start + WORD_SIZE, pack(DOUBLE_WORD, 1));
    store_word(heap_start + 2 * WORD_SIZE, pack(DOUBLE_WORD, 1));
    store_word(heap_start + 3 * WORD_SIZE, pack(0, 1));
    heap_start += 2 * WORD_SIZE;
    free_list_head = NULL;

    return extend_heap(DEFAULT_CHUNK_SIZE) == NULL ? -1 : 0;
}

void *mm_malloc(size_t size)
{
    size_t adjusted;
    size_t grow_by;
    void *block;

    if (size == 0) {
        return NULL;
    }

    adjusted = align_size(size + DOUBLE_WORD);
    if (adjusted < MIN_BLOCK_SIZE) {
        adjusted = MIN_BLOCK_SIZE;
    }

    block = find_fit(adjusted);
    if (block == NULL) {
        grow_by = adjusted > DEFAULT_CHUNK_SIZE ? adjusted : DEFAULT_CHUNK_SIZE;
        block = extend_heap(grow_by);
        if (block == NULL) {
            return NULL;
        }
    }

    place_block(block, adjusted);
    return block;
}

void mm_free(void *ptr)
{
    size_t size;

    if (ptr == NULL) {
        return;
    }

    size = block_size(header_of(ptr));
    store_word(header_of(ptr), pack(size, 0));
    store_word(footer_of(ptr), pack(size, 0));
    coalesce(ptr);
}

void *mm_realloc(void *ptr, size_t size)
{
    size_t adjusted;
    size_t current_size;
    size_t copy_size;
    void *next;
    void *new_ptr;

    if (ptr == NULL) {
        return mm_malloc(size);
    }
    if (size == 0) {
        mm_free(ptr);
        return NULL;
    }

    adjusted = align_size(size + DOUBLE_WORD);
    if (adjusted < MIN_BLOCK_SIZE) {
        adjusted = MIN_BLOCK_SIZE;
    }

    current_size = block_size(header_of(ptr));
    if (current_size >= adjusted) {
        size_t remainder = current_size - adjusted;
        if (remainder >= MIN_BLOCK_SIZE) {
            void *split = (char *)ptr + adjusted;
            store_word(header_of(ptr), pack(adjusted, 1));
            store_word(footer_of(ptr), pack(adjusted, 1));
            store_word(header_of(split), pack(remainder, 0));
            store_word(footer_of(split), pack(remainder, 0));
            coalesce(split);
        }
        return ptr;
    }

    next = next_block(ptr);
    if (!is_allocated(header_of(next)) &&
        current_size + block_size(header_of(next)) >= adjusted) {
        size_t merged = current_size + block_size(header_of(next));
        size_t remainder;

        remove_from_free_list(next);
        store_word(header_of(ptr), pack(merged, 1));
        store_word(footer_of(ptr), pack(merged, 1));

        remainder = merged - adjusted;
        if (remainder >= MIN_BLOCK_SIZE) {
            void *split = (char *)ptr + adjusted;
            store_word(header_of(ptr), pack(adjusted, 1));
            store_word(footer_of(ptr), pack(adjusted, 1));
            store_word(header_of(split), pack(remainder, 0));
            store_word(footer_of(split), pack(remainder, 0));
            add_to_free_list(split);
        }
        return ptr;
    }

    new_ptr = mm_malloc(size);
    if (new_ptr == NULL) {
        return NULL;
    }

    copy_size = current_size - DOUBLE_WORD;
    if (copy_size > size) {
        copy_size = size;
    }
    memcpy(new_ptr, ptr, copy_size);
    mm_free(ptr);
    return new_ptr;
}
