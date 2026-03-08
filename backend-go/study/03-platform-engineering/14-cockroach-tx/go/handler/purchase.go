// Package handler provides HTTP handlers for the inventory service.
package handler

import (
	"encoding/json"
	"errors"
	"net/http"

	"github.com/woopinbell/go-backend/study/03-platform-engineering/14-cockroach-tx/repository"
	"github.com/woopinbell/go-backend/study/03-platform-engineering/14-cockroach-tx/service"
)

// PurchaseHandler handles POST /api/purchase requests.
type PurchaseHandler struct {
	Service *service.PurchaseService
}

// purchaseInput is the JSON request body for a purchase.
type purchaseInput struct {
	PlayerID string `json:"player_id"`
	ItemName string `json:"item_name"`
	Price    int64  `json:"price"`
}

// errorResponse is a standard error envelope.
type errorResponse struct {
	Error string `json:"error"`
}

// ServeHTTP implements http.Handler.
func (h *PurchaseHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		writeJSON(w, http.StatusMethodNotAllowed, errorResponse{Error: "method not allowed"})
		return
	}

	// Extract idempotency key from header.
	idempotencyKey := r.Header.Get("Idempotency-Key")
	if idempotencyKey == "" {
		writeJSON(w, http.StatusBadRequest, errorResponse{Error: "Idempotency-Key header is required"})
		return
	}

	// Decode body.
	var input purchaseInput
	if err := json.NewDecoder(r.Body).Decode(&input); err != nil {
		writeJSON(w, http.StatusBadRequest, errorResponse{Error: "invalid JSON body"})
		return
	}

	if input.PlayerID == "" || input.ItemName == "" || input.Price <= 0 {
		writeJSON(w, http.StatusBadRequest, errorResponse{Error: "player_id, item_name, and positive price are required"})
		return
	}

	req := service.PurchaseRequest{
		IdempotencyKey: idempotencyKey,
		PlayerID:       input.PlayerID,
		ItemName:       input.ItemName,
		Price:          input.Price,
	}

	resp, err := h.Service.Purchase(r.Context(), req)
	if err != nil {
		if errors.Is(err, repository.ErrConflict) {
			writeJSON(w, http.StatusConflict, errorResponse{Error: "balance version conflict, please retry"})
			return
		}
		writeJSON(w, http.StatusInternalServerError, errorResponse{Error: err.Error()})
		return
	}

	writeJSON(w, http.StatusOK, resp)
}

// writeJSON encodes v as JSON and writes it to w.
func writeJSON(w http.ResponseWriter, status int, v interface{}) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(v)
}
