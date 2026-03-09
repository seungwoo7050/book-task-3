import { useEffect, useState } from "react";
import { apiGet } from "../api/client";
import { FailureTable } from "../components/FailureTable";
import { ScoreCard } from "../components/ScoreCard";
import { gradeKo } from "../i18n/ko";

type Overview = {
  avg_score: number;
  fail_rate: number;
  critical_count: number;
  evaluation_count: number;
  avg_latency_ms: number;
  grade_distribution: Record<string, number>;
  failure_top: { failure_type: string; count: number }[];
};

type CompareResult = {
  result: {
    baseline: string;
    candidate: string;
    baseline_avg: number;
    candidate_avg: number;
    delta: number;
  };
};

export function OverviewPage() {
  const [data, setData] = useState<Overview | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [compare, setCompare] = useState<CompareResult | null>(null);

  useEffect(() => {
    apiGet<Overview>("/api/dashboard/overview")
      .then(setData)
      .catch((err) => setError(String(err)));
  }, []);

  async function loadCompare() {
    const result = await apiGet<CompareResult>("/api/dashboard/version-compare?baseline=v1.0&candidate=v1.1");
    setCompare(result);
  }

  if (error) return <div className="card">오류: {error}</div>;
  if (!data) return <div className="card">데이터를 불러오는 중...</div>;

  const gradeRows = Object.entries(data.grade_distribution);

  return (
    <div className="stack">
      <h2>개요</h2>
      <div className="grid">
        <ScoreCard label="평균 점수" value={data.avg_score} />
        <ScoreCard label="실패율" value={`${data.fail_rate}%`} />
        <ScoreCard label="CRITICAL" value={data.critical_count} />
        <ScoreCard label="평균 지연" value={`${data.avg_latency_ms}ms`} />
      </div>

      <div className="card">
        <h3>등급 분포</h3>
        <table className="table">
          <thead>
            <tr>
              <th>등급</th>
              <th>건수</th>
            </tr>
          </thead>
          <tbody>
            {gradeRows.map(([grade, count]) => (
              <tr key={grade}>
                <td>{gradeKo(grade)}</td>
                <td>{count}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="card">
        <h3>주요 실패 유형</h3>
        <FailureTable items={data.failure_top.map((item) => ({ ...item, critical_count: 0, avg_score: 0 }))} />
      </div>

      <div className="card">
        <h3>Phase2 비교 훅</h3>
        <button onClick={loadCompare}>v1.0 과 v1.1 비교 로드</button>
        {compare && <pre>{JSON.stringify(compare.result, null, 2)}</pre>}
      </div>
    </div>
  );
}
