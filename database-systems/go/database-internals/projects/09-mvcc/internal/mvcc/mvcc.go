package mvcc

import "fmt"

type Version struct {
	Value   any
	TxID    int
	Deleted bool
}

type VersionStore struct {
	Store map[string][]Version
}

func NewVersionStore() *VersionStore {
	return &VersionStore{Store: map[string][]Version{}}
}

func (store *VersionStore) Append(key string, value any, txID int, deleted bool) {
	chain := store.Store[key]
	index := 0
	for index < len(chain) && chain[index].TxID > txID {
		index++
	}
	chain = append(chain, Version{})
	copy(chain[index+1:], chain[index:])
	chain[index] = Version{Value: value, TxID: txID, Deleted: deleted}
	store.Store[key] = chain
}

func (store *VersionStore) GetVisible(key string, snapshot int, committed map[int]bool) *Version {
	chain := store.Store[key]
	for _, version := range chain {
		if version.TxID <= snapshot && committed[version.TxID] {
			copyVersion := version
			return &copyVersion
		}
	}
	return nil
}

func (store *VersionStore) RemoveByTxID(key string, txID int) {
	chain := store.Store[key]
	filtered := make([]Version, 0, len(chain))
	for _, version := range chain {
		if version.TxID != txID {
			filtered = append(filtered, version)
		}
	}
	if len(filtered) == 0 {
		delete(store.Store, key)
		return
	}
	store.Store[key] = filtered
}

func (store *VersionStore) GC(minSnapshot int) {
	for key, chain := range store.Store {
		recent := []Version{}
		old := []Version{}
		for _, version := range chain {
			if version.TxID >= minSnapshot {
				recent = append(recent, version)
			} else {
				old = append(old, version)
			}
		}
		if len(old) > 0 {
			recent = append(recent, old[0])
		}
		if len(recent) == 0 {
			delete(store.Store, key)
			continue
		}
		store.Store[key] = recent
	}
}

const (
	txActive    = "active"
	txCommitted = "committed"
	txAborted   = "aborted"
)

type Transaction struct {
	Snapshot int
	Status   string
	WriteSet map[string]bool
}

type TransactionManager struct {
	NextTxID     int
	VersionStore *VersionStore
	Transactions map[int]*Transaction
	Committed    map[int]bool
}

func NewTransactionManager() *TransactionManager {
	return &TransactionManager{
		NextTxID:     1,
		VersionStore: NewVersionStore(),
		Transactions: map[int]*Transaction{},
		Committed:    map[int]bool{},
	}
}

func (manager *TransactionManager) Begin() int {
	txID := manager.NextTxID
	manager.NextTxID++

	maxCommitted := 0
	for id := range manager.Committed {
		if id > maxCommitted {
			maxCommitted = id
		}
	}
	manager.Transactions[txID] = &Transaction{
		Snapshot: maxCommitted,
		Status:   txActive,
		WriteSet: map[string]bool{},
	}
	return txID
}

func (manager *TransactionManager) Read(txID int, key string) any {
	tx := manager.activeTx(txID)

	if tx.WriteSet[key] {
		for _, version := range manager.VersionStore.Store[key] {
			if version.TxID == txID {
				if version.Deleted {
					return nil
				}
				return version.Value
			}
		}
	}

	version := manager.VersionStore.GetVisible(key, tx.Snapshot, manager.Committed)
	if version == nil || version.Deleted {
		return nil
	}
	return version.Value
}

func (manager *TransactionManager) Write(txID int, key string, value any) {
	tx := manager.activeTx(txID)
	manager.VersionStore.Append(key, value, txID, false)
	tx.WriteSet[key] = true
}

func (manager *TransactionManager) Delete(txID int, key string) {
	tx := manager.activeTx(txID)
	manager.VersionStore.Append(key, nil, txID, true)
	tx.WriteSet[key] = true
}

func (manager *TransactionManager) Commit(txID int) error {
	tx := manager.activeTx(txID)
	for key := range tx.WriteSet {
		for _, version := range manager.VersionStore.Store[key] {
			if version.TxID > tx.Snapshot && version.TxID != txID && manager.Committed[version.TxID] {
				manager.abortInternal(txID, tx)
				return fmt.Errorf("write-write conflict on key %q", key)
			}
		}
	}

	tx.Status = txCommitted
	manager.Committed[txID] = true
	return nil
}

func (manager *TransactionManager) Abort(txID int) {
	manager.abortInternal(txID, manager.activeTx(txID))
}

func (manager *TransactionManager) GC() {
	minSnapshot := manager.NextTxID
	for _, tx := range manager.Transactions {
		if tx.Status == txActive && tx.Snapshot < minSnapshot {
			minSnapshot = tx.Snapshot
		}
	}
	manager.VersionStore.GC(minSnapshot)
}

func (manager *TransactionManager) activeTx(txID int) *Transaction {
	tx := manager.Transactions[txID]
	if tx == nil {
		panic(fmt.Sprintf("unknown transaction %d", txID))
	}
	if tx.Status != txActive {
		panic(fmt.Sprintf("transaction %d is %s", txID, tx.Status))
	}
	return tx
}

func (manager *TransactionManager) abortInternal(txID int, tx *Transaction) {
	for key := range tx.WriteSet {
		manager.VersionStore.RemoveByTxID(key, txID)
	}
	tx.Status = txAborted
}
