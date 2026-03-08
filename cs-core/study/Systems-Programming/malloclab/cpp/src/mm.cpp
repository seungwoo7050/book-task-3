#include <cstddef>
#include <cstdint>
#include <cstring>

#include "memlib.h"
#include "mm.h"

namespace {

constexpr std::size_t kAlignment = 16;
constexpr std::size_t kWordSize = 8;
constexpr std::size_t kDoubleWord = 16;
constexpr std::size_t kMinBlockSize = 32;
constexpr std::size_t kChunkSize = 1 << 12;

char *g_heap_start = nullptr;
void *g_free_list_head = nullptr;

std::size_t align_size(std::size_t size)
{
    return (size + (kAlignment - 1)) & ~(kAlignment - 1);
}

std::size_t pack(std::size_t size, bool allocated)
{
    return size | static_cast<std::size_t>(allocated);
}

std::size_t load_word(const void *address)
{
    return *reinterpret_cast<const std::size_t *>(address);
}

void store_word(void *address, std::size_t value)
{
    *reinterpret_cast<std::size_t *>(address) = value;
}

std::size_t block_size(const void *header)
{
    return load_word(header) & ~static_cast<std::size_t>(0xf);
}

bool is_allocated(const void *header)
{
    return (load_word(header) & static_cast<std::size_t>(0x1)) != 0;
}

void *header_of(void *block)
{
    return static_cast<char *>(block) - kWordSize;
}

void *footer_of(void *block)
{
    return static_cast<char *>(block) + block_size(header_of(block)) - kDoubleWord;
}

void *next_block(void *block)
{
    return static_cast<char *>(block) + block_size(header_of(block));
}

void *previous_block(void *block)
{
    return static_cast<char *>(block) - block_size(static_cast<char *>(block) - kDoubleWord);
}

void **next_free_slot(void *block)
{
    return reinterpret_cast<void **>(block);
}

void **prev_free_slot(void *block)
{
    return reinterpret_cast<void **>(static_cast<char *>(block) + kWordSize);
}

void add_to_free_list(void *block)
{
    *next_free_slot(block) = g_free_list_head;
    *prev_free_slot(block) = nullptr;
    if (g_free_list_head != nullptr) {
        *prev_free_slot(g_free_list_head) = block;
    }
    g_free_list_head = block;
}

void remove_from_free_list(void *block)
{
    void *prev = *prev_free_slot(block);
    void *next = *next_free_slot(block);

    if (prev != nullptr) {
        *next_free_slot(prev) = next;
    } else {
        g_free_list_head = next;
    }

    if (next != nullptr) {
        *prev_free_slot(next) = prev;
    }
}

void *coalesce(void *block)
{
    const bool prev_alloc = is_allocated(footer_of(previous_block(block)));
    const bool next_alloc = is_allocated(header_of(next_block(block)));
    std::size_t size = block_size(header_of(block));

    if (prev_alloc && next_alloc) {
        store_word(header_of(block), pack(size, false));
        store_word(footer_of(block), pack(size, false));
    } else if (prev_alloc && !next_alloc) {
        void *next = next_block(block);
        size += block_size(header_of(next));
        remove_from_free_list(next);
        store_word(header_of(block), pack(size, false));
        store_word(footer_of(block), pack(size, false));
    } else if (!prev_alloc && next_alloc) {
        void *prev = previous_block(block);
        size += block_size(header_of(prev));
        remove_from_free_list(prev);
        store_word(header_of(prev), pack(size, false));
        store_word(footer_of(block), pack(size, false));
        block = prev;
    } else {
        void *prev = previous_block(block);
        void *next = next_block(block);
        size += block_size(header_of(prev)) + block_size(header_of(next));
        remove_from_free_list(prev);
        remove_from_free_list(next);
        store_word(header_of(prev), pack(size, false));
        store_word(footer_of(next), pack(size, false));
        block = prev;
    }

    add_to_free_list(block);
    return block;
}

void *extend_heap(std::size_t bytes)
{
    std::size_t size = align_size(bytes);
    char *block;

    if (size < kMinBlockSize) {
        size = kMinBlockSize;
    }

    block = static_cast<char *>(mem_sbrk(static_cast<int>(size)));
    if (block == reinterpret_cast<void *>(-1)) {
        return nullptr;
    }

    store_word(block - kWordSize, pack(size, false));
    store_word(block + size - kDoubleWord, pack(size, false));
    store_word(block + size - kWordSize, pack(0, true));
    return coalesce(block);
}

void place_block(void *block, std::size_t wanted)
{
    const std::size_t current = block_size(header_of(block));
    const std::size_t remainder = current - wanted;

    remove_from_free_list(block);

    if (remainder >= kMinBlockSize) {
        void *split = static_cast<char *>(block) + wanted;
        store_word(header_of(block), pack(wanted, true));
        store_word(footer_of(block), pack(wanted, true));
        store_word(header_of(split), pack(remainder, false));
        store_word(footer_of(split), pack(remainder, false));
        add_to_free_list(split);
    } else {
        store_word(header_of(block), pack(current, true));
        store_word(footer_of(block), pack(current, true));
    }
}

void *find_fit(std::size_t wanted)
{
    void *block = g_free_list_head;
    while (block != nullptr) {
        if (block_size(header_of(block)) >= wanted) {
            return block;
        }
        block = *next_free_slot(block);
    }
    return nullptr;
}

}  // namespace

extern "C" int mm_init(void)
{
    g_heap_start = static_cast<char *>(mem_sbrk(4 * kWordSize));
    if (g_heap_start == reinterpret_cast<void *>(-1)) {
        return -1;
    }

    store_word(g_heap_start, 0);
    store_word(g_heap_start + kWordSize, pack(kDoubleWord, true));
    store_word(g_heap_start + 2 * kWordSize, pack(kDoubleWord, true));
    store_word(g_heap_start + 3 * kWordSize, pack(0, true));
    g_heap_start += 2 * kWordSize;
    g_free_list_head = nullptr;

    return extend_heap(kChunkSize) == nullptr ? -1 : 0;
}

extern "C" void *mm_malloc(std::size_t size)
{
    std::size_t adjusted;
    std::size_t grow_by;
    void *block;

    if (size == 0) {
        return nullptr;
    }

    adjusted = align_size(size + kDoubleWord);
    if (adjusted < kMinBlockSize) {
        adjusted = kMinBlockSize;
    }

    block = find_fit(adjusted);
    if (block == nullptr) {
        grow_by = adjusted > kChunkSize ? adjusted : kChunkSize;
        block = extend_heap(grow_by);
        if (block == nullptr) {
            return nullptr;
        }
    }

    place_block(block, adjusted);
    return block;
}

extern "C" void mm_free(void *ptr)
{
    std::size_t size;

    if (ptr == nullptr) {
        return;
    }

    size = block_size(header_of(ptr));
    store_word(header_of(ptr), pack(size, false));
    store_word(footer_of(ptr), pack(size, false));
    coalesce(ptr);
}

extern "C" void *mm_realloc(void *ptr, std::size_t size)
{
    std::size_t adjusted;
    std::size_t current_size;
    std::size_t copy_size;
    void *next;
    void *new_ptr;

    if (ptr == nullptr) {
        return mm_malloc(size);
    }
    if (size == 0) {
        mm_free(ptr);
        return nullptr;
    }

    adjusted = align_size(size + kDoubleWord);
    if (adjusted < kMinBlockSize) {
        adjusted = kMinBlockSize;
    }

    current_size = block_size(header_of(ptr));
    if (current_size >= adjusted) {
        const std::size_t remainder = current_size - adjusted;
        if (remainder >= kMinBlockSize) {
            void *split = static_cast<char *>(ptr) + adjusted;
            store_word(header_of(ptr), pack(adjusted, true));
            store_word(footer_of(ptr), pack(adjusted, true));
            store_word(header_of(split), pack(remainder, false));
            store_word(footer_of(split), pack(remainder, false));
            coalesce(split);
        }
        return ptr;
    }

    next = next_block(ptr);
    if (!is_allocated(header_of(next)) &&
        current_size + block_size(header_of(next)) >= adjusted) {
        const std::size_t merged = current_size + block_size(header_of(next));
        const std::size_t remainder = merged - adjusted;

        remove_from_free_list(next);
        store_word(header_of(ptr), pack(merged, true));
        store_word(footer_of(ptr), pack(merged, true));

        if (remainder >= kMinBlockSize) {
            void *split = static_cast<char *>(ptr) + adjusted;
            store_word(header_of(ptr), pack(adjusted, true));
            store_word(footer_of(ptr), pack(adjusted, true));
            store_word(header_of(split), pack(remainder, false));
            store_word(footer_of(split), pack(remainder, false));
            add_to_free_list(split);
        }
        return ptr;
    }

    new_ptr = mm_malloc(size);
    if (new_ptr == nullptr) {
        return nullptr;
    }

    copy_size = current_size - kDoubleWord;
    if (copy_size > size) {
        copy_size = size;
    }
    std::memcpy(new_ptr, ptr, copy_size);
    mm_free(ptr);
    return new_ptr;
}
