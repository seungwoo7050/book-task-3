package main

import (
	"fmt"
	"log/slog"
	"os"
)

func main() {
	logger := slog.New(slog.NewTextHandler(os.Stdout, nil))

	logger.Info("TODO: implement the server")
	fmt.Println("starter skeleton — replace this with your implementation")
	os.Exit(0)
}
