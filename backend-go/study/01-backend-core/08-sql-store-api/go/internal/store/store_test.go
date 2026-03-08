package store

import (
	"bytes"
	"context"
	"database/sql"
	"errors"
	"net/http"
	"net/http/httptest"
	"testing"
)

func newTestRepo(t *testing.T) (*Repository, *sql.DB) {
	t.Helper()
	db, err := OpenInMemory()
	if err != nil {
		t.Fatalf("open db: %v", err)
	}
	if err := ApplyUpMigration(context.Background(), db); err != nil {
		t.Fatalf("apply migration: %v", err)
	}
	return NewRepository(db), db
}

func TestMigrationUpDown(t *testing.T) {
	t.Parallel()

	db, err := OpenInMemory()
	if err != nil {
		t.Fatalf("open db: %v", err)
	}
	ctx := context.Background()
	if err := ApplyUpMigration(ctx, db); err != nil {
		t.Fatalf("apply up: %v", err)
	}
	if err := ApplyDownMigration(ctx, db); err != nil {
		t.Fatalf("apply down: %v", err)
	}

	_, err = db.ExecContext(ctx, `SELECT * FROM products`)
	if err == nil {
		t.Fatal("expected missing table after down migration")
	}
}

func TestRepositoryCRUD(t *testing.T) {
	t.Parallel()

	repo, db := newTestRepo(t)
	defer db.Close()

	product := Product{Name: "potion", Stock: 10}
	if err := repo.Create(context.Background(), &product); err != nil {
		t.Fatalf("create: %v", err)
	}

	loaded, err := repo.Get(context.Background(), product.ID)
	if err != nil {
		t.Fatalf("get: %v", err)
	}
	loaded.Name = "super potion"
	if err := repo.Update(context.Background(), loaded); err != nil {
		t.Fatalf("update: %v", err)
	}

	list, err := repo.List(context.Background())
	if err != nil {
		t.Fatalf("list: %v", err)
	}
	if len(list) != 1 {
		t.Fatalf("list len = %d, want 1", len(list))
	}
}

func TestReserveStockRollback(t *testing.T) {
	t.Parallel()

	repo, db := newTestRepo(t)
	defer db.Close()

	product := Product{Name: "sword", Stock: 2}
	if err := repo.Create(context.Background(), &product); err != nil {
		t.Fatalf("create: %v", err)
	}
	err := repo.ReserveStock(context.Background(), product.ID, 3)
	if !errors.Is(err, ErrInsufficientStock) {
		t.Fatalf("reserve err = %v, want %v", err, ErrInsufficientStock)
	}
	loaded, err := repo.Get(context.Background(), product.ID)
	if err != nil {
		t.Fatalf("get: %v", err)
	}
	if loaded.Stock != 2 {
		t.Fatalf("stock = %d, want 2", loaded.Stock)
	}
}

func TestCreateProductValidation(t *testing.T) {
	t.Parallel()

	repo, db := newTestRepo(t)
	defer db.Close()

	req := httptest.NewRequest(http.MethodPost, "/v1/products", bytes.NewBufferString(`{"name":"","stock":1}`))
	rr := httptest.NewRecorder()
	NewApp(repo).Routes().ServeHTTP(rr, req)

	if rr.Code != http.StatusUnprocessableEntity {
		t.Fatalf("status = %d, want %d", rr.Code, http.StatusUnprocessableEntity)
	}
}
