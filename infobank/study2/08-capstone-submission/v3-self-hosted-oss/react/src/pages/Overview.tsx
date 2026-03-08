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
  selected_run_id: string | null;
  selected_job_id: string | null;
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

export function OverviewPage({ selectedJobId }: { selectedJobId: string | null }) {
  const [data, setData] = useState<Overview | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [compare, setCompare] = useState<CompareResult | null>(null);
  const [compareError, setCompareError] = useState<string | null>(null);
  const [baseline, setBaseline] = useState("baseline-run");
  const [candidate, setCandidate] = useState("candidate-run");
  const [dataset, setDataset] = useState("shared-dataset");

  useEffect(() => {
    const params = selectedJobId ? `?job_id=${selectedJobId}` : "";
    apiGet<Overview>(`/api/dashboard/overview${params}`)
      .then((overview) => {
        setData(overview);
      })
      .catch((err) => setError(String(err)));
  }, [selectedJobId]);

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

  if (error) {
    return <div className="card">오류: {error}</div>;
  }
  if (!data) {
    return <div className="card">데이터를 불러오는 중...</div>;
  }

  return (
    <div className="stack">
      <h2>Overview</h2>
      <div className="grid">
        <ScoreCard label="평균 점수" value={data.avg_score} />
        <ScoreCard label="실패율" value={`${data.fail_rate}%`} />
        <ScoreCard label="Critical" value={data.critical_count} />
        <ScoreCard label="평가 건수" value={data.evaluation_count} />
        <ScoreCard label="평균 지연" value={`${data.avg_latency_ms}ms`} />
      </div>

      <div className="card">
        <div className="key-value">
          <span>selected job={data.selected_job_id ?? "-"}</span>
          <span>selected run={data.selected_run_id ?? "-"}</span>
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
            {Object.entries(data.grade_distribution).map(([grade, count]) => (
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
        <h3>Baseline vs Candidate</h3>
        <div className="form-grid">
          <label>
            Baseline label
            <input value={baseline} onChange={(event) => setBaseline(event.target.value)} />
          </label>
          <label>
            Candidate label
            <input value={candidate} onChange={(event) => setCandidate(event.target.value)} />
          </label>
          <label>
            Dataset
            <input value={dataset} onChange={(event) => setDataset(event.target.value)} />
          </label>
        </div>
        <button onClick={() => void loadCompare()}>비교 로드</button>
        {compareError && <p className="error">{compareError}</p>}
        {compare && (
          <div className="compare-summary">
            <div className="inset-card">
              <h4>Delta</h4>
              <p>score={compare.result.delta}</p>
              <p>pass={compare.result.pass_delta}</p>
              <p>fail={compare.result.fail_delta}</p>
              <p>critical={compare.result.critical_delta}</p>
            </div>
            <div className="inset-card">
              <h4>Candidate</h4>
              <p>
                {compare.result.candidate} / {compare.result.dataset}
              </p>
              <p>
                avg {compare.result.candidate_avg} / critical {compare.result.candidate_critical}
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
