package repository

import (
	"context"
	"database/sql"
	"encoding/json"
)

// InsertAuditLog records an action in the audit log.
func InsertAuditLog(ctx context.Context, tx *sql.Tx, playerID, action string, detail interface{}) error {
	detailJSON, err := json.Marshal(detail)
	if err != nil {
		return err
	}
	_, err = tx.ExecContext(ctx,
		`INSERT INTO audit_log (player_id, action, detail)
		 VALUES ($1, $2, $3)`,
		playerID, action, detailJSON,
	)
	return err
}
