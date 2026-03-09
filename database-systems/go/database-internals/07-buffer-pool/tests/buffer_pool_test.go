package tests

import (
	"os"
	"path/filepath"
	"testing"

	"study.local/database-internals/07-buffer-pool/internal/bufferpool"
)

func TestFetchPageFromDisk(t *testing.T) {
	dataFile := seedPages(t)
	pool := bufferpool.New(4, 64)

	page, err := pool.FetchPage(dataFile + ":0")
	if err != nil {
		t.Fatalf("fetch page: %v", err)
	}
	if page.PinCount != 1 || string(page.Data[:6]) != "page-0" {
		t.Fatalf("unexpected page: %+v", page)
	}
}

func TestReturnCachedPage(t *testing.T) {
	dataFile := seedPages(t)
	pool := bufferpool.New(4, 64)

	page1, err := pool.FetchPage(dataFile + ":2")
	if err != nil {
		t.Fatal(err)
	}
	pool.UnpinPage(dataFile+":2", false)
	page2, err := pool.FetchPage(dataFile + ":2")
	if err != nil {
		t.Fatal(err)
	}
	if page1 != page2 {
		t.Fatalf("expected same cached page instance")
	}
}

func TestTrackDirtyPages(t *testing.T) {
	dataFile := seedPages(t)
	pool := bufferpool.New(4, 64)

	page, err := pool.FetchPage(dataFile + ":0")
	if err != nil {
		t.Fatal(err)
	}
	copy(page.Data[:8], []byte("modified"))
	pool.UnpinPage(dataFile+":0", true)
	if !page.Dirty {
		t.Fatalf("expected dirty page")
	}
}

func TestEvictionAfterUnpin(t *testing.T) {
	dataFile := seedPages(t)
	pool := bufferpool.New(2, 64)

	page0, err := pool.FetchPage(dataFile + ":0")
	mustPage(t, page0, err)
	pool.UnpinPage(dataFile+":0", false)
	page1, err := pool.FetchPage(dataFile + ":1")
	mustPage(t, page1, err)
	pool.UnpinPage(dataFile+":1", false)

	page2, err := pool.FetchPage(dataFile + ":2")
	if err != nil {
		t.Fatal(err)
	}
	if string(page2.Data[:6]) != "page-2" {
		t.Fatalf("unexpected page content")
	}
}

func seedPages(t *testing.T) string {
	t.Helper()
	tempDir := t.TempDir()
	dataFile := filepath.Join(tempDir, "data.db")
	pages := make([]byte, 0, 10*64)
	for i := 0; i < 10; i++ {
		buffer := make([]byte, 64)
		copy(buffer, []byte("page-"+itoa(i)))
		pages = append(pages, buffer...)
	}
	if err := os.WriteFile(dataFile, pages, 0o644); err != nil {
		t.Fatalf("seed pages: %v", err)
	}
	return dataFile
}

func mustPage(t *testing.T, page *bufferpool.Page, err error) *bufferpool.Page {
	t.Helper()
	if err != nil {
		t.Fatalf("fetch page: %v", err)
	}
	return page
}

func itoa(value int) string {
	if value == 0 {
		return "0"
	}
	buffer := make([]byte, 0, 2)
	for value > 0 {
		buffer = append([]byte{byte('0' + value%10)}, buffer...)
		value /= 10
	}
	return string(buffer)
}
