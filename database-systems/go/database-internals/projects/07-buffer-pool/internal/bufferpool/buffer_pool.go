package bufferpool

import (
	"errors"
	"path/filepath"
	"strconv"
	"strings"

	"study.local/go/database-internals/projects/07-buffer-pool/internal/lrucache"
	"study.local/go/shared/fileio"
)

const DefaultPageSize = 4096

type Page struct {
	PageID   string
	Data     []byte
	Dirty    bool
	PinCount int
}

type BufferPool struct {
	maxPages    int
	pageSize    int
	cache       *lrucache.LRUCache
	fileHandles map[string]*fileio.FileHandle
}

func New(maxPages, pageSize int) *BufferPool {
	if pageSize == 0 {
		pageSize = DefaultPageSize
	}
	return &BufferPool{
		maxPages:    maxPages,
		pageSize:    pageSize,
		cache:       lrucache.New(maxPages),
		fileHandles: map[string]*fileio.FileHandle{},
	}
}

func (pool *BufferPool) FetchPage(pageID string) (*Page, error) {
	if cached := pool.cache.Get(pageID); cached != nil {
		page := cached.(*Page)
		page.PinCount++
		return page, nil
	}

	filePath, pageNumber, err := parsePageID(pageID)
	if err != nil {
		return nil, err
	}
	handle, err := pool.getHandle(filePath)
	if err != nil {
		return nil, err
	}

	data, err := handle.ReadAt(int64(pageNumber*pool.pageSize), pool.pageSize)
	if err != nil {
		return nil, err
	}
	page := &Page{PageID: pageID, Data: data, PinCount: 1}

	if evicted := pool.cache.Put(pageID, page); evicted != nil {
		evictedPage := evicted.Value.(*Page)
		if evictedPage.PinCount > 0 {
			pool.cache.Put(evicted.Key, evictedPage)
			return nil, errors.New("bufferpool: cannot evict pinned page")
		}
		if evictedPage.Dirty {
			if err := pool.writePage(evictedPage); err != nil {
				return nil, err
			}
		}
	}

	return page, nil
}

func (pool *BufferPool) UnpinPage(pageID string, isDirty bool) {
	cached := pool.cache.Get(pageID)
	if cached == nil {
		return
	}
	page := cached.(*Page)
	if page.PinCount > 0 {
		page.PinCount--
	}
	if isDirty {
		page.Dirty = true
	}
}

func (pool *BufferPool) FlushPage(pageID string) error {
	cached := pool.cache.Get(pageID)
	if cached == nil {
		return nil
	}
	page := cached.(*Page)
	if !page.Dirty {
		return nil
	}
	if err := pool.writePage(page); err != nil {
		return err
	}
	page.Dirty = false
	return nil
}

func (pool *BufferPool) FlushAll() error {
	for _, key := range pool.cache.Keys() {
		if err := pool.FlushPage(key); err != nil {
			return err
		}
	}
	return nil
}

func (pool *BufferPool) Close() error {
	if err := pool.FlushAll(); err != nil {
		return err
	}
	for _, handle := range pool.fileHandles {
		if err := handle.Close(); err != nil {
			return err
		}
	}
	pool.fileHandles = map[string]*fileio.FileHandle{}
	return nil
}

func (pool *BufferPool) getHandle(filePath string) (*fileio.FileHandle, error) {
	if handle := pool.fileHandles[filePath]; handle != nil {
		return handle, nil
	}

	handle := fileio.NewHandle(filePath)
	if err := handle.Open("r+"); err != nil {
		return nil, err
	}
	pool.fileHandles[filePath] = handle
	return handle, nil
}

func (pool *BufferPool) writePage(page *Page) error {
	filePath, pageNumber, err := parsePageID(page.PageID)
	if err != nil {
		return err
	}
	handle, err := pool.getHandle(filePath)
	if err != nil {
		return err
	}
	if _, err := handle.WriteAt(page.Data, int64(pageNumber*pool.pageSize)); err != nil {
		return err
	}
	return handle.Sync()
}

func parsePageID(pageID string) (string, int, error) {
	lastColon := strings.LastIndex(pageID, ":")
	if lastColon == -1 {
		return "", 0, errors.New("bufferpool: invalid page id")
	}
	filePath := filepath.Clean(pageID[:lastColon])
	pageNumber, err := strconv.Atoi(pageID[lastColon+1:])
	if err != nil {
		return "", 0, err
	}
	return filePath, pageNumber, nil
}
