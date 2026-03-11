package main

import (
	"fmt"
	"os"
	"path/filepath"

	"study.local/go/database-internals/projects/07-buffer-pool/internal/bufferpool"
)

func main() {
	tempDir, err := os.MkdirTemp("", "buffer-pool-demo-")
	if err != nil {
		panic(err)
	}
	defer os.RemoveAll(tempDir)

	dataFile := filepath.Join(tempDir, "data.db")
	pages := make([]byte, 0, 3*64)
	for i := 0; i < 3; i++ {
		buffer := make([]byte, 64)
		copy(buffer, []byte(fmt.Sprintf("page-%d", i)))
		pages = append(pages, buffer...)
	}
	must(os.WriteFile(dataFile, pages, 0o644))

	pool := bufferpool.New(2, 64)
	page, err := pool.FetchPage(dataFile + ":1")
	must(err)
	fmt.Printf("%s\n", string(page.Data[:6]))
}

func must(err error) {
	if err != nil {
		panic(err)
	}
}
