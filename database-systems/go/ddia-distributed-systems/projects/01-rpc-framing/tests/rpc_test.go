package tests

import (
	"context"
	"encoding/json"
	"errors"
	"sync"
	"testing"
	"time"

	"study.local/go/ddia-distributed-systems/projects/01-rpc-framing/internal/framing"
	"study.local/go/ddia-distributed-systems/projects/01-rpc-framing/internal/rpc"
)

func TestDecoderHandlesSingleMessage(t *testing.T) {
	frame, err := framing.Encode(map[string]any{"method": "ping"})
	if err != nil {
		t.Fatal(err)
	}
	decoder := &framing.Decoder{}
	payloads, err := decoder.Feed(frame)
	if err != nil {
		t.Fatal(err)
	}
	if len(payloads) != 1 {
		t.Fatalf("expected 1 payload, got %d", len(payloads))
	}
}

func TestDecoderHandlesSplitChunks(t *testing.T) {
	frame, err := framing.Encode(map[string]any{"hello": "world"})
	if err != nil {
		t.Fatal(err)
	}
	decoder := &framing.Decoder{}
	half := len(frame) / 2
	if payloads, err := decoder.Feed(frame[:half]); err != nil || len(payloads) != 0 {
		t.Fatalf("expected no message on first half, got %d err=%v", len(payloads), err)
	}
	payloads, err := decoder.Feed(frame[half:])
	if err != nil || len(payloads) != 1 {
		t.Fatalf("expected final payload, got %d err=%v", len(payloads), err)
	}
}

func TestRPCServerClientRoundTrip(t *testing.T) {
	server := rpc.NewServer("127.0.0.1:0")
	server.Register("echo", func(_ context.Context, params json.RawMessage) (any, error) {
		var payload map[string]string
		if err := json.Unmarshal(params, &payload); err != nil {
			return nil, err
		}
		return payload, nil
	})
	if err := server.Start(); err != nil {
		t.Fatal(err)
	}
	defer server.Close()

	client := rpc.NewClient(server.Addr())
	if err := client.Connect(); err != nil {
		t.Fatal(err)
	}
	defer client.Close()

	var result map[string]string
	if err := client.Call(context.Background(), "echo", map[string]string{"msg": "hello"}, &result); err != nil {
		t.Fatal(err)
	}
	if result["msg"] != "hello" {
		t.Fatalf("unexpected result %+v", result)
	}
}

func TestRPCHandlesConcurrentCalls(t *testing.T) {
	server := rpc.NewServer("127.0.0.1:0")
	server.Register("add", func(_ context.Context, params json.RawMessage) (any, error) {
		var payload struct {
			A int `json:"a"`
			B int `json:"b"`
		}
		if err := json.Unmarshal(params, &payload); err != nil {
			return nil, err
		}
		return map[string]int{"sum": payload.A + payload.B}, nil
	})
	if err := server.Start(); err != nil {
		t.Fatal(err)
	}
	defer server.Close()

	client := rpc.NewClient(server.Addr())
	if err := client.Connect(); err != nil {
		t.Fatal(err)
	}
	defer client.Close()

	sums := make([]int, 3)
	wg := sync.WaitGroup{}
	for i, pair := range [][2]int{{1, 2}, {10, 20}, {100, 200}} {
		wg.Add(1)
		go func(index int, a int, b int) {
			defer wg.Done()
			var result map[string]int
			if err := client.Call(context.Background(), "add", map[string]int{"a": a, "b": b}, &result); err != nil {
				t.Errorf("call failed: %v", err)
				return
			}
			sums[index] = result["sum"]
		}(i, pair[0], pair[1])
	}
	wg.Wait()

	if sums[0] != 3 || sums[1] != 30 || sums[2] != 300 {
		t.Fatalf("unexpected sums: %+v", sums)
	}
}

func TestRPCPropagatesServerErrorsAndTimeout(t *testing.T) {
	server := rpc.NewServer("127.0.0.1:0")
	server.Register("fail", func(_ context.Context, _ json.RawMessage) (any, error) {
		return nil, errors.New("intentional failure")
	})
	server.Register("slow", func(_ context.Context, _ json.RawMessage) (any, error) {
		time.Sleep(200 * time.Millisecond)
		return map[string]string{"status": "done"}, nil
	})
	if err := server.Start(); err != nil {
		t.Fatal(err)
	}
	defer server.Close()

	client := rpc.NewClient(server.Addr())
	if err := client.Connect(); err != nil {
		t.Fatal(err)
	}
	defer client.Close()

	if err := client.Call(context.Background(), "fail", map[string]string{}, nil); err == nil {
		t.Fatalf("expected server error")
	}

	ctx, cancel := context.WithTimeout(context.Background(), 20*time.Millisecond)
	defer cancel()
	if err := client.Call(ctx, "slow", map[string]string{}, nil); err == nil {
		t.Fatalf("expected timeout")
	}
}
