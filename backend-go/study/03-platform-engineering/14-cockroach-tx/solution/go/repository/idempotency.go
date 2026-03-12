package repository

import (
	"context"
	"database/sql"
	"encoding/json"
	"errors"
)

func GetIdempotencyKey(ctx context.Context, tx *sql.Tx, key string) (json.RawMessage, error) {
	var resp json.RawMessage
	err := tx.QueryRowContext(ctx,
		`SELECT response FROM idempotency_keys WHERE key = $1`, key,
	).Scan(&resp)
	if err != nil {
		return nil, err
	}
	return resp, nil
}
func InsertIdempotencyKey(ctx context.Context, tx *sql.Tx, key, playerID string, response json.RawMessage) error {
	_, err := tx.ExecContext(ctx,
		`INSERT INTO idempotency_keys (key, player_id, response)
		 VALUES ($1, $2, $3)`,
		key, playerID, response,
	)
	return err
}
func IdempotencyKeyExists(ctx context.Context, tx *sql.Tx, key string) (bool, error) {
	_, err := GetIdempotencyKey(ctx, tx, key)
	if errors.Is(err, sql.ErrNoRows) {
		return false, nil
	}
	if err != nil {
		return false, err
	}
	return true, nil
}
