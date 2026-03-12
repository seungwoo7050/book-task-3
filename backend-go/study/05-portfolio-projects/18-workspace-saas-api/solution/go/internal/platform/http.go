package platform

import (
	"encoding/json"
	"errors"
	"net/http"
)

// AppError는 HTTP 응답 코드와 에러 페이로드를 함께 표현한다.
type AppError struct {
	Status  int    `json:"-"`
	Code    string `json:"code"`
	Message string `json:"message"`
}

func (e *AppError) Error() string {
	return e.Message
}

// Errorf는 상태 코드와 에러 정보를 묶은 AppError를 만든다.
func Errorf(status int, code, message string) *AppError {
	return &AppError{Status: status, Code: code, Message: message}
}

// WriteJSON은 지정한 상태 코드와 JSON 페이로드를 응답으로 쓴다.
func WriteJSON(w http.ResponseWriter, status int, payload any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(payload)
}

// WriteError는 AppError 또는 기본 500 에러 응답을 JSON으로 기록한다.
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

// DecodeJSON은 요청 본문을 JSON으로 디코딩한다.
func DecodeJSON(r *http.Request, dst any) error {
	decoder := json.NewDecoder(r.Body)
	decoder.DisallowUnknownFields()
	if err := decoder.Decode(dst); err != nil {
		return Errorf(http.StatusBadRequest, "invalid_json", "request body must be valid JSON")
	}
	return nil
}
