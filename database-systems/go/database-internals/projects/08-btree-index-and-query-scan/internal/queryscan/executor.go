package queryscan

import (
	"sort"

	"study.local/go/database-internals/projects/08-btree-index-and-query-scan/internal/btreeindex"
)

type Row struct {
	ID     int
	Values map[string]string
}

type Query struct {
	Column string
	Exact  string
	Start  string
	End    string
}

type QueryPlan struct {
	Strategy string
	Reason   string
}

type QueryResult struct {
	Plan QueryPlan
	Rows []Row
}

type QueryScanExecutor struct {
	indexColumn string
	nextRowID   int
	rows        map[int]Row
	index       *btreeindex.BTreeIndex
}

func New(indexColumn string, order int) *QueryScanExecutor {
	return &QueryScanExecutor{
		indexColumn: indexColumn,
		nextRowID:   1,
		rows:        map[int]Row{},
		index:       btreeindex.New(order),
	}
}

func (executor *QueryScanExecutor) Insert(values map[string]string) Row {
	row := Row{
		ID:     executor.nextRowID,
		Values: copyValues(values),
	}
	executor.nextRowID++
	executor.rows[row.ID] = row
	executor.index.Insert(row.Values[executor.indexColumn], row.ID)
	return row
}

func (executor *QueryScanExecutor) Plan(query Query) QueryPlan {
	if query.Column == executor.indexColumn && query.Exact != "" {
		return QueryPlan{
			Strategy: "index-point-lookup",
			Reason:   "indexed equality predicate can jump directly to the leaf entry",
		}
	}
	if query.Column == executor.indexColumn && (query.Start != "" || query.End != "") {
		return QueryPlan{
			Strategy: "index-range-scan",
			Reason:   "indexed range predicate can walk linked leaves in key order",
		}
	}
	return QueryPlan{
		Strategy: "full-scan",
		Reason:   "predicate is not aligned with the secondary index",
	}
}

func (executor *QueryScanExecutor) Execute(query Query) QueryResult {
	plan := executor.Plan(query)
	switch plan.Strategy {
	case "index-point-lookup":
		return QueryResult{Plan: plan, Rows: executor.collectByRowIDs(executor.index.Lookup(query.Exact))}
	case "index-range-scan":
		return QueryResult{Plan: plan, Rows: executor.collectByCursor(query.Start, query.End)}
	default:
		return QueryResult{Plan: plan, Rows: executor.collectByFullScan(query)}
	}
}

func (executor *QueryScanExecutor) collectByRowIDs(rowIDs []int) []Row {
	rows := make([]Row, 0, len(rowIDs))
	for _, rowID := range rowIDs {
		if row, ok := executor.rows[rowID]; ok {
			rows = append(rows, cloneRow(row))
		}
	}
	return rows
}

func (executor *QueryScanExecutor) collectByCursor(start, end string) []Row {
	cursor := executor.index.OpenRange(start, end)
	rows := []Row{}
	for {
		entry, ok := cursor.Next()
		if !ok {
			break
		}
		rows = append(rows, executor.collectByRowIDs(entry.RowIDs)...)
	}
	return rows
}

func (executor *QueryScanExecutor) collectByFullScan(query Query) []Row {
	ids := make([]int, 0, len(executor.rows))
	for id := range executor.rows {
		ids = append(ids, id)
	}
	sort.Ints(ids)

	rows := []Row{}
	for _, id := range ids {
		row := executor.rows[id]
		if matches(row, query) {
			rows = append(rows, cloneRow(row))
		}
	}
	return rows
}

func matches(row Row, query Query) bool {
	value := row.Values[query.Column]
	if query.Exact != "" {
		return value == query.Exact
	}
	if query.Start != "" && value < query.Start {
		return false
	}
	if query.End != "" && value > query.End {
		return false
	}
	return true
}

func cloneRow(row Row) Row {
	return Row{
		ID:     row.ID,
		Values: copyValues(row.Values),
	}
}

func copyValues(values map[string]string) map[string]string {
	copied := make(map[string]string, len(values))
	for key, value := range values {
		copied[key] = value
	}
	return copied
}
