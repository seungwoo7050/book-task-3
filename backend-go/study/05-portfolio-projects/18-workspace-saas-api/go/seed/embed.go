package seed

import "embed"

// Files contains seed SQL files used by cmd/migrate.
//
//go:embed *.sql
var Files embed.FS
