import { useState } from "react";
import { apiPost } from "../api/client";

type RunResult = {
  count: number;
  avg_score: number;
  critical_count: number;
};

export function EvalRunnerPage() {
  const [running, setRunning] = useState(false);
  const [result, setResult] = useState<RunResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function runGoldenSet() {
    setRunning(true);
    setError(null);
    try {
      const payload = await apiPost<RunResult>("/api/golden-set/run", {
        prompt_version: "v1.0",
        kb_version: "v1.0",
        evaluator_version: "eval-v1"
      });
      setResult(payload);
    } catch (err) {
      setError(`실행 오류: ${String(err)}`);
    } finally {
      setRunning(false);
    }
  }

  return (
    <div className="stack">
      <h2>평가 실행</h2>
      <div className="card">
        <button disabled={running} onClick={runGoldenSet}>
          {running ? "실행 중..." : "골든셋 평가 실행"}
        </button>
        {error && <p className="error">{error}</p>}
        {result && (
          <div className="stack">
            <p>평가 건수: {result.count}</p>
            <p>평균 점수: {result.avg_score}</p>
            <p>CRITICAL 건수: {result.critical_count}</p>
          </div>
        )}
      </div>
    </div>
  );
}
