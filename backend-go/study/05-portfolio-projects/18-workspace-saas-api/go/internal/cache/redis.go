package cache

import (
	"context"
	"errors"
	"time"

	"github.com/redis/go-redis/v9"
)

var (
	// ErrUnavailable indicates Redis could not be reached.
	ErrUnavailable = errors.New("redis unavailable")
	// ErrNotFound indicates requested Redis key is absent.
	ErrNotFound = errors.New("redis key not found")
)

// Client wraps Redis operations for refresh sessions and dashboard cache.
type Client struct {
	rdb *redis.Client
}

// New creates a Redis client.
func New(addr, password string, db int) *Client {
	return &Client{
		rdb: redis.NewClient(&redis.Options{
			Addr:     addr,
			Password: password,
			DB:       db,
		}),
	}
}

// Ping checks whether Redis is reachable.
func (c *Client) Ping(ctx context.Context) error {
	if err := c.rdb.Ping(ctx).Err(); err != nil {
		return mapError(err)
	}
	return nil
}

// SetRefreshSession stores refresh-session state.
func (c *Client) SetRefreshSession(ctx context.Context, sessionID, tokenHash string, ttl time.Duration) error {
	return mapError(c.rdb.Set(ctx, refreshKey(sessionID), tokenHash, ttl).Err())
}

// GetRefreshSessionHash fetches refresh-session token hash.
func (c *Client) GetRefreshSessionHash(ctx context.Context, sessionID string) (string, error) {
	value, err := c.rdb.Get(ctx, refreshKey(sessionID)).Result()
	if err != nil {
		return "", mapError(err)
	}
	return value, nil
}

// DeleteRefreshSession removes refresh-session state.
func (c *Client) DeleteRefreshSession(ctx context.Context, sessionID string) error {
	return mapError(c.rdb.Del(ctx, refreshKey(sessionID)).Err())
}

// GetDashboardSummary reads a cached summary payload.
func (c *Client) GetDashboardSummary(ctx context.Context, organizationID string) ([]byte, error) {
	value, err := c.rdb.Get(ctx, dashboardKey(organizationID)).Bytes()
	if err != nil {
		return nil, mapError(err)
	}
	return value, nil
}

// SetDashboardSummary writes a cached summary payload.
func (c *Client) SetDashboardSummary(ctx context.Context, organizationID string, payload []byte, ttl time.Duration) error {
	return mapError(c.rdb.Set(ctx, dashboardKey(organizationID), payload, ttl).Err())
}

// DeleteDashboardSummary removes a cached summary payload.
func (c *Client) DeleteDashboardSummary(ctx context.Context, organizationID string) error {
	return mapError(c.rdb.Del(ctx, dashboardKey(organizationID)).Err())
}

func refreshKey(sessionID string) string {
	return "workspace-saas:refresh:" + sessionID
}

func dashboardKey(organizationID string) string {
	return "workspace-saas:dashboard:" + organizationID
}

func mapError(err error) error {
	switch {
	case err == nil:
		return nil
	case errors.Is(err, redis.Nil):
		return ErrNotFound
	default:
		return ErrUnavailable
	}
}
