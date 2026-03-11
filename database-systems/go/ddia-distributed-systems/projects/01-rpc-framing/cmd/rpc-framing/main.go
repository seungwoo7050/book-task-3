package main

import (
	"context"
	"encoding/json"
	"fmt"

	"study.local/go/ddia-distributed-systems/projects/01-rpc-framing/internal/rpc"
)

func main() {
	server := rpc.NewServer("127.0.0.1:0")
	server.Register("ping", func(_ context.Context, params json.RawMessage) (any, error) {
		var payload map[string]string
		_ = json.Unmarshal(params, &payload)
		return map[string]string{"reply": "pong:" + payload["msg"]}, nil
	})
	if err := server.Start(); err != nil {
		panic(err)
	}
	defer server.Close()

	client := rpc.NewClient(server.Addr())
	if err := client.Connect(); err != nil {
		panic(err)
	}
	defer client.Close()

	var result map[string]string
	if err := client.Call(context.Background(), "ping", map[string]string{"msg": "hello"}, &result); err != nil {
		panic(err)
	}
	fmt.Println(result["reply"])
}
