package catalog

import (
	"context"
	"database/sql"
	"errors"
	"fmt"
	"time"

	_ "modernc.org/sqlite"
)

var ErrUnknownItem = errors.New("unknown item")

const schema = `
CREATE TABLE players (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    price_cents INTEGER NOT NULL CHECK (price_cents > 0)
);

CREATE TABLE inventory (
    player_id INTEGER NOT NULL REFERENCES players(id),
    item_id INTEGER NOT NULL REFERENCES items(id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    PRIMARY KEY (player_id, item_id)
);

CREATE INDEX idx_inventory_player ON inventory(player_id);
`

type InventoryRow struct {
	PlayerName string
	ItemName   string
	Quantity   int
}

func OpenInMemory() (*sql.DB, error) {
	return sql.Open("sqlite", fmt.Sprintf("file:sql-modeling-%d?mode=memory&cache=shared", time.Now().UnixNano()))
}

func ApplySchema(ctx context.Context, db *sql.DB) error {
	_, err := db.ExecContext(ctx, schema)
	return err
}

func Seed(ctx context.Context, db *sql.DB) error {
	statements := []string{
		`INSERT INTO players(id, name) VALUES (1, 'alice'), (2, 'bob')`,
		`INSERT INTO items(id, name, price_cents) VALUES (1, 'potion', 300), (2, 'sword', 1500)`,
		`INSERT INTO inventory(player_id, item_id, quantity) VALUES (1, 1, 2)`,
	}
	for _, stmt := range statements {
		if _, err := db.ExecContext(ctx, stmt); err != nil {
			return err
		}
	}
	return nil
}

func ListInventory(ctx context.Context, db *sql.DB, playerName string) ([]InventoryRow, error) {
	rows, err := db.QueryContext(ctx, `
SELECT p.name, i.name, inv.quantity
FROM inventory inv
JOIN players p ON p.id = inv.player_id
JOIN items i ON i.id = inv.item_id
WHERE p.name = ?
ORDER BY i.name
`, playerName)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var out []InventoryRow
	for rows.Next() {
		var row InventoryRow
		if err := rows.Scan(&row.PlayerName, &row.ItemName, &row.Quantity); err != nil {
			return nil, err
		}
		out = append(out, row)
	}
	return out, rows.Err()
}

func Purchase(ctx context.Context, db *sql.DB, playerID int, itemName string, quantity int) error {
	if quantity <= 0 {
		return fmt.Errorf("quantity must be positive")
	}

	tx, err := db.BeginTx(ctx, nil)
	if err != nil {
		return err
	}
	defer tx.Rollback()

	var itemID int
	err = tx.QueryRowContext(ctx, `SELECT id FROM items WHERE name = ?`, itemName).Scan(&itemID)
	if errors.Is(err, sql.ErrNoRows) {
		return ErrUnknownItem
	}
	if err != nil {
		return err
	}

	_, err = tx.ExecContext(ctx, `
INSERT INTO inventory(player_id, item_id, quantity)
VALUES (?, ?, ?)
ON CONFLICT(player_id, item_id)
DO UPDATE SET quantity = inventory.quantity + excluded.quantity
`, playerID, itemID, quantity)
	if err != nil {
		return err
	}

	return tx.Commit()
}
