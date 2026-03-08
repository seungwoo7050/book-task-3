package main

import (
	"fmt"
	"log"

	"github.com/woopinbell/go-backend/study/00-go-fundamentals/02-types-errors-interfaces/domain"
)

func main() {
	catalog := domain.NewCatalog()
	if err := catalog.Add(domain.Item{SKU: "starter-pack", Name: "Starter Pack", PriceCents: 3000}); err != nil {
		log.Fatal(err)
	}

	price, err := catalog.FinalPrice("starter-pack", domain.PercentageDiscount{Percent: 20})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("starter-pack final price: %d cents\n", price)
}
