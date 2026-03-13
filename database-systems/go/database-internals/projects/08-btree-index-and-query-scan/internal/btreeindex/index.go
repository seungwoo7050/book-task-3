package btreeindex

import "sort"

type Entry struct {
	Key    string
	RowIDs []int
}

type RangeCursor struct {
	leaf       *node
	entryIndex int
	end        string
}

type node struct {
	leaf     bool
	keys     []string
	children []*node
	entries  []Entry
	next     *node
}

type splitResult struct {
	promotedKey string
	right       *node
}

type BTreeIndex struct {
	order     int
	root      *node
	firstLeaf *node
}

func New(order int) *BTreeIndex {
	if order < 3 {
		order = 4
	}
	root := &node{leaf: true}
	return &BTreeIndex{
		order:     order,
		root:      root,
		firstLeaf: root,
	}
}

func (tree *BTreeIndex) Insert(key string, rowID int) {
	if key == "" {
		return
	}
	if result := tree.insert(tree.root, key, rowID); result != nil {
		tree.root = &node{
			keys:     []string{result.promotedKey},
			children: []*node{tree.root, result.right},
		}
	}
}

func (tree *BTreeIndex) Lookup(key string) []int {
	leaf := tree.findLeaf(key)
	if leaf == nil {
		return nil
	}
	index := sort.Search(len(leaf.entries), func(i int) bool {
		return leaf.entries[i].Key >= key
	})
	if index == len(leaf.entries) || leaf.entries[index].Key != key {
		return nil
	}
	return append([]int(nil), leaf.entries[index].RowIDs...)
}

func (tree *BTreeIndex) OpenRange(start, end string) *RangeCursor {
	leaf, entryIndex := tree.seek(start)
	return &RangeCursor{
		leaf:       leaf,
		entryIndex: entryIndex,
		end:        end,
	}
}

func (tree *BTreeIndex) Height() int {
	height := 0
	current := tree.root
	for current != nil {
		height++
		if current.leaf || len(current.children) == 0 {
			break
		}
		current = current.children[0]
	}
	return height
}

func (tree *BTreeIndex) RootKeys() []string {
	if tree.root == nil {
		return nil
	}
	if tree.root.leaf {
		keys := make([]string, 0, len(tree.root.entries))
		for _, entry := range tree.root.entries {
			keys = append(keys, entry.Key)
		}
		return keys
	}
	return append([]string(nil), tree.root.keys...)
}

func (tree *BTreeIndex) seek(start string) (*node, int) {
	if tree.root == nil {
		return nil, 0
	}
	if start == "" {
		return tree.firstLeaf, 0
	}
	leaf := tree.findLeaf(start)
	if leaf == nil {
		return nil, 0
	}
	index := sort.Search(len(leaf.entries), func(i int) bool {
		return leaf.entries[i].Key >= start
	})
	for leaf != nil && index == len(leaf.entries) {
		leaf = leaf.next
		index = 0
	}
	return leaf, index
}

func (tree *BTreeIndex) findLeaf(key string) *node {
	current := tree.root
	for current != nil && !current.leaf {
		childIndex := sort.Search(len(current.keys), func(i int) bool {
			return key < current.keys[i]
		})
		current = current.children[childIndex]
	}
	return current
}

func (tree *BTreeIndex) insert(current *node, key string, rowID int) *splitResult {
	if current.leaf {
		return tree.insertIntoLeaf(current, key, rowID)
	}

	childIndex := sort.Search(len(current.keys), func(i int) bool {
		return key < current.keys[i]
	})
	result := tree.insert(current.children[childIndex], key, rowID)
	if result == nil {
		return nil
	}

	current.keys = insertStringAt(current.keys, childIndex, result.promotedKey)
	current.children = insertNodeAt(current.children, childIndex+1, result.right)
	if len(current.keys) <= tree.order {
		return nil
	}
	return splitInternal(current)
}

func (tree *BTreeIndex) insertIntoLeaf(leaf *node, key string, rowID int) *splitResult {
	entryIndex := sort.Search(len(leaf.entries), func(i int) bool {
		return leaf.entries[i].Key >= key
	})
	if entryIndex < len(leaf.entries) && leaf.entries[entryIndex].Key == key {
		leaf.entries[entryIndex].RowIDs = append(leaf.entries[entryIndex].RowIDs, rowID)
		return nil
	}

	leaf.entries = insertEntryAt(leaf.entries, entryIndex, Entry{
		Key:    key,
		RowIDs: []int{rowID},
	})
	if len(leaf.entries) <= tree.order {
		return nil
	}

	splitIndex := len(leaf.entries) / 2
	rightEntries := append([]Entry(nil), leaf.entries[splitIndex:]...)
	right := &node{
		leaf:    true,
		entries: rightEntries,
		next:    leaf.next,
	}
	leaf.entries = append([]Entry(nil), leaf.entries[:splitIndex]...)
	leaf.next = right
	return &splitResult{
		promotedKey: right.entries[0].Key,
		right:       right,
	}
}

func splitInternal(current *node) *splitResult {
	splitIndex := len(current.keys) / 2
	right := &node{
		keys:     append([]string(nil), current.keys[splitIndex+1:]...),
		children: append([]*node(nil), current.children[splitIndex+1:]...),
	}
	result := &splitResult{
		promotedKey: current.keys[splitIndex],
		right:       right,
	}
	current.keys = append([]string(nil), current.keys[:splitIndex]...)
	current.children = append([]*node(nil), current.children[:splitIndex+1]...)
	return result
}

func (cursor *RangeCursor) Next() (Entry, bool) {
	for cursor.leaf != nil {
		if cursor.entryIndex >= len(cursor.leaf.entries) {
			cursor.leaf = cursor.leaf.next
			cursor.entryIndex = 0
			continue
		}
		entry := cursor.leaf.entries[cursor.entryIndex]
		if cursor.end != "" && entry.Key > cursor.end {
			return Entry{}, false
		}
		cursor.entryIndex++
		return Entry{
			Key:    entry.Key,
			RowIDs: append([]int(nil), entry.RowIDs...),
		}, true
	}
	return Entry{}, false
}

func insertEntryAt(entries []Entry, index int, entry Entry) []Entry {
	entries = append(entries, Entry{})
	copy(entries[index+1:], entries[index:])
	entries[index] = entry
	return entries
}

func insertStringAt(values []string, index int, value string) []string {
	values = append(values, "")
	copy(values[index+1:], values[index:])
	values[index] = value
	return values
}

func insertNodeAt(values []*node, index int, value *node) []*node {
	values = append(values, nil)
	copy(values[index+1:], values[index:])
	values[index] = value
	return values
}
