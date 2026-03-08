package platform

import (
	"encoding/json"
	"errors"
	"net/http"
)

// AppError is a structured application error that maps directly to HTTP responses.
type AppError struct {
	Status  int    `json:"-"`
	Code    string `json:"code"`
	Message string `json:"message"`
}

func (e *AppError) Error() string {
	return e.Message
}

// Errorf creates an AppError for business-level failures.
func Errorf(status int, code, message string) *AppError {
	return &AppError{Status: status, Code: code, Message: message}
}

// WriteJSON encodes payload as JSON with the given status.
func WriteJSON(w http.ResponseWriter, status int, payload any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(payload)
}

// WriteError writes a structured error response.
func WriteError(w http.ResponseWriter, err error) {
	var appErr *AppError
	if errors.As(err, &appErr) {
		WriteJSON(w, appErr.Status, map[string]any{
			"error": map[string]string{
				"code":    appErr.Code,
				"message": appErr.Message,
			},
		})
		return
	}

	WriteJSON(w, http.StatusInternalServerError, map[string]any{
		"error": map[string]string{
			"code":    "internal_error",
			"message": "internal server error",
		},
	})
}

// DecodeJSON decodes request JSON payloads.
func DecodeJSON(r *http.Request, dst any) error {
	decoder := json.NewDecoder(r.Body)
	decoder.DisallowUnknownFields()
	if err := decoder.Decode(dst); err != nil {
		return Errorf(http.StatusBadRequest, "invalid_json", "request body must be valid JSON")
	}
	return nil
}
