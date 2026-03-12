package data

import (
	"errors"
	"strings"
	"sync"
	"sync/atomic"
	"time"
)

var ErrRecordNotFound = errors.New("record not found")

type MovieStore struct {
	mu     sync.RWMutex
	movies map[int64]*Movie
	nextID atomic.Int64
}

func NewMovieStore() *MovieStore {
	s := &MovieStore{
		movies: make(map[int64]*Movie),
	}
	s.nextID.Store(1)
	return s
}
func (s *MovieStore) Insert(movie *Movie) {
	s.mu.Lock()
	defer s.mu.Unlock()

	movie.ID = s.nextID.Add(1) - 1
	movie.CreatedAt = time.Now().UTC()
	movie.Version = 1
	stored := *movie
	stored.Genres = make([]string, len(movie.Genres))
	copy(stored.Genres, movie.Genres)

	s.movies[movie.ID] = &stored
}
func (s *MovieStore) Get(id int64) (*Movie, error) {
	s.mu.RLock()
	defer s.mu.RUnlock()

	movie, ok := s.movies[id]
	if !ok {
		return nil, ErrRecordNotFound
	}
	result := *movie
	result.Genres = make([]string, len(movie.Genres))
	copy(result.Genres, movie.Genres)

	return &result, nil
}
func (s *MovieStore) Update(movie *Movie) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	if _, ok := s.movies[movie.ID]; !ok {
		return ErrRecordNotFound
	}

	stored := *movie
	stored.Genres = make([]string, len(movie.Genres))
	copy(stored.Genres, movie.Genres)

	s.movies[movie.ID] = &stored
	return nil
}
func (s *MovieStore) Delete(id int64) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	if _, ok := s.movies[id]; !ok {
		return ErrRecordNotFound
	}

	delete(s.movies, id)
	return nil
}
func (s *MovieStore) GetAll(titleFilter string, page, pageSize int) ([]*Movie, int) {
	s.mu.RLock()
	defer s.mu.RUnlock()

	var all []*Movie
	for _, m := range s.movies {
		if titleFilter != "" && !strings.Contains(
			strings.ToLower(m.Title),
			strings.ToLower(titleFilter),
		) {
			continue
		}
		cp := *m
		cp.Genres = make([]string, len(m.Genres))
		copy(cp.Genres, m.Genres)
		all = append(all, &cp)
	}

	total := len(all)
	start := (page - 1) * pageSize
	if start >= total {
		return []*Movie{}, total
	}
	end := start + pageSize
	if end > total {
		end = total
	}

	return all[start:end], total
}
