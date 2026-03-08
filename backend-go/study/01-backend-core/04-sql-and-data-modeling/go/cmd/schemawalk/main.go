package main

import (
	"context"
	"fmt"
	"log"

	"github.com/woopinbell/go-backend/study/01-backend-core/04-sql-and-data-modeling/catalog"
)

func main() {
	ctx := context.Background()
	db, err := catalog.OpenInMemory()
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	if err := catalog.ApplySchema(ctx, db); err != nil {
		log.Fatal(err)
	}
	if err := catalog.Seed(ctx, db); err != nil {
		log.Fatal(err)
	}

	rows, err := catalog.ListInventory(ctx, db, "alice")
	if err != nil {
		log.Fatal(err)
	}
	for _, row := range rows {
		fmt.Printf("%s owns %d x %s\n", row.PlayerName, row.Quantity, row.ItemName)
	}
}
