package main

import (
	"context"
	"log"
	"net/http"

	"github.com/woopinbell/go-backend/study/01-backend-core/08-sql-store-api/internal/store"
)

func main() {
	db, err := store.OpenInMemory()
	if err != nil {
		log.Fatal(err)
	}
	if err := store.ApplyUpMigration(context.Background(), db); err != nil {
		log.Fatal(err)
	}

	app := store.NewApp(store.NewRepository(db))
	log.Println("listening on :4040")
	log.Fatal(http.ListenAndServe(":4040", app.Routes()))
}
