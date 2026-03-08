package platform

import (
	"fmt"
	"net/http"
	"sync/atomic"
)

// Metrics stores process-local counters exposed through /metrics.
type Metrics struct {
	requestsTotal         atomic.Int64
	authLoginsTotal       atomic.Int64
	dashboardCacheHits    atomic.Int64
	dashboardCacheMisses  atomic.Int64
	workerProcessedEvents atomic.Int64
}

func (m *Metrics) IncRequests() {
	m.requestsTotal.Add(1)
}

func (m *Metrics) IncAuthLogins() {
	m.authLoginsTotal.Add(1)
}

func (m *Metrics) IncDashboardCacheHit() {
	m.dashboardCacheHits.Add(1)
}

func (m *Metrics) IncDashboardCacheMiss() {
	m.dashboardCacheMisses.Add(1)
}

func (m *Metrics) AddWorkerProcessed(count int) {
	m.workerProcessedEvents.Add(int64(count))
}

// Handler exposes metrics in Prometheus text format.
func (m *Metrics) Handler(w http.ResponseWriter, _ *http.Request) {
	w.Header().Set("Content-Type", "text/plain; version=0.0.4")
	_, _ = fmt.Fprintf(
		w,
		"workspace_requests_total %d\nworkspace_auth_logins_total %d\nworkspace_dashboard_cache_hits_total %d\nworkspace_dashboard_cache_misses_total %d\nworkspace_worker_processed_events_total %d\n",
		m.requestsTotal.Load(),
		m.authLoginsTotal.Load(),
		m.dashboardCacheHits.Load(),
		m.dashboardCacheMisses.Load(),
		m.workerProcessedEvents.Load(),
	)
}
