import { useEffect, useState } from "react";
import { apiGet } from "../api/client";
import { FailureTable } from "../components/FailureTable";

type FailureRow = {
  failure_type: string;
  count: number;
  critical_count: number;
  avg_score: number;
};

export function FailuresPage() {
  const [rows, setRows] = useState<FailureRow[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiGet<{ items: FailureRow[] }>("/api/dashboard/failures")
      .then((result) => {
        setRows(result.items);
        setLoading(false);
      })
      .catch((err) => {
        setRows([]);
        setError(String(err));
        setLoading(false);
      });
  }, []);

  const totalCount = rows.reduce((sum, row) => sum + row.count, 0);

  return (
    <div className="stack">
      <h2>실패 분석</h2>
      <div className="card">
        <div className="summary-row">
          <span>유형 수: {rows.length}</span>
          <span>총 실패 카운트: {totalCount}</span>
        </div>
        {loading && <p>실패 데이터를 불러오는 중...</p>}
        {error && <p className="error">오류: {error}</p>}
        <FailureTable items={rows} />
      </div>
    </div>
  );
}
