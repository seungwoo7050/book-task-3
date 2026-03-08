// Package data contains the data models and in-memory stores
// for the application.
package data

import "time"

// Movie represents a movie record.
type Movie struct {
	ID        int64     `json:"id"`
	CreatedAt time.Time `json:"created_at"`
	Title     string    `json:"title"`
	Year      int32     `json:"year"`
	Runtime   int32     `json:"runtime"`
	Genres    []string  `json:"genres"`
	Version   int32     `json:"version"`
}

// Models wraps all data models for convenient dependency injection.
type Models struct {
	Movies *MovieStore
}

// NewModels returns a Models instance with initialized stores.
func NewModels() Models {
	return Models{
		Movies: NewMovieStore(),
	}
}
