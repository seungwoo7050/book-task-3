package tests

import (
	"reflect"
	"testing"

	"study.local/go/database-internals/projects/08-btree-index-and-query-scan/internal/queryscan"
)

func TestPlannerUsesIndexForEqualityAndRange(t *testing.T) {
	executor := seededExecutor()

	equality := executor.Execute(queryscan.Query{
		Column: "handle",
		Exact:  "dina",
	})
	if equality.Plan.Strategy != "index-point-lookup" {
		t.Fatalf("expected index-point-lookup, got %s", equality.Plan.Strategy)
	}
	if got := rowHandles(equality.Rows); !reflect.DeepEqual(got, []string{"dina"}) {
		t.Fatalf("expected point lookup result [dina], got %v", got)
	}

	rangeResult := executor.Execute(queryscan.Query{
		Column: "handle",
		Start:  "ben",
		End:    "erin",
	})
	if rangeResult.Plan.Strategy != "index-range-scan" {
		t.Fatalf("expected index-range-scan, got %s", rangeResult.Plan.Strategy)
	}
	if got := rowHandles(rangeResult.Rows); !reflect.DeepEqual(got, []string{"ben", "cora", "dina", "erin"}) {
		t.Fatalf("unexpected range result %v", got)
	}
}

func TestPlannerFallsBackToFullScanForNonIndexedColumn(t *testing.T) {
	executor := seededExecutor()

	result := executor.Execute(queryscan.Query{
		Column: "tier",
		Exact:  "gold",
	})
	if result.Plan.Strategy != "full-scan" {
		t.Fatalf("expected full-scan, got %s", result.Plan.Strategy)
	}
	if got := rowHandles(result.Rows); !reflect.DeepEqual(got, []string{"ada", "dina"}) {
		t.Fatalf("unexpected rows from full scan %v", got)
	}
}

func seededExecutor() *queryscan.QueryScanExecutor {
	executor := queryscan.New("handle", 3)
	executor.Insert(map[string]string{"handle": "ada", "tier": "gold"})
	executor.Insert(map[string]string{"handle": "ben", "tier": "silver"})
	executor.Insert(map[string]string{"handle": "cora", "tier": "bronze"})
	executor.Insert(map[string]string{"handle": "dina", "tier": "gold"})
	executor.Insert(map[string]string{"handle": "erin", "tier": "silver"})
	return executor
}

func rowHandles(rows []queryscan.Row) []string {
	handles := make([]string, 0, len(rows))
	for _, row := range rows {
		handles = append(handles, row.Values["handle"])
	}
	return handles
}
