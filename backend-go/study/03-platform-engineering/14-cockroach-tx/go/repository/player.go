// Package repository provides data-access functions for the inventory service.
// All operations accept a *sql.Tx to participate in a caller-managed transaction.
package repository

import (
	"context"
	"database/sql"
	"errors"
	"time"
)

// ErrConflict is returned when an optimistic locking conflict is detected.
var ErrConflict = errors.New("optimistic locking conflict")

// Player represents a row in the players table.
type Player struct {
	ID        string
	Name      string
	Balance   int64
	Version   int
	CreatedAt time.Time
}

// GetPlayer retrieves a player by ID within the given transaction.
func GetPlayer(ctx context.Context, tx *sql.Tx, playerID string) (*Player, error) {
	p := &Player{}
	err := tx.QueryRowContext(ctx,
		`SELECT id, name, balance, version, created_at
		 FROM players WHERE id = $1`,
		playerID,
	).Scan(&p.ID, &p.Name, &p.Balance, &p.Version, &p.CreatedAt)
	if err != nil {
		return nil, err
	}
	return p, nil
}

// DeductBalance subtracts amount from the player's balance using optimistic
// locking. Returns ErrConflict if the version has changed since the player
// was read.
func DeductBalance(ctx context.Context, tx *sql.Tx, playerID string, amount int64, expectedVersion int) (newBalance int64, newVersion int, err error) {
	var balance int64
	var version int

	err = tx.QueryRowContext(ctx,
		`UPDATE players
		 SET balance = balance - $1, version = version + 1
		 WHERE id = $2 AND version = $3
		 RETURNING balance, version`,
		amount, playerID, expectedVersion,
	).Scan(&balance, &version)

	if errors.Is(err, sql.ErrNoRows) {
		return 0, 0, ErrConflict
	}
	if err != nil {
		return 0, 0, err
	}
	return balance, version, nil
}

// CreatePlayer inserts a new player. Primarily for testing.
func CreatePlayer(ctx context.Context, tx *sql.Tx, id, name string, balance int64) error {
	_, err := tx.ExecContext(ctx,
		`INSERT INTO players (id, name, balance) VALUES ($1, $2, $3)`,
		id, name, balance,
	)
	return err
}
