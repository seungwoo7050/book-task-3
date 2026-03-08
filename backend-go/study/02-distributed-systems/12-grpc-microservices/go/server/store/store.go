// Package store provides an in-memory product store for the gRPC catalog service.
package store

import (
	"errors"
	"fmt"
	"strings"
	"sync"
	"sync/atomic"
	"time"
)

// Product represents a product in the catalog.
type Product struct {
	ID          string
	Name        string
	Description string
	Price       float64
	Categories  []string
	Stock       int32
	CreatedAt   time.Time
	UpdatedAt   time.Time
}

var (
	ErrNotFound      = errors.New("product not found")
	ErrAlreadyExists = errors.New("product already exists")
)

// ProductStore is a thread-safe in-memory store for products.
type ProductStore struct {
	mu       sync.RWMutex
	products map[string]*Product
	nextID   atomic.Int64
}

// NewProductStore creates an empty product store.
func NewProductStore() *ProductStore {
	s := &ProductStore{
		products: make(map[string]*Product),
	}
	s.nextID.Store(1)
	return s
}

// Create adds a new product and returns it with a generated ID.
func (s *ProductStore) Create(p *Product) *Product {
	s.mu.Lock()
	defer s.mu.Unlock()

	id := s.nextID.Add(1) - 1
	p.ID = fmt.Sprintf("prod-%d", id)
	p.CreatedAt = time.Now().UTC()
	p.UpdatedAt = p.CreatedAt

	stored := copyProduct(p)
	s.products[p.ID] = stored

	return copyProduct(stored)
}

// Get retrieves a product by ID.
func (s *ProductStore) Get(id string) (*Product, error) {
	s.mu.RLock()
	defer s.mu.RUnlock()

	p, ok := s.products[id]
	if !ok {
		return nil, ErrNotFound
	}
	return copyProduct(p), nil
}

// Update modifies an existing product.
func (s *ProductStore) Update(p *Product) (*Product, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	existing, ok := s.products[p.ID]
	if !ok {
		return nil, ErrNotFound
	}

	if p.Name != "" {
		existing.Name = p.Name
	}
	if p.Description != "" {
		existing.Description = p.Description
	}
	if p.Price > 0 {
		existing.Price = p.Price
	}
	if len(p.Categories) > 0 {
		existing.Categories = make([]string, len(p.Categories))
		copy(existing.Categories, p.Categories)
	}
	if p.Stock >= 0 {
		existing.Stock = p.Stock
	}
	existing.UpdatedAt = time.Now().UTC()

	return copyProduct(existing), nil
}

// Delete removes a product by ID.
func (s *ProductStore) Delete(id string) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	if _, ok := s.products[id]; !ok {
		return ErrNotFound
	}
	delete(s.products, id)
	return nil
}

// List returns all products, optionally filtered by category.
func (s *ProductStore) List(categoryFilter string) []*Product {
	s.mu.RLock()
	defer s.mu.RUnlock()

	var result []*Product
	for _, p := range s.products {
		if categoryFilter != "" {
			found := false
			for _, c := range p.Categories {
				if strings.EqualFold(c, categoryFilter) {
					found = true
					break
				}
			}
			if !found {
				continue
			}
		}
		result = append(result, copyProduct(p))
	}
	return result
}

func copyProduct(p *Product) *Product {
	cp := *p
	cp.Categories = make([]string, len(p.Categories))
	copy(cp.Categories, p.Categories)
	return &cp
}
