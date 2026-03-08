package migrations

import "embed"

// Files contains the SQL migration files for the portfolio project.
//
//go:embed *.sql
var Files embed.FS
