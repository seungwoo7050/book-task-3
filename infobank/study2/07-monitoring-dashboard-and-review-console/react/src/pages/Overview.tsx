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
  run_labels: string[];
};

type CompareResult = {
  result: {
    baseline: string;
    candidate: string;
    dataset: string;
    baseline_avg: number;
    candidate_avg: number;
    baseline_critical: number;
    candidate_critical: number;
    baseline_pass_count: number;
    candidate_pass_count: number;
    baseline_fail_count: number;
    candidate_fail_count: number;
    baseline_failures: Record<string, number>;
    candidate_failures: Record<string, number>;
    delta: number;
    pass_delta: number;
    fail_delta: number;
    critical_delta: number;
  };
};

export function OverviewPage() {
  const [data, setData] = useState<Overview | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [compare, setCompare] = useState<CompareResult | null>(null);
  const [compareError, setCompareError] = useState<string | null>(null);
  const [baseline, setBaseline] = useState("v1.0");
  const [candidate, setCandidate] = useState("v1.1");
  const [dataset, setDataset] = useState("golden-set");

  useEffect(() => {
    apiGet<Overview>("/api/dashboard/overview")
      .then((overview) => {
        setData(overview);
        if (overview.run_labels.length > 0) {
          setBaseline((current) => current || overview.run_labels[0] || "v1.0");
          setCandidate((current) => {
            if (current) return current;
            return overview.run_labels[1] ?? overview.run_labels[0] ?? "v1.1";
          });
        }
      })
      .catch((err) => setError(String(err)));
  }, []);

  async function loadCompare() {
    setCompareError(null);
    try {
      const params = new URLSearchParams({ baseline, candidate });
      if (dataset.trim()) {
        params.set("dataset", dataset.trim());
      }
      const result = await apiGet<CompareResult>(`/api/dashboard/version-compare?${params.toString()}`);
      setCompare(result);
    } catch (err) {
      setCompareError(String(err));
      setCompare(null);
    }
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
        <ScoreCard label="평가 건수" value={data.evaluation_count} />
        <ScoreCard label="평균 지연" value={`${data.avg_latency_ms}ms`} />
      </div>

      <div className="card">
        <h3>Run Labels</h3>
        <div className="pill-row">
          {data.run_labels.length === 0 && <span className="pill muted">기록 없음</span>}
          {data.run_labels.map((label) => (
            <span key={label} className="pill">
              {label}
            </span>
          ))}
        </div>
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
        <div className="form-grid">
          <label>
            Baseline
            <input value={baseline} onChange={(event) => setBaseline(event.target.value)} />
          </label>
          <label>
            Candidate
            <input value={candidate} onChange={(event) => setCandidate(event.target.value)} />
          </label>
          <label>
            Dataset
            <input value={dataset} onChange={(event) => setDataset(event.target.value)} />
          </label>
        </div>
        <button onClick={loadCompare}>비교 로드</button>
        {compareError && <p className="error">{compareError}</p>}
        {compare && (
          <div className="stack">
            <div className="grid">
              <ScoreCard label="점수 변화" value={compare.result.delta} />
              <ScoreCard label="Pass 변화" value={compare.result.pass_delta} />
              <ScoreCard label="Fail 변화" value={compare.result.fail_delta} />
              <ScoreCard label="Critical 변화" value={compare.result.critical_delta} />
            </div>
            <div className="compare-summary">
              <div className="inset-card">
                <h4>Baseline</h4>
                <p>
                  {compare.result.baseline} / {compare.result.dataset}
                </p>
                <p>
                  평균 {compare.result.baseline_avg} / pass {compare.result.baseline_pass_count} / fail{" "}
                  {compare.result.baseline_fail_count} / critical {compare.result.baseline_critical}
                </p>
              </div>
              <div className="inset-card">
                <h4>Candidate</h4>
                <p>
                  {compare.result.candidate} / {compare.result.dataset}
                </p>
                <p>
                  평균 {compare.result.candidate_avg} / pass {compare.result.candidate_pass_count} / fail{" "}
                  {compare.result.candidate_fail_count} / critical {compare.result.candidate_critical}
                </p>
              </div>
            </div>
            <div className="compare-summary">
              <div className="inset-card">
                <h4>Baseline 실패 분포</h4>
                <FailureTable
                  items={Object.entries(compare.result.baseline_failures).map(([failure_type, count]) => ({
                    failure_type,
                    count,
                  }))}
                />
              </div>
              <div className="inset-card">
                <h4>Candidate 실패 분포</h4>
                <FailureTable
                  items={Object.entries(compare.result.candidate_failures).map(([failure_type, count]) => ({
                    failure_type,
                    count,
                  }))}
                />
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
