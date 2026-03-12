package analyzer

import (
	"fmt"
	"strconv"
	"strings"
	"sync"
)

type Event struct {
	Category   string
	DurationMS int
}

type Summary struct {
	Count     int
	TotalMS   int
	AverageMS int
}

type Recorder struct {
	mu     sync.Mutex
	events []Event
}

func ParseLine(line string) (Event, error) {
	parts := strings.Split(line, ",")
	if len(parts) != 2 {
		return Event{}, fmt.Errorf("invalid line %q", line)
	}
	duration, err := strconv.Atoi(strings.TrimSpace(parts[1]))
	if err != nil {
		return Event{}, fmt.Errorf("invalid duration: %w", err)
	}
	category := strings.TrimSpace(parts[0])
	if category == "" {
		return Event{}, fmt.Errorf("empty category")
	}
	return Event{Category: category, DurationMS: duration}, nil
}

func Summarize(lines []string) (map[string]Summary, error) {
	summaries := make(map[string]Summary)
	for _, line := range lines {
		event, err := ParseLine(line)
		if err != nil {
			return nil, err
		}
		summary := summaries[event.Category]
		summary.Count++
		summary.TotalMS += event.DurationMS
		summary.AverageMS = summary.TotalMS / summary.Count
		summaries[event.Category] = summary
	}
	return summaries, nil
}

func (r *Recorder) Add(event Event) {
	r.mu.Lock()
	defer r.mu.Unlock()
	r.events = append(r.events, event)
}

func (r *Recorder) Snapshot() []Event {
	r.mu.Lock()
	defer r.mu.Unlock()
	out := make([]Event, len(r.events))
	copy(out, r.events)
	return out
}
