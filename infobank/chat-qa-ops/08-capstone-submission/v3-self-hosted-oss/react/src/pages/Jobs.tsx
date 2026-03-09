import { FormEvent, useEffect, useState } from "react";
import { apiGet, apiPost } from "../api/client";
import type { JobSummary } from "../App";

type DatasetItem = {
  id: string;
  name: string;
  is_sample: boolean;
};

type BundleItem = {
  id: string;
  name: string;
  is_sample: boolean;
};

type Props = {
  jobs: JobSummary[];
  selectedJobId: string | null;
  onSelectJobId: (id: string) => void;
  onRefreshJobs: () => Promise<void>;
};

export function JobsPage({ jobs, selectedJobId, onSelectJobId, onRefreshJobs }: Props) {
  const [datasets, setDatasets] = useState<DatasetItem[]>([]);
  const [bundles, setBundles] = useState<BundleItem[]>([]);
  const [datasetId, setDatasetId] = useState("");
  const [bundleId, setBundleId] = useState("");
  const [runLabel, setRunLabel] = useState("");
  const [promptVersion, setPromptVersion] = useState("v1.0");
  const [kbVersion, setKbVersion] = useState("v1.0");
  const [evaluatorVersion, setEvaluatorVersion] = useState("eval-v1");
  const [retrievalVersion, setRetrievalVersion] = useState("retrieval-v2");
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  async function loadOptions() {
    try {
      const [datasetResult, bundleResult] = await Promise.all([
        apiGet<{ items: DatasetItem[] }>("/api/datasets"),
        apiGet<{ items: BundleItem[] }>("/api/kb-bundles"),
      ]);
      setDatasets(datasetResult.items);
      setBundles(bundleResult.items);
      if (!datasetId && datasetResult.items[0]) {
        setDatasetId(datasetResult.items[0].id);
      }
      if (!bundleId && bundleResult.items[0]) {
        setBundleId(bundleResult.items[0].id);
      }
    } catch (err) {
      setError(String(err));
    }
  }

  useEffect(() => {
    void loadOptions();
  }, []);

  useEffect(() => {
    const hasActiveJob = jobs.some((job) => job.status === "pending" || job.status === "running");
    if (!hasActiveJob) {
      return undefined;
    }
    const timer = window.setInterval(() => {
      void onRefreshJobs();
    }, 2500);
    return () => window.clearInterval(timer);
  }, [jobs, onRefreshJobs]);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      const result = await apiPost<{ job: JobSummary }>("/api/jobs", {
        dataset_id: datasetId,
        kb_bundle_id: bundleId,
        run_label: runLabel.trim() || undefined,
        prompt_version: promptVersion,
        kb_version: kbVersion,
        evaluator_version: evaluatorVersion,
        retrieval_version: retrievalVersion,
      });
      await onRefreshJobs();
      onSelectJobId(result.job.id);
      if (!runLabel.trim()) {
        setRunLabel("");
      }
    } catch (err) {
      setError(String(err));
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="stack">
      <h2>Jobs</h2>
      <div className="card">
        <form className="stack" onSubmit={submit}>
          <div className="form-grid">
            <label>
              Dataset
              <select value={datasetId} onChange={(event) => setDatasetId(event.target.value)}>
                {datasets.map((item) => (
                  <option key={item.id} value={item.id}>
                    {item.name} {item.is_sample ? "(sample)" : ""}
                  </option>
                ))}
              </select>
            </label>
            <label>
              KB bundle
              <select value={bundleId} onChange={(event) => setBundleId(event.target.value)}>
                {bundles.map((item) => (
                  <option key={item.id} value={item.id}>
                    {item.name} {item.is_sample ? "(sample)" : ""}
                  </option>
                ))}
              </select>
            </label>
            <label>
              Run label
              <input value={runLabel} onChange={(event) => setRunLabel(event.target.value)} placeholder="candidate-run" />
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
          </div>
          <button type="submit" disabled={submitting || !datasetId || !bundleId}>
            {submitting ? "job 생성 중..." : "job 생성"}
          </button>
          {error && <p className="error">{error}</p>}
        </form>
      </div>

      <div className="card">
        <table className="table">
          <thead>
            <tr>
              <th>선택</th>
              <th>run</th>
              <th>status</th>
              <th>dataset</th>
              <th>kb</th>
              <th>progress</th>
              <th>avg</th>
              <th>critical</th>
            </tr>
          </thead>
          <tbody>
            {jobs.map((job) => (
              <tr key={job.id} className={job.id === selectedJobId ? "row-selected" : ""}>
                <td>
                  <button type="button" onClick={() => onSelectJobId(job.id)}>
                    선택
                  </button>
                </td>
                <td>{job.run_label ?? "-"}</td>
                <td>{job.status}</td>
                <td>{job.dataset_name ?? "-"}</td>
                <td>{job.kb_bundle_name ?? "-"}</td>
                <td>
                  {job.progress_completed}/{job.progress_total}
                </td>
                <td>{job.avg_score}</td>
                <td>{job.critical_count}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
