package handler

import (
	"encoding/json"
	"errors"
	"net/http"

	"github.com/woopinbell/go-backend/study/03-platform-engineering/14-cockroach-tx/repository"
	"github.com/woopinbell/go-backend/study/03-platform-engineering/14-cockroach-tx/service"
)

type PurchaseHandler struct {
	Service *service.PurchaseService
}
type purchaseInput struct {
	PlayerID string `json:"player_id"`
	ItemName string `json:"item_name"`
	Price    int64  `json:"price"`
}
type errorResponse struct {
	Error string `json:"error"`
}

func (h *PurchaseHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		writeJSON(w, http.StatusMethodNotAllowed, errorResponse{Error: "method not allowed"})
		return
	}
	idempotencyKey := r.Header.Get("Idempotency-Key")
	if idempotencyKey == "" {
		writeJSON(w, http.StatusBadRequest, errorResponse{Error: "Idempotency-Key header is required"})
		return
	}
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
func writeJSON(w http.ResponseWriter, status int, v interface{}) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(v)
}
