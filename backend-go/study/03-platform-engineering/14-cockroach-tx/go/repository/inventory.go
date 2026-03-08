package repository

import (
	"context"
	"database/sql"
)

// UpsertInventory adds an item to the player's inventory or increments
// the quantity if the item already exists.
func UpsertInventory(ctx context.Context, tx *sql.Tx, playerID, itemName string, quantity int) error {
	_, err := tx.ExecContext(ctx,
		`INSERT INTO inventory (player_id, item_name, quantity)
		 VALUES ($1, $2, $3)
		 ON CONFLICT (player_id, item_name)
		 DO UPDATE SET quantity = inventory.quantity + EXCLUDED.quantity`,
		playerID, itemName, quantity,
	)
	return err
}
