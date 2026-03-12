package main

import (
	"context"
	"log"
	"net/http"

	"github.com/woopinbell/go-backend/study/01-backend-core/09-cache-migrations-observability/internal/app"
)

func main() {
	db, err := app.OpenInMemory()
	if err != nil {
		log.Fatal(err)
	}
	ctx := context.Background()
	if err := app.ApplyUpMigration(ctx, db); err != nil {
		log.Fatal(err)
	}
	if err := app.Seed(ctx, db); err != nil {
		log.Fatal(err)
	}

	service := app.NewService(db, nil)
	log.Println("listening on :4050")
	log.Fatal(http.ListenAndServe(":4050", service.Routes()))
}
