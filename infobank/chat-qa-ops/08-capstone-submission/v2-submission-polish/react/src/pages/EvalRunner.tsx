import { useState } from "react";
import { apiPost } from "../api/client";

type RunResult = {
  run_id: string;
  run_label: string;
  dataset: string;
  count: number;
  avg_score: number;
  critical_count: number;
  pass_count: number;
  fail_count: number;
};

export function EvalRunnerPage() {
  const [running, setRunning] = useState(false);
  const [result, setResult] = useState<RunResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [runLabel, setRunLabel] = useState("v1.1");
  const [dataset, setDataset] = useState("golden-set");
  const [promptVersion, setPromptVersion] = useState("v1.0");
  const [kbVersion, setKbVersion] = useState("v1.0");
  const [evaluatorVersion, setEvaluatorVersion] = useState("eval-v1");
  const [retrievalVersion, setRetrievalVersion] = useState("retrieval-v1");
  const [baselineLabel, setBaselineLabel] = useState("v1.0");
  const [candidateLabel, setCandidateLabel] = useState("v1.1");

  async function runGoldenSet() {
    setRunning(true);
    setError(null);
    try {
      const payload = await apiPost<RunResult>("/api/golden-set/run", {
        prompt_version: promptVersion,
        kb_version: kbVersion,
        evaluator_version: evaluatorVersion,
        retrieval_version: retrievalVersion,
        run_label: runLabel,
        dataset,
        baseline_label: baselineLabel,
        candidate_label: candidateLabel,
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
        <div className="form-grid">
          <label>
            Run label
            <input value={runLabel} onChange={(event) => setRunLabel(event.target.value)} />
          </label>
          <label>
            Dataset
            <input value={dataset} onChange={(event) => setDataset(event.target.value)} />
          </label>
          <label>
            Prompt version
            <input value={promptVersion} onChange={(event) => setPromptVersion(event.target.value)} />
          </label>
          <label>
            KB version
            <input value={kbVersion} onChange={(event) => setKbVersion(event.target.value)} />
          </label>
          <label>
            Evaluator version
            <input value={evaluatorVersion} onChange={(event) => setEvaluatorVersion(event.target.value)} />
          </label>
          <label>
            Retrieval version
            <input value={retrievalVersion} onChange={(event) => setRetrievalVersion(event.target.value)} />
          </label>
          <label>
            Baseline label
            <input value={baselineLabel} onChange={(event) => setBaselineLabel(event.target.value)} />
          </label>
          <label>
            Candidate label
            <input value={candidateLabel} onChange={(event) => setCandidateLabel(event.target.value)} />
          </label>
        </div>
        <button disabled={running} onClick={runGoldenSet}>
          {running ? "실행 중..." : "골든셋 평가 실행"}
        </button>
        {error && <p className="error">{error}</p>}
        {result && (
          <div className="stack">
            <p>run_id: {result.run_id}</p>
            <p>run_label: {result.run_label}</p>
            <p>dataset: {result.dataset}</p>
            <p>평가 건수: {result.count}</p>
            <p>평균 점수: {result.avg_score}</p>
            <p>CRITICAL 건수: {result.critical_count}</p>
            <p>assertion pass/fail: {result.pass_count} / {result.fail_count}</p>
          </div>
        )}
      </div>
    </div>
  );
}
