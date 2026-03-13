package main

import (
	"fmt"

	"study.local/go/database-internals/projects/08-btree-index-and-query-scan/internal/queryscan"
)

func main() {
	executor := queryscan.New("handle", 3)
	executor.Insert(map[string]string{"handle": "ada", "tier": "gold", "region": "apac"})
	executor.Insert(map[string]string{"handle": "ben", "tier": "silver", "region": "emea"})
	executor.Insert(map[string]string{"handle": "cora", "tier": "bronze", "region": "apac"})
	executor.Insert(map[string]string{"handle": "dina", "tier": "gold", "region": "na"})
	executor.Insert(map[string]string{"handle": "erin", "tier": "silver", "region": "na"})

	pointLookup := executor.Execute(queryscan.Query{
		Column: "handle",
		Exact:  "dina",
	})
	fmt.Printf("point lookup plan: %s (%s)\n", pointLookup.Plan.Strategy, pointLookup.Plan.Reason)
	for _, row := range pointLookup.Rows {
		fmt.Printf("  row=%d handle=%s tier=%s\n", row.ID, row.Values["handle"], row.Values["tier"])
	}

	rangeScan := executor.Execute(queryscan.Query{
		Column: "handle",
		Start:  "ben",
		End:    "erin",
	})
	fmt.Printf("range scan plan: %s (%s)\n", rangeScan.Plan.Strategy, rangeScan.Plan.Reason)
	for _, row := range rangeScan.Rows {
		fmt.Printf("  row=%d handle=%s region=%s\n", row.ID, row.Values["handle"], row.Values["region"])
	}

	fullScan := executor.Execute(queryscan.Query{
		Column: "tier",
		Exact:  "gold",
	})
	fmt.Printf("fallback plan: %s (%s)\n", fullScan.Plan.Strategy, fullScan.Plan.Reason)
	for _, row := range fullScan.Rows {
		fmt.Printf("  row=%d handle=%s tier=%s\n", row.ID, row.Values["handle"], row.Values["tier"])
	}
}
