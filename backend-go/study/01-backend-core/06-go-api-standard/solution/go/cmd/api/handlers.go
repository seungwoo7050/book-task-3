package main

import (
	"fmt"
	"net/http"
	"strconv"
	"time"

	"github.com/woopinbell/go-backend/study/01-backend-core/06-go-api-standard/internal/data"
)

func (app *application) healthcheckHandler(w http.ResponseWriter, r *http.Request) {
	env := envelope{
		"status": "available",
		"system_info": map[string]string{
			"environment": app.config.env,
			"version":     "1.0.0",
		},
	}

	err := app.writeJSON(w, http.StatusOK, env, nil)
	if err != nil {
		app.serverErrorResponse(w, r, err)
	}
}
func (app *application) createMovieHandler(w http.ResponseWriter, r *http.Request) {
	var input struct {
		Title   string   `json:"title"`
		Year    int32    `json:"year"`
		Runtime int32    `json:"runtime"`
		Genres  []string `json:"genres"`
	}

	err := app.readJSON(w, r, &input)
	if err != nil {
		app.badRequestResponse(w, r, err)
		return
	}

	movie := &data.Movie{
		Title:   input.Title,
		Year:    input.Year,
		Runtime: input.Runtime,
		Genres:  input.Genres,
	}
	if errs := validateMovie(movie); len(errs) > 0 {
		app.failedValidationResponse(w, r, errs)
		return
	}

	app.models.Movies.Insert(movie)

	headers := make(http.Header)
	headers.Set("Location", fmt.Sprintf("/v1/movies/%d", movie.ID))

	err = app.writeJSON(w, http.StatusCreated, envelope{"movie": movie}, headers)
	if err != nil {
		app.serverErrorResponse(w, r, err)
	}
}
func (app *application) showMovieHandler(w http.ResponseWriter, r *http.Request) {
	id, err := app.readIDParam(r)
	if err != nil {
		app.notFoundResponse(w, r)
		return
	}

	movie, err := app.models.Movies.Get(id)
	if err != nil {
		app.notFoundResponse(w, r)
		return
	}

	err = app.writeJSON(w, http.StatusOK, envelope{"movie": movie}, nil)
	if err != nil {
		app.serverErrorResponse(w, r, err)
	}
}
func (app *application) listMoviesHandler(w http.ResponseWriter, r *http.Request) {
	page, _ := strconv.Atoi(r.URL.Query().Get("page"))
	if page < 1 {
		page = 1
	}

	pageSize, _ := strconv.Atoi(r.URL.Query().Get("page_size"))
	if pageSize < 1 || pageSize > 100 {
		pageSize = 20
	}

	titleFilter := r.URL.Query().Get("title")

	movies, total := app.models.Movies.GetAll(titleFilter, page, pageSize)

	err := app.writeJSON(w, http.StatusOK, envelope{
		"movies": movies,
		"meta": map[string]int{
			"current_page": page,
			"page_size":    pageSize,
			"total":        total,
		},
	}, nil)
	if err != nil {
		app.serverErrorResponse(w, r, err)
	}
}
func (app *application) updateMovieHandler(w http.ResponseWriter, r *http.Request) {
	id, err := app.readIDParam(r)
	if err != nil {
		app.notFoundResponse(w, r)
		return
	}

	movie, err := app.models.Movies.Get(id)
	if err != nil {
		app.notFoundResponse(w, r)
		return
	}

	var input struct {
		Title   *string  `json:"title"`
		Year    *int32   `json:"year"`
		Runtime *int32   `json:"runtime"`
		Genres  []string `json:"genres"`
	}

	err = app.readJSON(w, r, &input)
	if err != nil {
		app.badRequestResponse(w, r, err)
		return
	}
	if input.Title != nil {
		movie.Title = *input.Title
	}
	if input.Year != nil {
		movie.Year = *input.Year
	}
	if input.Runtime != nil {
		movie.Runtime = *input.Runtime
	}
	if input.Genres != nil {
		movie.Genres = input.Genres
	}

	if errs := validateMovie(movie); len(errs) > 0 {
		app.failedValidationResponse(w, r, errs)
		return
	}

	movie.Version++

	app.models.Movies.Update(movie)

	err = app.writeJSON(w, http.StatusOK, envelope{"movie": movie}, nil)
	if err != nil {
		app.serverErrorResponse(w, r, err)
	}
}
func (app *application) deleteMovieHandler(w http.ResponseWriter, r *http.Request) {
	id, err := app.readIDParam(r)
	if err != nil {
		app.notFoundResponse(w, r)
		return
	}

	err = app.models.Movies.Delete(id)
	if err != nil {
		app.notFoundResponse(w, r)
		return
	}

	err = app.writeJSON(w, http.StatusOK, envelope{"message": "movie successfully deleted"}, nil)
	if err != nil {
		app.serverErrorResponse(w, r, err)
	}
}
func validateMovie(movie *data.Movie) map[string]string {
	errs := make(map[string]string)

	if movie.Title == "" {
		errs["title"] = "must be provided"
	}
	if len(movie.Title) > 500 {
		errs["title"] = "must not be more than 500 bytes long"
	}
	if movie.Year < 1888 {
		errs["year"] = "must be greater than 1888"
	}
	if movie.Year > int32(time.Now().Year()) {
		errs["year"] = "must not be in the future"
	}
	if movie.Runtime < 1 {
		errs["runtime"] = "must be a positive integer"
	}
	if len(movie.Genres) == 0 {
		errs["genres"] = "must contain at least one genre"
	}
	if len(movie.Genres) > 5 {
		errs["genres"] = "must not contain more than 5 genres"
	}
	seen := make(map[string]bool)
	for _, g := range movie.Genres {
		if seen[g] {
			errs["genres"] = "must not contain duplicate values"
			break
		}
		seen[g] = true
	}

	return errs
}
