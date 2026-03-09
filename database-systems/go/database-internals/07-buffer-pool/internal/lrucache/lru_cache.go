package lrucache

type node struct {
	key   string
	value any
	prev  *node
	next  *node
}

type LRUCache struct {
	capacity int
	size     int
	items    map[string]*node
	head     *node
	tail     *node
}

func New(capacity int) *LRUCache {
	head := &node{}
	tail := &node{}
	head.next = tail
	tail.prev = head
	return &LRUCache{
		capacity: capacity,
		items:    map[string]*node{},
		head:     head,
		tail:     tail,
	}
}

func (cache *LRUCache) Get(key string) any {
	item := cache.items[key]
	if item == nil {
		return nil
	}
	cache.moveToFront(item)
	return item.value
}

func (cache *LRUCache) Put(key string, value any) *Entry {
	if existing := cache.items[key]; existing != nil {
		existing.value = value
		cache.moveToFront(existing)
		return nil
	}

	var evicted *Entry
	if cache.size >= cache.capacity {
		lru := cache.tail.prev
		if lru != cache.head {
			evicted = &Entry{Key: lru.key, Value: lru.value}
			cache.remove(lru)
			delete(cache.items, lru.key)
			cache.size--
		}
	}

	item := &node{key: key, value: value}
	cache.addToFront(item)
	cache.items[key] = item
	cache.size++
	return evicted
}

func (cache *LRUCache) Delete(key string) bool {
	item := cache.items[key]
	if item == nil {
		return false
	}
	cache.remove(item)
	delete(cache.items, key)
	cache.size--
	return true
}

func (cache *LRUCache) Has(key string) bool {
	_, ok := cache.items[key]
	return ok
}

func (cache *LRUCache) Keys() []string {
	keys := []string{}
	current := cache.head.next
	for current != nil && current != cache.tail {
		keys = append(keys, current.key)
		current = current.next
	}
	return keys
}

func (cache *LRUCache) Size() int {
	return cache.size
}

type Entry struct {
	Key   string
	Value any
}

func (cache *LRUCache) remove(item *node) {
	item.prev.next = item.next
	item.next.prev = item.prev
	item.prev = nil
	item.next = nil
}

func (cache *LRUCache) addToFront(item *node) {
	item.next = cache.head.next
	item.prev = cache.head
	cache.head.next.prev = item
	cache.head.next = item
}

func (cache *LRUCache) moveToFront(item *node) {
	cache.remove(item)
	cache.addToFront(item)
}
