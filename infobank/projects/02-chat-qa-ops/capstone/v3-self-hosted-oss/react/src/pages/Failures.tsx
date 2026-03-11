import { useEffect, useState } from "react";
import { apiGet } from "../api/client";
import { FailureTable } from "../components/FailureTable";

type FailureRow = {
  failure_type: string;
  count: number;
  critical_count: number;
  avg_score: number;
};

export function FailuresPage({ selectedJobId }: { selectedJobId: string | null }) {
  const [rows, setRows] = useState<FailureRow[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const params = selectedJobId ? `?job_id=${selectedJobId}` : "";
    apiGet<{ items: FailureRow[] }>(`/api/dashboard/failures${params}`)
      .then((result) => {
        setRows(result.items);
      })
      .catch((err) => {
        setRows([]);
        setError(String(err));
      });
  }, [selectedJobId]);

  const totalCount = rows.reduce((sum, row) => sum + row.count, 0);

  return (
    <div className="stack">
      <h2>Failures</h2>
      <div className="card">
        <div className="summary-row">
          <span>유형 수: {rows.length}</span>
          <span>총 실패 카운트: {totalCount}</span>
          <span>selected job: {selectedJobId ?? "-"}</span>
        </div>
        {error && <p className="error">오류: {error}</p>}
        <FailureTable items={rows} />
      </div>
    </div>
  );
}
