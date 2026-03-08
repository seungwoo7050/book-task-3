package domain

import (
	"errors"
	"testing"
)

func TestCatalogAddDuplicate(t *testing.T) {
	t.Parallel()

	catalog := NewCatalog()
	item := Item{SKU: "sku-1", Name: "Sword", PriceCents: 1500}
	if err := catalog.Add(item); err != nil {
		t.Fatalf("unexpected add error: %v", err)
	}
	if err := catalog.Add(item); !errors.Is(err, ErrDuplicateSKU) {
		t.Fatalf("duplicate add error = %v, want %v", err, ErrDuplicateSKU)
	}
}

func TestCatalogFinalPrice(t *testing.T) {
	t.Parallel()

	catalog := NewCatalog()
	if err := catalog.Add(Item{SKU: "sku-2", Name: "Shield", PriceCents: 2000}); err != nil {
		t.Fatalf("add error: %v", err)
	}
	price, err := catalog.FinalPrice("sku-2", PercentageDiscount{Percent: 10})
	if err != nil {
		t.Fatalf("final price error: %v", err)
	}
	if price != 1800 {
		t.Fatalf("price = %d, want 1800", price)
	}
}

func TestCatalogGetNotFound(t *testing.T) {
	t.Parallel()

	catalog := NewCatalog()
	_, err := catalog.Get("missing")
	var notFound NotFoundError
	if !errors.As(err, &notFound) {
		t.Fatalf("expected NotFoundError, got %v", err)
	}
}
