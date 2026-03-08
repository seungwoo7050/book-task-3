package httpapi

import (
	"database/sql"
	"encoding/json"
	"errors"
	"log/slog"
	"net/http"

	"github.com/woopinbell/go-backend/study/04-capstone/17-game-store-capstone/internal/repository"
	"github.com/woopinbell/go-backend/study/04-capstone/17-game-store-capstone/internal/service"
)

// API wires HTTP handlers to services.
type API struct {
	purchaseService *service.PurchaseService
	queryService    *service.QueryService
	logger          *slog.Logger
	limiter         *RateLimiter
}

// NewAPI creates API handlers.
func NewAPI(
	purchaseService *service.PurchaseService,
	queryService *service.QueryService,
	logger *slog.Logger,
	rateLimitRPS int,
) *API {
	var limiter *RateLimiter
	if rateLimitRPS > 0 {
		limiter = NewRateLimiter(rateLimitRPS)
	}

	return &API{
		purchaseService: purchaseService,
		queryService:    queryService,
		logger:          logger,
		limiter:         limiter,
	}
}

// Routes builds the API router with middleware.
func (a *API) Routes() http.Handler {
	mux := http.NewServeMux()
	mux.HandleFunc("GET /v1/healthcheck", a.handleHealthcheck)
	mux.HandleFunc("POST /v1/purchases", a.handleCreatePurchase)
	mux.HandleFunc("GET /v1/purchases/{id}", a.handleGetPurchase)
	mux.HandleFunc("GET /v1/players/{id}/inventory", a.handleGetInventory)

	var handler http.Handler = mux
	handler = rateLimitMiddleware(handler, a.limiter)
	handler = loggingMiddleware(handler, a.logger)
	return handler
}

func (a *API) handleHealthcheck(w http.ResponseWriter, r *http.Request) {
	writeJSON(w, http.StatusOK, map[string]string{"status": "ok"})
}

type createPurchaseInput struct {
	PlayerID string `json:"player_id"`
	ItemID   string `json:"item_id"`
}

func (a *API) handleCreatePurchase(w http.ResponseWriter, r *http.Request) {
	idempotencyKey := r.Header.Get("Idempotency-Key")
	if idempotencyKey == "" {
		writeJSON(w, http.StatusBadRequest, map[string]string{
			"error": "Idempotency-Key header is required",
		})
		return
	}

	var input createPurchaseInput
	decoder := json.NewDecoder(r.Body)
	decoder.DisallowUnknownFields()
	if err := decoder.Decode(&input); err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid request body"})
		return
	}

	resp, err := a.purchaseService.Purchase(r.Context(), service.PurchaseRequest{
		PlayerID:       input.PlayerID,
		ItemID:         input.ItemID,
		IdempotencyKey: idempotencyKey,
	})
	if err != nil {
		var validationErr *service.ValidationError
		status := http.StatusInternalServerError
		switch {
		case errors.As(err, &validationErr):
			status = http.StatusBadRequest
		case errors.Is(err, service.ErrPlayerNotFound), errors.Is(err, service.ErrItemNotFound):
			status = http.StatusNotFound
		case errors.Is(err, service.ErrInsufficientBalance):
			status = http.StatusConflict
		case errors.Is(err, repository.ErrConflict):
			status = http.StatusConflict
		case errors.Is(err, service.ErrIdempotencyKeyConflict):
			status = http.StatusConflict
		}
		writeJSON(w, status, map[string]string{"error": err.Error()})
		return
	}

	writeJSON(w, http.StatusOK, resp)
}

func (a *API) handleGetPurchase(w http.ResponseWriter, r *http.Request) {
	purchaseID := r.PathValue("id")
	purchase, err := a.queryService.GetPurchase(r.Context(), purchaseID)
	if err != nil {
		status := http.StatusInternalServerError
		switch {
		case errors.Is(err, service.ErrPurchaseIDRequired):
			status = http.StatusBadRequest
		case errors.Is(err, sql.ErrNoRows):
			status = http.StatusNotFound
		}
		writeJSON(w, status, map[string]string{"error": err.Error()})
		return
	}
	writeJSON(w, http.StatusOK, purchase)
}

func (a *API) handleGetInventory(w http.ResponseWriter, r *http.Request) {
	playerID := r.PathValue("id")
	items, err := a.queryService.GetInventory(r.Context(), playerID)
	if err != nil {
		status := http.StatusInternalServerError
		if errors.Is(err, service.ErrPlayerIDRequired) {
			status = http.StatusBadRequest
		}
		writeJSON(w, status, map[string]string{"error": err.Error()})
		return
	}

	writeJSON(w, http.StatusOK, map[string]any{
		"player_id": playerID,
		"items":     items,
	})
}

func writeJSON(w http.ResponseWriter, status int, body any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	enc := json.NewEncoder(w)
	enc.SetEscapeHTML(false)
	_ = enc.Encode(body)
}
