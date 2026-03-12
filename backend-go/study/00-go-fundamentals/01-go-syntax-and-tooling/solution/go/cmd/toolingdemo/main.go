package main

import (
	"fmt"
	"os"
	"strings"

	"github.com/woopinbell/go-backend/study/00-go-fundamentals/01-go-syntax-and-tooling/lesson"
)

func main() {
	input := "Go is simple, and simple tools make Go easier to learn."
	if len(os.Args) > 1 {
		input = strings.Join(os.Args[1:], " ")
	}

	summary := lesson.BuildSummary(input)
	fmt.Printf("total=%d unique=%d top=%s\n", summary.TotalWords, summary.UniqueWords, summary.TopWord)
}
