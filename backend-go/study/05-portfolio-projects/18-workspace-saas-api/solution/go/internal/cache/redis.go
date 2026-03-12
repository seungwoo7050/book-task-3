package cache

import (
	"context"
	"errors"
	"time"

	"github.com/redis/go-redis/v9"
)

var (
	// ErrUnavailable은 Redis 연결 또는 명령 수행에 실패했을 때 반환된다.
	ErrUnavailable = errors.New("redis unavailable")
	// ErrNotFound는 요청한 Redis 키가 없을 때 반환된다.
	ErrNotFound = errors.New("redis key not found")
)

// Client는 refresh session과 dashboard summary를 Redis에 저장한다.
type Client struct {
	rdb *redis.Client
}

// New는 Redis 클라이언트를 생성한다.
func New(addr, password string, db int) *Client {
	return &Client{
		rdb: redis.NewClient(&redis.Options{
			Addr:     addr,
			Password: password,
			DB:       db,
		}),
	}
}

// Ping은 Redis 연결 가능 여부를 확인한다.
func (c *Client) Ping(ctx context.Context) error {
	if err := c.rdb.Ping(ctx).Err(); err != nil {
		return mapError(err)
	}
	return nil
}

// SetRefreshSession은 refresh session 해시를 Redis에 저장한다.
func (c *Client) SetRefreshSession(ctx context.Context, sessionID, tokenHash string, ttl time.Duration) error {
	return mapError(c.rdb.Set(ctx, refreshKey(sessionID), tokenHash, ttl).Err())
}

// GetRefreshSessionHash는 저장된 refresh session 해시를 읽는다.
func (c *Client) GetRefreshSessionHash(ctx context.Context, sessionID string) (string, error) {
	value, err := c.rdb.Get(ctx, refreshKey(sessionID)).Result()
	if err != nil {
		return "", mapError(err)
	}
	return value, nil
}

// DeleteRefreshSession은 refresh session 키를 삭제한다.
func (c *Client) DeleteRefreshSession(ctx context.Context, sessionID string) error {
	return mapError(c.rdb.Del(ctx, refreshKey(sessionID)).Err())
}

// GetDashboardSummary는 캐시된 대시보드 요약을 읽는다.
func (c *Client) GetDashboardSummary(ctx context.Context, organizationID string) ([]byte, error) {
	value, err := c.rdb.Get(ctx, dashboardKey(organizationID)).Bytes()
	if err != nil {
		return nil, mapError(err)
	}
	return value, nil
}

// SetDashboardSummary는 대시보드 요약 페이로드를 캐시에 저장한다.
func (c *Client) SetDashboardSummary(ctx context.Context, organizationID string, payload []byte, ttl time.Duration) error {
	return mapError(c.rdb.Set(ctx, dashboardKey(organizationID), payload, ttl).Err())
}

// DeleteDashboardSummary는 대시보드 캐시를 무효화한다.
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
