package store

import (
	"context"
	"database/sql"
	"encoding/json"
	"errors"
	"fmt"
	"net/http"
	"strconv"
	"time"

	_ "modernc.org/sqlite"
)

var (
	ErrNotFound          = errors.New("product not found")
	ErrConflict          = errors.New("version conflict")
	ErrInsufficientStock = errors.New("insufficient stock")
)

const schemaUp = `
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    stock INTEGER NOT NULL CHECK (stock >= 0),
    version INTEGER NOT NULL DEFAULT 1
);
`

const schemaDown = `DROP TABLE IF EXISTS products;`

type Product struct {
	ID      int64  `json:"id"`
	Name    string `json:"name"`
	Stock   int    `json:"stock"`
	Version int    `json:"version"`
}

type Repository struct {
	db *sql.DB
}

type App struct {
	repo *Repository
}

func OpenInMemory() (*sql.DB, error) {
	return sql.Open("sqlite", fmt.Sprintf("file:sql-store-api-%d?mode=memory&cache=shared", time.Now().UnixNano()))
}

func ApplyUpMigration(ctx context.Context, db *sql.DB) error {
	_, err := db.ExecContext(ctx, schemaUp)
	return err
}

func ApplyDownMigration(ctx context.Context, db *sql.DB) error {
	_, err := db.ExecContext(ctx, schemaDown)
	return err
}

func NewRepository(db *sql.DB) *Repository {
	return &Repository{db: db}
}

func NewApp(repo *Repository) *App {
	return &App{repo: repo}
}

func (r *Repository) Create(ctx context.Context, product *Product) error {
	result, err := r.db.ExecContext(ctx, `INSERT INTO products(name, stock) VALUES (?, ?)`, product.Name, product.Stock)
	if err != nil {
		return err
	}
	product.ID, err = result.LastInsertId()
	if err != nil {
		return err
	}
	product.Version = 1
	return nil
}

func (r *Repository) Get(ctx context.Context, id int64) (Product, error) {
	var product Product
	err := r.db.QueryRowContext(ctx, `SELECT id, name, stock, version FROM products WHERE id = ?`, id).
		Scan(&product.ID, &product.Name, &product.Stock, &product.Version)
	if errors.Is(err, sql.ErrNoRows) {
		return Product{}, ErrNotFound
	}
	return product, err
}

func (r *Repository) List(ctx context.Context) ([]Product, error) {
	rows, err := r.db.QueryContext(ctx, `SELECT id, name, stock, version FROM products ORDER BY id`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var out []Product
	for rows.Next() {
		var product Product
		if err := rows.Scan(&product.ID, &product.Name, &product.Stock, &product.Version); err != nil {
			return nil, err
		}
		out = append(out, product)
	}
	return out, rows.Err()
}

func (r *Repository) Update(ctx context.Context, product Product) error {
	result, err := r.db.ExecContext(ctx, `
UPDATE products
SET name = ?, stock = ?, version = version + 1
WHERE id = ? AND version = ?
`, product.Name, product.Stock, product.ID, product.Version)
	if err != nil {
		return err
	}
	affected, err := result.RowsAffected()
	if err != nil {
		return err
	}
	if affected == 0 {
		return ErrConflict
	}
	return nil
}

func (r *Repository) ReserveStock(ctx context.Context, id int64, quantity int) error {
	tx, err := r.db.BeginTx(ctx, nil)
	if err != nil {
		return err
	}
	defer tx.Rollback()

	var stock int
	err = tx.QueryRowContext(ctx, `SELECT stock FROM products WHERE id = ?`, id).Scan(&stock)
	if errors.Is(err, sql.ErrNoRows) {
		return ErrNotFound
	}
	if err != nil {
		return err
	}
	if stock < quantity {
		return ErrInsufficientStock
	}
	if _, err := tx.ExecContext(ctx, `UPDATE products SET stock = stock - ? WHERE id = ?`, quantity, id); err != nil {
		return err
	}
	return tx.Commit()
}

func (a *App) Routes() http.Handler {
	mux := http.NewServeMux()
	mux.HandleFunc("POST /v1/products", a.createProduct)
	mux.HandleFunc("GET /v1/products", a.listProducts)
	mux.HandleFunc("GET /v1/products/{id}", a.showProduct)
	mux.HandleFunc("PATCH /v1/products/{id}", a.updateProduct)
	return mux
}

func (a *App) createProduct(w http.ResponseWriter, r *http.Request) {
	var input struct {
		Name  string `json:"name"`
		Stock int    `json:"stock"`
	}
	if err := json.NewDecoder(r.Body).Decode(&input); err != nil {
		writeError(w, http.StatusBadRequest, "invalid json")
		return
	}
	if input.Name == "" || input.Stock < 0 {
		writeError(w, http.StatusUnprocessableEntity, "invalid input")
		return
	}

	product := Product{Name: input.Name, Stock: input.Stock}
	if err := a.repo.Create(r.Context(), &product); err != nil {
		writeError(w, http.StatusInternalServerError, "create failed")
		return
	}
	writeJSON(w, http.StatusCreated, map[string]any{"product": product})
}

func (a *App) listProducts(w http.ResponseWriter, r *http.Request) {
	products, err := a.repo.List(r.Context())
	if err != nil {
		writeError(w, http.StatusInternalServerError, "list failed")
		return
	}
	writeJSON(w, http.StatusOK, map[string]any{"products": products})
}

func (a *App) showProduct(w http.ResponseWriter, r *http.Request) {
	id, err := strconv.ParseInt(r.PathValue("id"), 10, 64)
	if err != nil {
		writeError(w, http.StatusBadRequest, "invalid id")
		return
	}
	product, err := a.repo.Get(r.Context(), id)
	if errors.Is(err, ErrNotFound) {
		writeError(w, http.StatusNotFound, "product not found")
		return
	}
	if err != nil {
		writeError(w, http.StatusInternalServerError, "server error")
		return
	}
	writeJSON(w, http.StatusOK, map[string]any{"product": product})
}

func (a *App) updateProduct(w http.ResponseWriter, r *http.Request) {
	id, err := strconv.ParseInt(r.PathValue("id"), 10, 64)
	if err != nil {
		writeError(w, http.StatusBadRequest, "invalid id")
		return
	}

	var input struct {
		Name    string `json:"name"`
		Stock   int    `json:"stock"`
		Version int    `json:"version"`
	}
	if err := json.NewDecoder(r.Body).Decode(&input); err != nil {
		writeError(w, http.StatusBadRequest, "invalid json")
		return
	}

	err = a.repo.Update(r.Context(), Product{
		ID:      id,
		Name:    input.Name,
		Stock:   input.Stock,
		Version: input.Version,
	})
	if errors.Is(err, ErrConflict) {
		writeError(w, http.StatusConflict, "version conflict")
		return
	}
	if err != nil {
		writeError(w, http.StatusInternalServerError, "update failed")
		return
	}

	product, err := a.repo.Get(r.Context(), id)
	if err != nil {
		writeError(w, http.StatusInternalServerError, "reload failed")
		return
	}
	writeJSON(w, http.StatusOK, map[string]any{"product": product})
}

func writeJSON(w http.ResponseWriter, status int, payload map[string]any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(payload)
}

func writeError(w http.ResponseWriter, status int, message string) {
	writeJSON(w, status, map[string]any{"error": map[string]string{"message": message}})
}
