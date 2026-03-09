package fileio

import (
	"errors"
	"io"
	"os"
	"path/filepath"
	"slices"
)

// FileHandle wraps os.File with the minimal surface used across study modules.
type FileHandle struct {
	path string
	file *os.File
}

// NewHandle returns a handle bound to a path.
func NewHandle(path string) *FileHandle {
	return &FileHandle{path: path}
}

// Path returns the underlying file path.
func (handle *FileHandle) Path() string {
	return handle.path
}

// Open opens the file using Node-like flags such as r, w, a, r+, w+, a+.
func (handle *FileHandle) Open(flags string) error {
	if err := EnsureDir(filepath.Dir(handle.path)); err != nil {
		return err
	}

	goFlags, perm, err := parseFlags(flags)
	if err != nil {
		return err
	}

	file, err := os.OpenFile(handle.path, goFlags, perm)
	if err != nil {
		return err
	}
	handle.file = file
	return nil
}

// Append writes bytes at the current end-of-file.
func (handle *FileHandle) Append(data []byte) (int, error) {
	if handle.file == nil {
		return 0, errors.New("fileio: append on closed handle")
	}
	return handle.file.Write(data)
}

// WriteAt writes bytes at an absolute position.
func (handle *FileHandle) WriteAt(data []byte, position int64) (int, error) {
	if handle.file == nil {
		return 0, errors.New("fileio: writeAt on closed handle")
	}
	return handle.file.WriteAt(data, position)
}

// ReadAt reads up to length bytes at an absolute position.
func (handle *FileHandle) ReadAt(position int64, length int) ([]byte, error) {
	if handle.file == nil {
		return nil, errors.New("fileio: readAt on closed handle")
	}

	buffer := make([]byte, length)
	bytesRead, err := handle.file.ReadAt(buffer, position)
	if err != nil && !errors.Is(err, io.EOF) {
		return nil, err
	}
	return buffer[:bytesRead], nil
}

// ReadAll returns the full file contents.
func (handle *FileHandle) ReadAll() ([]byte, error) {
	size, err := handle.Size()
	if err != nil {
		return nil, err
	}
	if size == 0 {
		return []byte{}, nil
	}
	return handle.ReadAt(0, int(size))
}

// Sync fsyncs buffered writes to disk.
func (handle *FileHandle) Sync() error {
	if handle.file == nil {
		return errors.New("fileio: sync on closed handle")
	}
	return handle.file.Sync()
}

// Size returns the current file size.
func (handle *FileHandle) Size() (int64, error) {
	if handle.file == nil {
		return 0, errors.New("fileio: size on closed handle")
	}
	info, err := handle.file.Stat()
	if err != nil {
		return 0, err
	}
	return info.Size(), nil
}

// Close closes the file descriptor.
func (handle *FileHandle) Close() error {
	if handle.file == nil {
		return nil
	}
	err := handle.file.Close()
	handle.file = nil
	return err
}

// EnsureDir creates a directory tree if it does not exist.
func EnsureDir(path string) error {
	return os.MkdirAll(path, 0o755)
}

// ListFiles returns sorted file names, optionally filtered by suffix.
func ListFiles(path string, suffix string) ([]string, error) {
	entries, err := os.ReadDir(path)
	if err != nil {
		if errors.Is(err, os.ErrNotExist) {
			return []string{}, nil
		}
		return nil, err
	}

	files := make([]string, 0, len(entries))
	for _, entry := range entries {
		if entry.IsDir() {
			continue
		}
		if suffix != "" && filepath.Ext(entry.Name()) != suffix {
			continue
		}
		files = append(files, entry.Name())
	}
	slices.Sort(files)
	return files, nil
}

// AtomicWrite writes data through a sibling temp file and renames it into place.
func AtomicWrite(path string, data []byte) error {
	if err := EnsureDir(filepath.Dir(path)); err != nil {
		return err
	}

	temp, err := os.CreateTemp(filepath.Dir(path), ".tmp-*")
	if err != nil {
		return err
	}
	tempPath := temp.Name()
	defer os.Remove(tempPath)

	if _, err := temp.Write(data); err != nil {
		temp.Close()
		return err
	}
	if err := temp.Sync(); err != nil {
		temp.Close()
		return err
	}
	if err := temp.Close(); err != nil {
		return err
	}
	return os.Rename(tempPath, path)
}

// RemoveFile removes a file if it exists.
func RemoveFile(path string) error {
	err := os.Remove(path)
	if err != nil && !errors.Is(err, os.ErrNotExist) {
		return err
	}
	return nil
}

// FileSize returns file size without keeping the file open.
func FileSize(path string) (int64, error) {
	info, err := os.Stat(path)
	if err != nil {
		return 0, err
	}
	return info.Size(), nil
}

func parseFlags(flags string) (int, os.FileMode, error) {
	switch flags {
	case "r":
		return os.O_RDONLY, 0o644, nil
	case "w":
		return os.O_CREATE | os.O_WRONLY | os.O_TRUNC, 0o644, nil
	case "a":
		return os.O_CREATE | os.O_WRONLY | os.O_APPEND, 0o644, nil
	case "r+":
		return os.O_RDWR, 0o644, nil
	case "w+":
		return os.O_CREATE | os.O_RDWR | os.O_TRUNC, 0o644, nil
	case "a+":
		return os.O_CREATE | os.O_RDWR | os.O_APPEND, 0o644, nil
	default:
		return 0, 0, errors.New("fileio: unsupported flag set")
	}
}
