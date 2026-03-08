package lesson

import (
	"sort"
	"strings"
	"unicode"
)

type Summary struct {
	TotalWords  int
	UniqueWords int
	TopWord     string
}

func NormalizeWords(text string) []string {
	fields := strings.FieldsFunc(strings.ToLower(text), func(r rune) bool {
		return !unicode.IsLetter(r) && !unicode.IsNumber(r)
	})
	words := make([]string, 0, len(fields))
	for _, field := range fields {
		if field == "" {
			continue
		}
		words = append(words, field)
	}
	return words
}

func CountWords(words []string) map[string]int {
	counts := make(map[string]int, len(words))
	for _, word := range words {
		counts[word]++
	}
	return counts
}

func BuildSummary(text string) Summary {
	words := NormalizeWords(text)
	counts := CountWords(words)
	return Summary{
		TotalWords:  len(words),
		UniqueWords: len(counts),
		TopWord:     topWord(counts),
	}
}

func SortedKeys(counts map[string]int) []string {
	keys := make([]string, 0, len(counts))
	for key := range counts {
		keys = append(keys, key)
	}
	sort.Strings(keys)
	return keys
}

func topWord(counts map[string]int) string {
	topWord := ""
	topCount := 0
	for _, key := range SortedKeys(counts) {
		if counts[key] > topCount {
			topWord = key
			topCount = counts[key]
		}
	}
	return topWord
}
