package data

import (
	"testing"
)

func TestMovieStoreInsertAndGet(t *testing.T) {
	store := NewMovieStore()

	movie := &Movie{Title: "Test Movie", Year: 2020, Runtime: 120, Genres: []string{"action"}}
	store.Insert(movie)

	if movie.ID != 1 {
		t.Errorf("expected ID 1, got %d", movie.ID)
	}
	if movie.Version != 1 {
		t.Errorf("expected Version 1, got %d", movie.Version)
	}

	got, err := store.Get(1)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if got.Title != "Test Movie" {
		t.Errorf("expected title 'Test Movie', got %q", got.Title)
	}
}

func TestMovieStoreGetNotFound(t *testing.T) {
	store := NewMovieStore()

	_, err := store.Get(999)
	if err != ErrRecordNotFound {
		t.Errorf("expected ErrRecordNotFound, got %v", err)
	}
}

func TestMovieStoreUpdate(t *testing.T) {
	store := NewMovieStore()

	movie := &Movie{Title: "Original", Year: 2020, Runtime: 90, Genres: []string{"drama"}}
	store.Insert(movie)

	movie.Title = "Updated"
	movie.Version = 2
	err := store.Update(movie)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	got, _ := store.Get(movie.ID)
	if got.Title != "Updated" {
		t.Errorf("expected title 'Updated', got %q", got.Title)
	}
}

func TestMovieStoreDelete(t *testing.T) {
	store := NewMovieStore()

	movie := &Movie{Title: "ToDelete", Year: 2020, Runtime: 90, Genres: []string{"comedy"}}
	store.Insert(movie)

	err := store.Delete(movie.ID)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	_, err = store.Get(movie.ID)
	if err != ErrRecordNotFound {
		t.Errorf("expected ErrRecordNotFound after delete, got %v", err)
	}
}

func TestMovieStoreDeleteNotFound(t *testing.T) {
	store := NewMovieStore()

	err := store.Delete(999)
	if err != ErrRecordNotFound {
		t.Errorf("expected ErrRecordNotFound, got %v", err)
	}
}

func TestMovieStoreGetAll(t *testing.T) {
	store := NewMovieStore()

	movies := []*Movie{
		{Title: "Alpha", Year: 2020, Runtime: 90, Genres: []string{"action"}},
		{Title: "Beta", Year: 2021, Runtime: 100, Genres: []string{"comedy"}},
		{Title: "Alpha Two", Year: 2022, Runtime: 110, Genres: []string{"action"}},
	}
	for _, m := range movies {
		store.Insert(m)
	}

	tests := []struct {
		name        string
		titleFilter string
		page        int
		pageSize    int
		wantCount   int
		wantTotal   int
	}{
		{
			name:      "all movies page 1",
			page:      1,
			pageSize:  10,
			wantCount: 3,
			wantTotal: 3,
		},
		{
			name:      "paginate page 1 size 2",
			page:      1,
			pageSize:  2,
			wantCount: 2,
			wantTotal: 3,
		},
		{
			name:        "filter by alpha",
			titleFilter: "alpha",
			page:        1,
			pageSize:    10,
			wantCount:   2,
			wantTotal:   2,
		},
		{
			name:      "page beyond range",
			page:      10,
			pageSize:  10,
			wantCount: 0,
			wantTotal: 3,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			results, total := store.GetAll(tt.titleFilter, tt.page, tt.pageSize)
			if len(results) != tt.wantCount {
				t.Errorf("got %d results, want %d", len(results), tt.wantCount)
			}
			if total != tt.wantTotal {
				t.Errorf("got total %d, want %d", total, tt.wantTotal)
			}
		})
	}
}

func TestMovieStoreConcurrency(t *testing.T) {
	store := NewMovieStore()
	done := make(chan bool)
	for i := 0; i < 100; i++ {
		go func(n int) {
			store.Insert(&Movie{
				Title:   "Concurrent Movie",
				Year:    2020,
				Runtime: 90,
				Genres:  []string{"test"},
			})
			done <- true
		}(i)
	}

	for i := 0; i < 100; i++ {
		<-done
	}

	_, total := store.GetAll("", 1, 200)
	if total != 100 {
		t.Errorf("expected 100 movies, got %d", total)
	}
}
