package main

import "net/http"

// routes sets up the HTTP router with Go 1.22 enhanced patterns
// and wraps it with the middleware chain.
func (app *application) routes() http.Handler {
	mux := http.NewServeMux()

	// Healthcheck
	mux.HandleFunc("GET /v1/healthcheck", app.healthcheckHandler)

	// Movies CRUD
	mux.HandleFunc("POST /v1/movies", app.createMovieHandler)
	mux.HandleFunc("GET /v1/movies/{id}", app.showMovieHandler)
	mux.HandleFunc("GET /v1/movies", app.listMoviesHandler)
	mux.HandleFunc("PATCH /v1/movies/{id}", app.updateMovieHandler)
	mux.HandleFunc("DELETE /v1/movies/{id}", app.deleteMovieHandler)

	// Apply middleware (outermost runs first).
	return app.recoverPanic(app.logRequest(app.enableCORS(mux)))
}
