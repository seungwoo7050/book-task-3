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

  useEffect(() => {
    apiGet<{ items: FailureRow[] }>("/api/dashboard/failures")
      .then((result) => setRows(result.items))
      .catch(() => setRows([]));
  }, []);

  return (
    <div className="stack">
      <h2>실패 분석</h2>
      <div className="card">
        <FailureTable items={rows} />
      </div>
    </div>
  );
}
