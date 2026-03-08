package main

import (
	"context"
	"database/sql"
	"fmt"
	"io/fs"
	"log"
	"os"
	"sort"

	_ "github.com/jackc/pgx/v5/stdlib"

	"github.com/woopinbell/go-backend/study/05-portfolio-projects/18-workspace-saas-api/internal/platform"
	migrationfiles "github.com/woopinbell/go-backend/study/05-portfolio-projects/18-workspace-saas-api/migrations"
	seedfiles "github.com/woopinbell/go-backend/study/05-portfolio-projects/18-workspace-saas-api/seed"
)

func main() {
	if len(os.Args) < 2 {
		log.Fatalf("usage: go run ./cmd/migrate [up|seed]")
	}

	cfg := platform.LoadConfig()
	db, err := sql.Open("pgx", cfg.DatabaseURL)
	if err != nil {
		log.Fatalf("open database: %v", err)
	}
	defer db.Close()

	ctx := context.Background()
	if err := db.PingContext(ctx); err != nil {
		log.Fatalf("ping database: %v", err)
	}

	switch os.Args[1] {
	case "up":
		if err := applyFiles(ctx, db, migrationfiles.Files); err != nil {
			log.Fatalf("apply migrations: %v", err)
		}
	case "seed":
		if err := applyFiles(ctx, db, seedfiles.Files); err != nil {
			log.Fatalf("apply seed: %v", err)
		}
	default:
		log.Fatalf("unknown command %q", os.Args[1])
	}
}

func applyFiles(ctx context.Context, db *sql.DB, files fs.FS) error {
	entries, err := fs.ReadDir(files, ".")
	if err != nil {
		return err
	}

	names := make([]string, 0, len(entries))
	for _, entry := range entries {
		if entry.IsDir() {
			continue
		}
		names = append(names, entry.Name())
	}
	sort.Strings(names)

	for _, name := range names {
		statement, err := fs.ReadFile(files, name)
		if err != nil {
			return err
		}
		if _, err := db.ExecContext(ctx, string(statement)); err != nil {
			return fmt.Errorf("%s: %w", name, err)
		}
	}
	return nil
}
