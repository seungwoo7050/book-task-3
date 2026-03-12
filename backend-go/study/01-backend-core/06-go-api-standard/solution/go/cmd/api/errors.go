package main

import (
	"net/http"
)

func (app *application) errorResponse(w http.ResponseWriter, r *http.Request, status int, message any) {
	env := envelope{"error": map[string]any{"message": message}}

	err := app.writeJSON(w, status, env, nil)
	if err != nil {
		app.logger.Error("error writing response", "error", err)
		w.WriteHeader(http.StatusInternalServerError)
	}
}
func (app *application) serverErrorResponse(w http.ResponseWriter, r *http.Request, err error) {
	app.logger.Error("internal server error",
		"method", r.Method,
		"uri", r.URL.RequestURI(),
		"error", err.Error(),
	)
	app.errorResponse(w, r, http.StatusInternalServerError, "the server encountered a problem and could not process your request")
}
func (app *application) notFoundResponse(w http.ResponseWriter, r *http.Request) {
	app.errorResponse(w, r, http.StatusNotFound, "the requested resource could not be found")
}
func (app *application) badRequestResponse(w http.ResponseWriter, r *http.Request, err error) {
	app.errorResponse(w, r, http.StatusBadRequest, err.Error())
}
func (app *application) failedValidationResponse(w http.ResponseWriter, r *http.Request, errors map[string]string) {
	app.errorResponse(w, r, http.StatusUnprocessableEntity, errors)
}
