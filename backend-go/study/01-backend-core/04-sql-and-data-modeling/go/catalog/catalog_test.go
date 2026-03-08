package catalog

import (
	"context"
	"database/sql"
	"errors"
	"testing"
)

func newTestDB(t *testing.T) *sqlDB {
	t.Helper()
	db, err := OpenInMemory()
	if err != nil {
		t.Fatalf("open db: %v", err)
	}
	ctx := context.Background()
	if err := ApplySchema(ctx, db); err != nil {
		t.Fatalf("apply schema: %v", err)
	}
	if err := Seed(ctx, db); err != nil {
		t.Fatalf("seed: %v", err)
	}
	return &sqlDB{db}
}

type sqlDB struct{ *sql.DB }

func TestListInventory(t *testing.T) {
	t.Parallel()

	db := newTestDB(t)
	rows, err := ListInventory(context.Background(), db.DB, "alice")
	if err != nil {
		t.Fatalf("list inventory: %v", err)
	}
	if len(rows) != 1 {
		t.Fatalf("rows len = %d, want 1", len(rows))
	}
	if rows[0].ItemName != "potion" {
		t.Fatalf("item = %q, want potion", rows[0].ItemName)
	}
}

func TestPurchase(t *testing.T) {
	t.Parallel()

	db := newTestDB(t)
	if err := Purchase(context.Background(), db.DB, 1, "sword", 1); err != nil {
		t.Fatalf("purchase: %v", err)
	}
	rows, err := ListInventory(context.Background(), db.DB, "alice")
	if err != nil {
		t.Fatalf("list after purchase: %v", err)
	}
	if len(rows) != 2 {
		t.Fatalf("rows len = %d, want 2", len(rows))
	}
}

func TestPurchaseUnknownItem(t *testing.T) {
	t.Parallel()

	db := newTestDB(t)
	err := Purchase(context.Background(), db.DB, 1, "missing", 1)
	if !errors.Is(err, ErrUnknownItem) {
		t.Fatalf("purchase error = %v, want %v", err, ErrUnknownItem)
	}
}
