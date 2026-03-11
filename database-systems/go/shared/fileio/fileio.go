package fileio

import (
	"errors"
	"io"
	"os"
	"path/filepath"
	"slices"
)

// FileHandle은 학습용 모듈 전반에서 쓰는 최소한의 os.File 표면을 감싼다.
type FileHandle struct {
	path string
	file *os.File
}

// NewHandle은 특정 path에 연결된 handle을 반환한다.
func NewHandle(path string) *FileHandle {
	return &FileHandle{path: path}
}

// Path는 실제 파일 경로를 반환한다.
func (handle *FileHandle) Path() string {
	return handle.path
}

// Open은 r, w, a, r+, w+, a+ 같은 Node-style flag로 파일을 연다.
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

// Append는 현재 end-of-file 위치에 byte를 쓴다.
func (handle *FileHandle) Append(data []byte) (int, error) {
	if handle.file == nil {
		return 0, errors.New("fileio: append on closed handle")
	}
	return handle.file.Write(data)
}

// WriteAt은 절대 위치에 byte를 쓴다.
func (handle *FileHandle) WriteAt(data []byte, position int64) (int, error) {
	if handle.file == nil {
		return 0, errors.New("fileio: writeAt on closed handle")
	}
	return handle.file.WriteAt(data, position)
}

// ReadAt은 절대 위치에서 length byte까지 읽는다.
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

// ReadAll은 파일 전체 내용을 반환한다.
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

// Sync는 buffered write를 디스크에 fsync한다.
func (handle *FileHandle) Sync() error {
	if handle.file == nil {
		return errors.New("fileio: sync on closed handle")
	}
	return handle.file.Sync()
}

// Size는 현재 파일 크기를 반환한다.
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

// Close는 file descriptor를 닫는다.
func (handle *FileHandle) Close() error {
	if handle.file == nil {
		return nil
	}
	err := handle.file.Close()
	handle.file = nil
	return err
}

// EnsureDir는 디렉터리가 없으면 필요한 경로를 만든다.
func EnsureDir(path string) error {
	return os.MkdirAll(path, 0o755)
}

// ListFiles는 suffix 조건을 적용해 정렬된 파일 이름 목록을 반환한다.
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

// AtomicWrite는 같은 디렉터리의 temp file에 쓴 뒤 rename으로 교체한다.
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

// RemoveFile은 파일이 존재할 때만 제거한다.
func RemoveFile(path string) error {
	err := os.Remove(path)
	if err != nil && !errors.Is(err, os.ErrNotExist) {
		return err
	}
	return nil
}

// FileSize는 파일을 열어 둔 채 유지하지 않고 크기만 조회한다.
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
