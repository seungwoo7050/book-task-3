package log

import (
	"os"
	"testing"
)

func TestStoreAppendRead(t *testing.T) {
	f, err := os.CreateTemp("", "store_test")
	if err != nil {
		t.Fatal(err)
	}
	defer os.Remove(f.Name())

	s, err := newStore(f)
	if err != nil {
		t.Fatal(err)
	}
	defer s.Close()

	testCases := []struct {
		data []byte
	}{
		{data: []byte("hello")},
		{data: []byte("world")},
		{data: []byte("")},
		{data: []byte("a longer record with more data to store in the log")},
	}

	var positions []uint64
	for _, tc := range testCases {
		n, pos, err := s.Append(tc.data)
		if err != nil {
			t.Fatalf("Append(%q): %v", tc.data, err)
		}
		if n != uint64(len(tc.data))+lenWidth {
			t.Errorf("Append(%q): got n=%d, want %d", tc.data, n, uint64(len(tc.data))+lenWidth)
		}
		positions = append(positions, pos)
	}

	for i, tc := range testCases {
		got, err := s.Read(positions[i])
		if err != nil {
			t.Fatalf("Read(pos=%d): %v", positions[i], err)
		}
		if string(got) != string(tc.data) {
			t.Errorf("Read(pos=%d): got %q, want %q", positions[i], got, tc.data)
		}
	}
}

func TestStoreReopen(t *testing.T) {
	f, err := os.CreateTemp("", "store_reopen_test")
	if err != nil {
		t.Fatal(err)
	}
	name := f.Name()
	defer os.Remove(name)

	s, err := newStore(f)
	if err != nil {
		t.Fatal(err)
	}

	_, _, err = s.Append([]byte("first"))
	if err != nil {
		t.Fatal(err)
	}
	if err := s.Close(); err != nil {
		t.Fatal(err)
	}
	f2, err := os.OpenFile(name, os.O_RDWR|os.O_APPEND, 0644)
	if err != nil {
		t.Fatal(err)
	}
	s2, err := newStore(f2)
	if err != nil {
		t.Fatal(err)
	}
	defer s2.Close()
	if s2.Size() != lenWidth+5 { // 8 + len("first")
		t.Errorf("reopened store size = %d, want %d", s2.Size(), lenWidth+5)
	}
	got, err := s2.Read(0)
	if err != nil {
		t.Fatal(err)
	}
	if string(got) != "first" {
		t.Errorf("Read after reopen: got %q, want %q", got, "first")
	}
	_, pos, err := s2.Append([]byte("second"))
	if err != nil {
		t.Fatal(err)
	}
	got2, err := s2.Read(pos)
	if err != nil {
		t.Fatal(err)
	}
	if string(got2) != "second" {
		t.Errorf("Read after second append: got %q, want %q", got2, "second")
	}
}

func BenchmarkStoreAppend(b *testing.B) {
	f, err := os.CreateTemp("", "store_bench")
	if err != nil {
		b.Fatal(err)
	}
	defer os.Remove(f.Name())

	s, err := newStore(f)
	if err != nil {
		b.Fatal(err)
	}
	defer s.Close()

	data := make([]byte, 256)
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_, _, err := s.Append(data)
		if err != nil {
			b.Fatal(err)
		}
	}
}
