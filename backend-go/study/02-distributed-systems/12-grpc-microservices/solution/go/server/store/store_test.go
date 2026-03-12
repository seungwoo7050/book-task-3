package store

import (
	"testing"
)

func TestCreateAndGet(t *testing.T) {
	s := NewProductStore()

	p := s.Create(&Product{
		Name:       "Widget",
		Price:      9.99,
		Categories: []string{"tools"},
		Stock:      100,
	})

	if p.ID == "" {
		t.Fatal("expected a generated ID")
	}

	got, err := s.Get(p.ID)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if got.Name != "Widget" {
		t.Errorf("got name %q, want %q", got.Name, "Widget")
	}
}

func TestGetNotFound(t *testing.T) {
	s := NewProductStore()
	_, err := s.Get("nonexistent")
	if err != ErrNotFound {
		t.Errorf("expected ErrNotFound, got %v", err)
	}
}

func TestUpdate(t *testing.T) {
	s := NewProductStore()
	p := s.Create(&Product{Name: "Original", Price: 10.0, Categories: []string{"a"}, Stock: 5})

	updated, err := s.Update(&Product{ID: p.ID, Name: "Updated", Price: 20.0})
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if updated.Name != "Updated" {
		t.Errorf("got name %q, want %q", updated.Name, "Updated")
	}
	if updated.Price != 20.0 {
		t.Errorf("got price %f, want %f", updated.Price, 20.0)
	}
}

func TestDelete(t *testing.T) {
	s := NewProductStore()
	p := s.Create(&Product{Name: "ToDelete", Price: 5.0, Categories: []string{"temp"}, Stock: 1})

	err := s.Delete(p.ID)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	_, err = s.Get(p.ID)
	if err != ErrNotFound {
		t.Errorf("expected ErrNotFound after delete, got %v", err)
	}
}

func TestList(t *testing.T) {
	s := NewProductStore()
	s.Create(&Product{Name: "A", Price: 1, Categories: []string{"electronics"}, Stock: 1})
	s.Create(&Product{Name: "B", Price: 2, Categories: []string{"books"}, Stock: 1})
	s.Create(&Product{Name: "C", Price: 3, Categories: []string{"electronics"}, Stock: 1})

	tests := []struct {
		name    string
		filter  string
		wantLen int
	}{
		{"no filter", "", 3},
		{"filter electronics", "electronics", 2},
		{"filter books", "books", 1},
		{"filter nonexistent", "food", 0},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := s.List(tt.filter)
			if len(result) != tt.wantLen {
				t.Errorf("got %d results, want %d", len(result), tt.wantLen)
			}
		})
	}
}
