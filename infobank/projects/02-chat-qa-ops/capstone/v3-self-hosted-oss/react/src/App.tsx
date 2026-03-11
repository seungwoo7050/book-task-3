import { FormEvent, useEffect, useState } from "react";
import { Link, Route, Routes } from "react-router-dom";
import { apiGet, apiPost } from "./api/client";
import { DatasetsPage } from "./pages/Datasets";
import { FailuresPage } from "./pages/Failures";
import { JobsPage } from "./pages/Jobs";
import { KnowledgeBasePage } from "./pages/KnowledgeBase";
import { OverviewPage } from "./pages/Overview";
import { SessionReviewPage } from "./pages/SessionReview";

type SessionState = {
  authenticated: boolean;
  email: string | null;
};

export type JobSummary = {
  id: string;
  status: string;
  progress_completed: number;
  progress_total: number;
  error_summary: string;
  run_id: string | null;
  run_label: string | null;
  dataset_id: string;
  dataset_name: string | null;
  kb_bundle_id: string;
  kb_bundle_name: string | null;
  evaluation_count: number;
  avg_score: number;
  critical_count: number;
  created_at: string;
  updated_at: string;
};

function LoginGate({
  onLogin,
}: {
  onLogin: (session: SessionState) => void;
}) {
  const [email, setEmail] = useState("admin@example.com");
  const [password, setPassword] = useState("password123");
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      const result = await apiPost<SessionState>("/api/auth/login", { email, password });
      onLogin(result);
    } catch (err) {
      setError(String(err));
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="auth-shell">
      <section className="auth-card">
        <p className="eyebrow">Qualbot v3</p>
        <h1>Self-Hosted QA Ops</h1>
        <p className="auth-copy">
          운영자는 로그인 후 transcript JSONL과 KB ZIP을 업로드하고, 비동기 평가 job을 실행한 뒤
          failures와 session review를 확인합니다.
        </p>
        <form className="stack" onSubmit={submit}>
          <label>
            Admin email
            <input value={email} onChange={(event) => setEmail(event.target.value)} />
          </label>
          <label>
            Admin password
            <input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
            />
          </label>
          <button type="submit" disabled={submitting}>
            {submitting ? "로그인 중..." : "로그인"}
          </button>
          {error && <p className="error">{error}</p>}
        </form>
      </section>
    </main>
  );
}

export function App() {
  const [session, setSession] = useState<SessionState | null>(null);
  const [jobs, setJobs] = useState<JobSummary[]>([]);
  const [selectedJobId, setSelectedJobId] = useState<string | null>(null);

  async function refreshJobs() {
    try {
      const result = await apiGet<{ items: JobSummary[] }>("/api/jobs");
      setJobs(result.items);
      if (!selectedJobId && result.items.length > 0) {
        setSelectedJobId(result.items[0].id);
      }
    } catch {
      setJobs([]);
    }
  }

  async function refreshSession() {
    try {
      const result = await apiGet<SessionState>("/api/auth/session");
      setSession(result);
      if (result.authenticated) {
        await refreshJobs();
      }
    } catch {
      setSession({ authenticated: false, email: null });
    }
  }

  useEffect(() => {
    void refreshSession();
  }, []);

  async function logout() {
    await apiPost("/api/auth/logout", {});
    setSession({ authenticated: false, email: null });
    setJobs([]);
    setSelectedJobId(null);
  }

  if (session === null) {
    return <div className="card">세션을 확인하는 중...</div>;
  }

  if (!session.authenticated) {
    return (
      <LoginGate
        onLogin={(next) => {
          setSession(next);
          void refreshJobs();
        }}
      />
    );
  }

  const selectedJob = jobs.find((item) => item.id === selectedJobId) ?? null;

  return (
    <div className="layout">
      <aside className="sidebar">
        <p className="eyebrow">Qualbot v3</p>
        <h1>상담 품질 운영</h1>
        <p className="sidebar-copy">single-team self-hosted QA Ops workflow</p>
        <nav>
          <Link to="/">Overview</Link>
          <Link to="/datasets">Datasets</Link>
          <Link to="/knowledge-base">Knowledge Base</Link>
          <Link to="/jobs">Jobs</Link>
          <Link to="/failures">Failures</Link>
          <Link to="/sessions">Session Review</Link>
        </nav>
        <div className="sidebar-footer">
          <div>{session.email}</div>
          <div>선택된 job: {selectedJob?.run_label ?? selectedJobId ?? "-"}</div>
          <button onClick={() => void logout()}>로그아웃</button>
        </div>
      </aside>
      <main className="content">
        <Routes>
          <Route path="/" element={<OverviewPage selectedJobId={selectedJobId} />} />
          <Route path="/datasets" element={<DatasetsPage />} />
          <Route path="/knowledge-base" element={<KnowledgeBasePage />} />
          <Route
            path="/jobs"
            element={
              <JobsPage
                jobs={jobs}
                selectedJobId={selectedJobId}
                onSelectJobId={setSelectedJobId}
                onRefreshJobs={refreshJobs}
              />
            }
          />
          <Route path="/failures" element={<FailuresPage selectedJobId={selectedJobId} />} />
          <Route path="/sessions" element={<SessionReviewPage selectedJobId={selectedJobId} />} />
        </Routes>
      </main>
    </div>
  );
}
