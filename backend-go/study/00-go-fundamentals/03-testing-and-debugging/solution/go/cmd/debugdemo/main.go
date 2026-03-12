package main

import (
	"fmt"
	"log"

	"github.com/woopinbell/go-backend/study/00-go-fundamentals/03-testing-and-debugging/analyzer"
)

func main() {
	lines := []string{"search,120", "search,80", "checkout,150"}
	summaries, err := analyzer.Summarize(lines)
	if err != nil {
		log.Fatal(err)
	}

	for category, summary := range summaries {
		fmt.Printf("%s count=%d avg_ms=%d\n", category, summary.Count, summary.AverageMS)
	}
}
