package domain

import (
	"errors"
	"fmt"
)

var ErrDuplicateSKU = errors.New("duplicate sku")

type Item struct {
	SKU        string
	Name       string
	PriceCents int
}

type PricingRule interface {
	Apply(priceCents int) int
}

type PercentageDiscount struct {
	Percent int
}

func (d PercentageDiscount) Apply(priceCents int) int {
	if d.Percent <= 0 {
		return priceCents
	}
	return priceCents - (priceCents*d.Percent)/100
}

type NotFoundError struct {
	SKU string
}

func (e NotFoundError) Error() string {
	return fmt.Sprintf("item %q not found", e.SKU)
}

type Catalog struct {
	items map[string]Item
}

func NewCatalog() *Catalog {
	return &Catalog{items: make(map[string]Item)}
}

func (c *Catalog) Add(item Item) error {
	if _, exists := c.items[item.SKU]; exists {
		return ErrDuplicateSKU
	}
	c.items[item.SKU] = item
	return nil
}

func (c *Catalog) Get(sku string) (Item, error) {
	item, ok := c.items[sku]
	if !ok {
		return Item{}, NotFoundError{SKU: sku}
	}
	return item, nil
}

func (c *Catalog) FinalPrice(sku string, rule PricingRule) (int, error) {
	item, err := c.Get(sku)
	if err != nil {
		return 0, err
	}
	if rule == nil {
		return item.PriceCents, nil
	}
	return rule.Apply(item.PriceCents), nil
}
