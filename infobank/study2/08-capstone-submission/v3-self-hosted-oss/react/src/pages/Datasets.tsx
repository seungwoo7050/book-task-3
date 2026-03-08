import { FormEvent, useEffect, useState } from "react";
import { apiGet, apiUpload } from "../api/client";

type DatasetItem = {
  id: string;
  name: string;
  source_filename: string;
  record_count: number;
  is_sample: boolean;
  created_at: string;
};

export function DatasetsPage() {
  const [items, setItems] = useState<DatasetItem[]>([]);
  const [name, setName] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  async function load() {
    try {
      const result = await apiGet<{ items: DatasetItem[] }>("/api/datasets");
      setItems(result.items);
    } catch (err) {
      setError(String(err));
    }
  }

  useEffect(() => {
    void load();
  }, []);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!file) {
      setError("JSONL 파일을 선택해야 합니다.");
      return;
    }
    setSubmitting(true);
    setError(null);
    try {
      await apiUpload("/api/datasets/import", {
        file,
        fields: name.trim() ? { name: name.trim() } : undefined,
      });
      setName("");
      setFile(null);
      await load();
    } catch (err) {
      setError(String(err));
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="stack">
      <h2>Datasets</h2>
      <div className="card">
        <form className="stack" onSubmit={submit}>
          <div className="form-grid">
            <label>
              표시 이름
              <input value={name} onChange={(event) => setName(event.target.value)} placeholder="support-transcripts" />
            </label>
            <label>
              Transcript JSONL
              <input
                type="file"
                accept=".jsonl"
                onChange={(event) => setFile(event.target.files?.[0] ?? null)}
              />
            </label>
          </div>
          <button type="submit" disabled={submitting}>
            {submitting ? "업로드 중..." : "dataset 업로드"}
          </button>
          {error && <p className="error">{error}</p>}
        </form>
      </div>
      <div className="card">
        <table className="table">
          <thead>
            <tr>
              <th>이름</th>
              <th>source</th>
              <th>records</th>
              <th>sample</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <tr key={item.id}>
                <td>{item.name}</td>
                <td>{item.source_filename}</td>
                <td>{item.record_count}</td>
                <td>{item.is_sample ? "yes" : "no"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
