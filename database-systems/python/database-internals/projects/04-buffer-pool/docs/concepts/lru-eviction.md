# LRU Eviction

- doubly-linked list와 hash map을 조합하면 O(1) get/put/evict가 가능하다.
- head 근처가 MRU, tail 근처가 LRU다.
- buffer pool은 eviction 대상을 고를 때 page metadata를 함께 고려해야 한다.

