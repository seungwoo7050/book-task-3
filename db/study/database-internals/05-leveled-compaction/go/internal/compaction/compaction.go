package compaction

import (
	"encoding/json"
	"errors"
	"os"
	"path/filepath"

	"study.local/database-internals/05-leveled-compaction/internal/sstable"
	"study.local/shared/fileio"
	"study.local/shared/serializer"
)

type Result struct {
	Added             []string
	Removed           []string
	DroppedTombstones bool
}

type Manager struct {
	DataDir      string
	Levels       map[int][]string
	NextSequence int
	L0MaxFiles   int
	ManifestPath string
}

type manifest struct {
	Levels       map[int][]string `json:"levels"`
	NextSequence int              `json:"nextSequence"`
}

func New(dataDir string, l0MaxFiles int) *Manager {
	if l0MaxFiles == 0 {
		l0MaxFiles = 4
	}
	return &Manager{
		DataDir:      dataDir,
		Levels:       map[int][]string{0: {}},
		NextSequence: 1,
		L0MaxFiles:   l0MaxFiles,
		ManifestPath: filepath.Join(dataDir, "MANIFEST"),
	}
}

func (manager *Manager) AddToLevel(level int, fileName string) {
	manager.Levels[level] = append(manager.Levels[level], fileName)
}

func (manager *Manager) NeedsL0Compaction() bool {
	return len(manager.Levels[0]) >= manager.L0MaxFiles
}

func (manager *Manager) CompactL0ToL1() (Result, error) {
	l0Files := append([]string(nil), manager.Levels[0]...)
	if len(l0Files) == 0 {
		return Result{}, nil
	}

	l1Files := append([]string(nil), manager.Levels[1]...)
	sources := make([][]serializer.Record, 0, len(l0Files)+len(l1Files))

	for i := len(l0Files) - 1; i >= 0; i-- {
		records, err := readAll(filepath.Join(manager.DataDir, l0Files[i]))
		if err != nil {
			return Result{}, err
		}
		sources = append(sources, records)
	}

	for _, fileName := range l1Files {
		records, err := readAll(filepath.Join(manager.DataDir, fileName))
		if err != nil {
			return Result{}, err
		}
		sources = append(sources, records)
	}

	dropTombstones := len(manager.Levels[2]) == 0
	merged := KWayMerge(sources, dropTombstones)

	newFileName := sequenceFileName(manager.NextSequence)
	manager.NextSequence++
	output := sstable.New(filepath.Join(manager.DataDir, newFileName))
	if err := output.Write(merged); err != nil {
		return Result{}, err
	}

	removed := append(append([]string{}, l0Files...), l1Files...)
	manager.Levels[0] = []string{}
	manager.Levels[1] = []string{newFileName}

	if err := manager.SaveManifest(); err != nil {
		return Result{}, err
	}
	for _, fileName := range removed {
		if err := fileio.RemoveFile(filepath.Join(manager.DataDir, fileName)); err != nil {
			return Result{}, err
		}
	}

	return Result{
		Added:             []string{newFileName},
		Removed:           removed,
		DroppedTombstones: dropTombstones,
	}, nil
}

func (manager *Manager) SaveManifest() error {
	payload := manifest{
		Levels:       cloneLevels(manager.Levels),
		NextSequence: manager.NextSequence,
	}
	buffer, err := json.MarshalIndent(payload, "", "  ")
	if err != nil {
		return err
	}
	return fileio.AtomicWrite(manager.ManifestPath, buffer)
}

func (manager *Manager) LoadManifest() error {
	handle := fileio.NewHandle(manager.ManifestPath)
	if err := handle.Open("r"); err != nil {
		if filepath.ErrBadPattern == nil { // no-op to keep filepath imported on older toolchains
		}
		if isNotExist(err) {
			return nil
		}
		return err
	}
	defer handle.Close()

	buffer, err := handle.ReadAll()
	if err != nil {
		return err
	}
	var payload manifest
	if err := json.Unmarshal(buffer, &payload); err != nil {
		return err
	}

	manager.Levels = cloneLevels(payload.Levels)
	if manager.Levels[0] == nil {
		manager.Levels[0] = []string{}
	}
	manager.NextSequence = payload.NextSequence
	if manager.NextSequence == 0 {
		manager.NextSequence = 1
	}
	return nil
}

func KWayMerge(sources [][]serializer.Record, dropTombstones bool) []serializer.Record {
	if len(sources) == 0 {
		return []serializer.Record{}
	}
	merged := append([]serializer.Record(nil), sources[0]...)
	for i := 1; i < len(sources); i++ {
		merged = mergeTwo(merged, sources[i])
	}
	if !dropTombstones {
		return merged
	}

	filtered := make([]serializer.Record, 0, len(merged))
	for _, record := range merged {
		if record.Value != nil {
			filtered = append(filtered, record)
		}
	}
	return filtered
}

func mergeTwo(newer []serializer.Record, older []serializer.Record) []serializer.Record {
	merged := make([]serializer.Record, 0, len(newer)+len(older))
	i := 0
	j := 0
	for i < len(newer) && j < len(older) {
		switch {
		case newer[i].Key < older[j].Key:
			merged = append(merged, newer[i])
			i++
		case newer[i].Key > older[j].Key:
			merged = append(merged, older[j])
			j++
		default:
			merged = append(merged, newer[i])
			i++
			j++
		}
	}
	merged = append(merged, newer[i:]...)
	merged = append(merged, older[j:]...)
	return merged
}

func readAll(path string) ([]serializer.Record, error) {
	table := sstable.New(path)
	return table.ReadAll()
}

func sequenceFileName(sequence int) string {
	return filepath.Base(sstable.FileName(".", sequence))
}

func cloneLevels(levels map[int][]string) map[int][]string {
	cloned := make(map[int][]string, len(levels))
	for level, files := range levels {
		cloned[level] = append([]string(nil), files...)
	}
	return cloned
}

func isNotExist(err error) bool {
	return errors.Is(err, os.ErrNotExist)
}
