"use client";

import type {
  AuditEvent,
  CatalogEntry,
  CatalogImportBundle,
  ExperimentConfig,
  InstanceSettings,
  JobRun,
  RecommendationResult,
  ReleaseCandidate,
  User
} from "@study1-v3/shared";
import React, { useEffect, useMemo, useState } from "react";

const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:3103";

const capabilityOptions = [
  "release-management",
  "changesets",
  "semver",
  "document-search",
  "git",
  "notion",
  "logs"
];

type AuthSession = {
  user: User;
  settings: InstanceSettings;
};

type EvalSummary = {
  id: string;
  metrics: {
    top3Recall: number;
    explanationCompleteness: number;
    forbiddenHitRate: number;
  };
  acceptance: {
    top3RecallPass: boolean;
    explanationPass: boolean;
    forbiddenPass: boolean;
  };
};

type CompareSummary = {
  id: string;
  metrics: {
    baselineNdcg3: number;
    candidateNdcg3: number;
    uplift: number;
    baselineTop1HitRate: number;
    candidateTop1HitRate: number;
  };
};

type CompatibilitySummary = {
  id: string;
  releaseCandidateId: string;
  passed: boolean;
  checks: Array<{ name: string; passed: boolean; detailKo: string }>;
};

type GateSummary = {
  id: string;
  releaseCandidateId: string;
  passed: boolean;
  reasons: string[];
  metrics: {
    top3Recall: number;
    explanationCompleteness: number;
    forbiddenHitRate: number;
    baselineNdcg3: number;
    candidateNdcg3: number;
    uplift: number;
  };
};

type ArtifactSummary = {
  id: string;
  releaseCandidateId: string;
  content: string;
};

type UsageSummary = {
  items: Array<{ catalogId: string; action: string }>;
  totals: { impression: number; click: number; accept: number; dismiss: number };
};

async function apiFetch<T>(path: string, init?: RequestInit) {
  const response = await fetch(`${apiBaseUrl}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {})
    },
    credentials: "include",
    cache: "no-store"
  });

  if (!response.ok) {
    const message = response.status === 401 ? "Unauthorized" : `API request failed: ${response.status}`;
    throw new Error(message);
  }

  return (await response.json()) as T;
}

function sleep(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function buildSampleCatalogEntry(seed: CatalogEntry, id: string): CatalogEntry {
  return {
    ...seed,
    id,
    slug: id,
    name: `OSS ${seed.name}`,
    version: "1.0.0",
    summaryKo: `${seed.summaryKo} self-hosted 운영 샘플`,
    descriptionKo: `${seed.descriptionKo} self-hosted team 운영 콘솔에서 import/export와 CRUD 흐름을 검증하기 위한 샘플 엔트리입니다.`,
    exposure: {
      ...seed.exposure,
      userFacingSummaryKo: `${seed.exposure.userFacingSummaryKo} (v3 sample)`
    }
  };
}

function buildSampleExperiment(id: string): ExperimentConfig {
  return {
    id,
    name: `self-host-ops-${id.slice(-4)}`,
    baselineStrategy: "weighted-baseline-v0",
    candidateStrategy: "signal-rerank-v1",
    trafficSplitPercent: 50,
    status: "draft",
    hypothesisKo: "운영자가 남긴 feedback과 usage signal이 self-hosted 환경에서도 compare를 안정화한다."
  };
}

function buildSampleReleaseCandidate(id: string, manifestId: string): ReleaseCandidate {
  const now = new Date().toISOString();
  return {
    id,
    name: `${manifestId} v1.5.1`,
    manifestId,
    previousVersion: "1.5.0",
    releaseVersion: "1.5.1",
    targetClientVersion: "1.2.0",
    releaseNotesKo:
      "변경 요약: self-hosted 운영 절차를 안정화했습니다.\n검증: eval, compare, compatibility, release gate를 다시 실행했습니다.\n리스크: 새 권한 정책은 운영자 교육이 필요합니다.",
    requiredDocs: [
      "docs/README.md",
      "docs/install.md",
      "docs/security-model.md",
      "docs/operations.md"
    ],
    requiredArtifacts: ["Dockerfile.api", "Dockerfile.worker", "Dockerfile.web", "docker-compose.yml"],
    deprecatedFieldsUsed: [],
    owner: "release-ops",
    status: "draft",
    createdAt: now,
    updatedAt: now
  };
}

export function MpcDashboard() {
  const [session, setSession] = useState<AuthSession | null>(null);
  const [checkingSession, setCheckingSession] = useState(true);
  const [catalog, setCatalog] = useState<CatalogEntry[]>([]);
  const [experiments, setExperiments] = useState<ExperimentConfig[]>([]);
  const [releaseCandidates, setReleaseCandidates] = useState<ReleaseCandidate[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [auditLogs, setAuditLogs] = useState<AuditEvent[]>([]);
  const [jobs, setJobs] = useState<JobRun[]>([]);
  const [usageSummary, setUsageSummary] = useState<UsageSummary | null>(null);
  const [latestEval, setLatestEval] = useState<EvalSummary | null>(null);
  const [latestCompare, setLatestCompare] = useState<CompareSummary | null>(null);
  const [latestCompatibility, setLatestCompatibility] = useState<CompatibilitySummary | null>(null);
  const [latestGate, setLatestGate] = useState<GateSummary | null>(null);
  const [latestArtifact, setLatestArtifact] = useState<ArtifactSummary | null>(null);
  const [baselineRecommendation, setBaselineRecommendation] = useState<RecommendationResult | null>(null);
  const [candidateRecommendation, setCandidateRecommendation] = useState<RecommendationResult | null>(
    null
  );
  const [query, setQuery] = useState("배포 전에 manifest 호환성과 changeset 릴리즈 체크를 같이 보고 싶어요");
  const [desiredCapabilities, setDesiredCapabilities] = useState<string[]>([
    "release-management",
    "changesets",
    "semver"
  ]);
  const [selectedCatalogId, setSelectedCatalogId] = useState("release-check-bot");
  const [selectedExperimentId, setSelectedExperimentId] = useState("exp-release-signal");
  const [selectedReleaseCandidateId, setSelectedReleaseCandidateId] = useState(
    "rc-release-check-bot-1-5-0"
  );
  const [catalogSummaryDraft, setCatalogSummaryDraft] = useState("");
  const [catalogFreshnessDraft, setCatalogFreshnessDraft] = useState("0.95");
  const [settingsDraft, setSettingsDraft] = useState<InstanceSettings | null>(null);
  const [newUserEmail, setNewUserEmail] = useState("operator2@study1.local");
  const [newUserName, setNewUserName] = useState("New Operator");
  const [newUserRole, setNewUserRole] = useState<User["role"]>("operator");
  const [newUserPassword, setNewUserPassword] = useState("Operator123!");
  const [importBundleText, setImportBundleText] = useState("");
  const [activeJobId, setActiveJobId] = useState<string | null>(null);
  const [authEmail, setAuthEmail] = useState("owner@study1.local");
  const [authPassword, setAuthPassword] = useState("ChangeMe123!");
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  const selectedCatalog = useMemo(
    () => catalog.find((item) => item.id === selectedCatalogId) ?? catalog[0] ?? null,
    [catalog, selectedCatalogId]
  );

  const canOperate = session?.user.role === "owner" || session?.user.role === "operator";
  const isOwner = session?.user.role === "owner";

  useEffect(() => {
    if (selectedCatalog) {
      setCatalogSummaryDraft(selectedCatalog.summaryKo);
      setCatalogFreshnessDraft(String(selectedCatalog.freshnessScore));
    }
  }, [selectedCatalog]);

  async function loadSession() {
    try {
      const response = await apiFetch<AuthSession>("/api/auth/session");
      setSession(response);
      setSettingsDraft(response.settings);
      return response;
    } catch {
      setSession(null);
      return null;
    } finally {
      setCheckingSession(false);
    }
  }

  async function loadData(currentSession: AuthSession) {
    const requests: Array<Promise<unknown>> = [
      apiFetch<{ items: CatalogEntry[] }>("/api/catalog"),
      apiFetch<{ items: ExperimentConfig[] }>("/api/experiments"),
      apiFetch<{ items: ReleaseCandidate[] }>("/api/release-candidates"),
      apiFetch<{ items: JobRun[] }>("/api/jobs"),
      apiFetch<{ latest: EvalSummary | null }>("/api/evals/latest"),
      apiFetch<{ latest: CompareSummary | null }>("/api/compare/latest"),
      apiFetch<{ latest: CompatibilitySummary | null }>("/api/compatibility/latest"),
      apiFetch<{ latest: GateSummary | null }>("/api/release-gate/latest"),
      apiFetch<{ latest: ArtifactSummary | null }>("/api/submission/latest"),
      apiFetch<UsageSummary>("/api/usage-events")
    ];

    if (currentSession.user.role === "owner") {
      requests.push(apiFetch<{ items: User[] }>("/api/users"));
      requests.push(apiFetch<{ items: AuditEvent[] }>("/api/audit-logs"));
      requests.push(apiFetch<{ item: InstanceSettings }>("/api/settings"));
    }

    const results = await Promise.all(requests);
    const [
      catalogResponse,
      experimentsResponse,
      releasesResponse,
      jobsResponse,
      evalResponse,
      compareResponse,
      compatibilityResponse,
      gateResponse,
      artifactResponse,
      usageResponse,
      usersResponse,
      auditResponse,
      settingsResponse
    ] = results;

    setCatalog((catalogResponse as { items: CatalogEntry[] }).items);
    setExperiments((experimentsResponse as { items: ExperimentConfig[] }).items);
    setReleaseCandidates((releasesResponse as { items: ReleaseCandidate[] }).items);
    setJobs((jobsResponse as { items: JobRun[] }).items);
    setLatestEval((evalResponse as { latest: EvalSummary | null }).latest);
    setLatestCompare((compareResponse as { latest: CompareSummary | null }).latest);
    setLatestCompatibility(
      (compatibilityResponse as { latest: CompatibilitySummary | null }).latest
    );
    setLatestGate((gateResponse as { latest: GateSummary | null }).latest);
    setLatestArtifact((artifactResponse as { latest: ArtifactSummary | null }).latest);
    setUsageSummary(usageResponse as UsageSummary);

    if (currentSession.user.role === "owner") {
      setUsers((usersResponse as { items: User[] }).items);
      setAuditLogs((auditResponse as { items: AuditEvent[] }).items);
      const item = (settingsResponse as { item: InstanceSettings }).item;
      setSettingsDraft(item);
      setSession((prev) => (prev ? { ...prev, settings: item } : prev));
    } else {
      setUsers([]);
      setAuditLogs([]);
    }
  }

  useEffect(() => {
    void loadSession().then((currentSession) => {
      if (currentSession) {
        void loadData(currentSession).catch((loadError) =>
          setError(loadError instanceof Error ? loadError.message : "데이터를 불러오지 못했습니다.")
        );
      }
    });
  }, []);

  useEffect(() => {
    if (!session) return;

    const interval = window.setInterval(() => {
      void apiFetch<{ items: JobRun[] }>("/api/jobs")
        .then((response) => setJobs(response.items))
        .catch(() => {
          /* ignore polling failures */
        });
    }, 3000);

    return () => window.clearInterval(interval);
  }, [session]);

  async function waitForJob(jobId: string) {
    for (let attempt = 0; attempt < 20; attempt += 1) {
      const response = await apiFetch<{ item: JobRun }>(`/api/jobs/${jobId}`);
      setActiveJobId(jobId);
      if (response.item.status === "completed" || response.item.status === "failed") {
        setMessage(response.item.resultSummaryKo ?? response.item.errorSummary ?? "작업이 끝났습니다.");
        if (session) {
          await loadData(session);
        }
        return response.item;
      }
      await sleep(1000);
    }

    throw new Error("job polling timed out");
  }

  async function handleLogin() {
    setBusy(true);
    setError(null);
    try {
      const nextSession = await apiFetch<AuthSession>("/api/auth/login", {
        method: "POST",
        body: JSON.stringify({
          email: authEmail,
          password: authPassword
        })
      });
      setSession(nextSession);
      setSettingsDraft(nextSession.settings);
      await loadData(nextSession);
      setMessage(`${nextSession.user.name} 계정으로 로그인했습니다.`);
    } catch (loginError) {
      setError(loginError instanceof Error ? loginError.message : "로그인에 실패했습니다.");
    } finally {
      setBusy(false);
    }
  }

  async function handleLogout() {
    await apiFetch("/api/auth/logout", { method: "POST" });
    setSession(null);
    setBaselineRecommendation(null);
    setCandidateRecommendation(null);
    setMessage("로그아웃했습니다.");
  }

  async function runRecommendation(mode: "baseline" | "candidate") {
    setBusy(true);
    setError(null);
    try {
      const result = await apiFetch<RecommendationResult>(
        mode === "baseline" ? "/api/recommendations" : "/api/recommendations/candidate",
        {
          method: "POST",
          body: JSON.stringify({
            query,
            desiredCapabilities,
            preferredCategories: ["ops"],
            environment: {
              locale: session?.settings.defaultLocale ?? "ko-KR",
              clientVersion: session?.settings.defaultClientVersion ?? "1.2.0",
              transport: "stdio",
              platform: "node"
            },
            maxResults: 3
          })
        }
      );

      if (mode === "baseline") {
        setBaselineRecommendation(result);
      } else {
        setCandidateRecommendation(result);
      }
    } catch (recommendError) {
      setError(
        recommendError instanceof Error ? recommendError.message : "추천을 실행하지 못했습니다."
      );
    } finally {
      setBusy(false);
    }
  }

  async function handleJob(name: "eval" | "compare" | "compatibility" | "release-gate" | "artifact-export") {
    setBusy(true);
    setError(null);
    try {
      const payload =
        name === "compare"
          ? { experimentId: selectedExperimentId }
          : name === "compatibility" || name === "release-gate" || name === "artifact-export"
            ? { releaseCandidateId: selectedReleaseCandidateId }
            : {};
      const response = await apiFetch<{ jobId: string; status: string }>(`/api/jobs/${name}`, {
        method: "POST",
        body: JSON.stringify(payload)
      });
      setMessage(`${name} job ${response.jobId}가 등록되었습니다.`);
      await waitForJob(response.jobId);
    } catch (jobError) {
      setError(jobError instanceof Error ? jobError.message : "작업을 실행하지 못했습니다.");
    } finally {
      setBusy(false);
    }
  }

  async function handleSaveCatalog() {
    if (!selectedCatalog) return;
    await apiFetch(`/api/catalog/${selectedCatalog.id}`, {
      method: "PUT",
      body: JSON.stringify({
        ...selectedCatalog,
        summaryKo: catalogSummaryDraft,
        freshnessScore: Number(catalogFreshnessDraft)
      })
    });
    if (session) await loadData(session);
    setMessage("catalog entry를 저장했습니다.");
  }

  async function handleAddCatalog() {
    if (!selectedCatalog) return;
    await apiFetch("/api/catalog", {
      method: "POST",
      body: JSON.stringify(buildSampleCatalogEntry(selectedCatalog, `oss-sample-${Date.now()}`))
    });
    if (session) await loadData(session);
    setMessage("샘플 catalog entry를 추가했습니다.");
  }

  async function handleDeleteCatalog() {
    if (!selectedCatalog) return;
    await apiFetch(`/api/catalog/${selectedCatalog.id}`, { method: "DELETE" });
    if (session) await loadData(session);
    setMessage("catalog entry를 삭제했습니다.");
  }

  async function handleCreateExperiment() {
    await apiFetch("/api/experiments", {
      method: "POST",
      body: JSON.stringify(buildSampleExperiment(`exp-${Date.now()}`))
    });
    if (session) await loadData(session);
    setMessage("실험을 생성했습니다.");
  }

  async function handleToggleExperiment(experiment: ExperimentConfig) {
    await apiFetch(`/api/experiments/${experiment.id}`, {
      method: "PUT",
      body: JSON.stringify({
        ...experiment,
        status: experiment.status === "running" ? "completed" : "running"
      })
    });
    if (session) await loadData(session);
  }

  async function handleDeleteExperiment(experimentId: string) {
    await apiFetch(`/api/experiments/${experimentId}`, { method: "DELETE" });
    if (session) await loadData(session);
  }

  async function handleCreateReleaseCandidate() {
    await apiFetch("/api/release-candidates", {
      method: "POST",
      body: JSON.stringify(
        buildSampleReleaseCandidate(`rc-${Date.now()}`, selectedCatalog?.id ?? "release-check-bot")
      )
    });
    if (session) await loadData(session);
    setMessage("샘플 릴리즈 후보를 생성했습니다.");
  }

  async function handleDeleteReleaseCandidate() {
    await apiFetch(`/api/release-candidates/${selectedReleaseCandidateId}`, { method: "DELETE" });
    if (session) await loadData(session);
  }

  async function handleSaveSettings() {
    if (!settingsDraft) return;
    const response = await apiFetch<{ item: InstanceSettings }>("/api/settings", {
      method: "PUT",
      body: JSON.stringify({
        workspaceName: settingsDraft.workspaceName,
        defaultLocale: settingsDraft.defaultLocale,
        defaultClientVersion: settingsDraft.defaultClientVersion,
        evalMinTop3Recall: settingsDraft.evalMinTop3Recall,
        compareMinUplift: settingsDraft.compareMinUplift
      })
    });
    setSettingsDraft(response.item);
    setSession((prev) => (prev ? { ...prev, settings: response.item } : prev));
    setMessage("인스턴스 설정을 저장했습니다.");
  }

  async function handleCreateUser() {
    await apiFetch("/api/users", {
      method: "POST",
      body: JSON.stringify({
        email: newUserEmail,
        name: newUserName,
        role: newUserRole,
        password: newUserPassword
      })
    });
    if (session) await loadData(session);
    setMessage("사용자를 생성했습니다.");
  }

  async function handleUpdateUser(user: User) {
    await apiFetch(`/api/users/${user.id}`, {
      method: "PUT",
      body: JSON.stringify({
        name: user.name,
        role: user.role,
        password: "",
        isActive: user.isActive
      })
    });
    if (session) await loadData(session);
  }

  async function handleTrackAccept(catalogId: string) {
    await apiFetch("/api/usage-events", {
      method: "POST",
      body: JSON.stringify({
        id: crypto.randomUUID(),
        recommendationRunId: candidateRecommendation?.requestId ?? baselineRecommendation?.requestId ?? "manual",
        catalogId,
        action: "accept",
        actor: "operator",
        createdAt: new Date().toISOString(),
        metadata: { source: "dashboard" }
      })
    });
    if (session) await loadData(session);
  }

  async function handleImportBundle() {
    const bundle = JSON.parse(importBundleText) as CatalogImportBundle;
    await apiFetch("/api/catalog/import", {
      method: "POST",
      body: JSON.stringify(bundle)
    });
    if (session) await loadData(session);
    setMessage("catalog bundle import를 적용했습니다.");
  }

  async function handleExportBundle() {
    const response = await apiFetch<{ item: CatalogImportBundle }>("/api/catalog/export");
    setImportBundleText(JSON.stringify(response.item, null, 2));
    setMessage("catalog bundle을 export했습니다.");
  }

  async function handleImportFile(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file) return;
    setImportBundleText(await file.text());
  }

  if (checkingSession) {
    return (
      <div className="shell">
        <section className="hero">
          <div className="hero-card">
            <span className="pill">Study1 v3 OSS Hardening</span>
            <h1>MCP OSS 운영 콘솔</h1>
            <p>세션을 확인하는 중입니다.</p>
          </div>
        </section>
      </div>
    );
  }

  if (!session) {
    return (
      <div className="shell">
        <section className="hero narrow">
          <div className="hero-card">
            <span className="pill">Study1 v3 OSS Hardening</span>
            <h1>MCP OSS 운영 콘솔 로그인</h1>
            <p>single-team self-hosted 환경에서 catalog, experiments, release gate를 안전하게 운영합니다.</p>
          </div>
          <div className="card">
            <h2>로그인</h2>
            <div className="form">
              <label>
                Email
                <input value={authEmail} onChange={(event) => setAuthEmail(event.target.value)} />
              </label>
              <label>
                Password
                <input
                  type="password"
                  value={authPassword}
                  onChange={(event) => setAuthPassword(event.target.value)}
                />
              </label>
              <button className="button" type="button" disabled={busy} onClick={() => void handleLogin()}>
                로그인
              </button>
              {error ? <p className="metric-note">{error}</p> : null}
              <p className="muted">seed 계정: owner@study1.local / ChangeMe123!</p>
            </div>
          </div>
        </section>
      </div>
    );
  }

  return (
    <div className="shell">
      <section className="hero">
        <div className="hero-card">
          <span className="pill">Study1 v3 OSS Hardening</span>
          <h1>MCP OSS 운영 콘솔</h1>
          <p>
            로그인된 팀이 catalog, experiment, release gate, artifact export를 self-hosted 환경에서
            운영하는 single-workspace 제품화 버전입니다.
          </p>
        </div>
        <div className="hero-grid">
          <div className="card">
            <h2>Workspace</h2>
            <p className="muted">{session.settings.workspaceName}</p>
            <strong>{session.settings.defaultLocale}</strong>
          </div>
          <div className="card">
            <h2>Current User</h2>
            <p className="muted">{session.user.email}</p>
            <strong>{session.user.role}</strong>
          </div>
          <div className="card">
            <h2>Latest Job</h2>
            <p className="muted">{jobs[0]?.name ?? "none"}</p>
            <strong>{jobs[0]?.status ?? "idle"}</strong>
          </div>
        </div>
        <div className="actions" style={{ maxWidth: 1280, margin: "0 auto" }}>
          <button className="button secondary" type="button" onClick={() => void handleLogout()}>
            로그아웃
          </button>
        </div>
      </section>

      <section className="grid">
        <div className="card">
          <h2>Recommendation Ops</h2>
          <div className="form">
            <label>
              추천 질의
              <textarea value={query} onChange={(event) => setQuery(event.target.value)} />
            </label>
            <div className="checkbox-grid">
              {capabilityOptions.map((capability) => (
                <label key={capability} htmlFor={capability}>
                  <input
                    id={capability}
                    type="checkbox"
                    checked={desiredCapabilities.includes(capability)}
                    onChange={(event) =>
                      setDesiredCapabilities((current) =>
                        event.target.checked
                          ? [...current, capability]
                          : current.filter((item) => item !== capability)
                      )
                    }
                  />
                  {capability}
                </label>
              ))}
            </div>
            {canOperate ? (
              <div className="actions">
                <button className="button" type="button" disabled={busy} onClick={() => void runRecommendation("baseline")}>
                  Baseline 실행
                </button>
                <button className="button secondary" type="button" disabled={busy} onClick={() => void runRecommendation("candidate")}>
                  Candidate 실행
                </button>
                <button className="button secondary" type="button" disabled={busy} onClick={() => void handleJob("eval")}>
                  Eval Job
                </button>
                <button className="button secondary" type="button" disabled={busy} onClick={() => void handleJob("compare")}>
                  Compare Job
                </button>
              </div>
            ) : (
              <p className="muted">viewer는 운영 실행 버튼이 비활성화됩니다.</p>
            )}
          </div>

          <div className="hero-grid" style={{ marginTop: 18 }}>
            <div className="card">
              <h3>Baseline</h3>
              {baselineRecommendation?.topCandidates.map((candidate) => (
                <article className="candidate" key={`baseline-${candidate.catalogId}`}>
                  <header>
                    <strong>{candidate.catalogId}</strong>
                    <strong>{candidate.score.toFixed(1)}</strong>
                  </header>
                  <p>{candidate.explanationKo}</p>
                </article>
              )) ?? <p className="muted">아직 baseline 추천이 없습니다.</p>}
            </div>
            <div className="card">
              <h3>Candidate</h3>
              {candidateRecommendation?.topCandidates.map((candidate) => (
                <article className="candidate" key={`candidate-${candidate.catalogId}`}>
                  <header>
                    <strong>{candidate.catalogId}</strong>
                    <strong>{candidate.score.toFixed(1)}</strong>
                  </header>
                  <p>{candidate.explanationKo}</p>
                  {canOperate ? (
                    <div className="actions">
                      <button
                        className="button secondary"
                        type="button"
                        onClick={() => void handleTrackAccept(candidate.catalogId)}
                      >
                        채택 로그 남기기
                      </button>
                    </div>
                  ) : null}
                </article>
              )) ?? <p className="muted">아직 candidate 추천이 없습니다.</p>}
            </div>
          </div>
        </div>

        <div style={{ display: "grid", gap: 18 }}>
          <div className="card">
            <h2>Release Automation</h2>
            <div className="form">
              <label>
                Release Candidate
                <select
                  value={selectedReleaseCandidateId}
                  onChange={(event) => setSelectedReleaseCandidateId(event.target.value)}
                >
                  {releaseCandidates.map((candidate) => (
                    <option key={candidate.id} value={candidate.id}>
                      {candidate.id}
                    </option>
                  ))}
                </select>
              </label>
              {canOperate ? (
                <div className="actions">
                  <button className="button secondary" type="button" disabled={busy} onClick={() => void handleJob("compatibility")}>
                    Compatibility Job
                  </button>
                  <button className="button secondary" type="button" disabled={busy} onClick={() => void handleJob("release-gate")}>
                    Release Gate Job
                  </button>
                  <button className="button secondary" type="button" disabled={busy} onClick={() => void handleJob("artifact-export")}>
                    Artifact Export Job
                  </button>
                </div>
              ) : null}
            </div>

            <div className="stats" style={{ marginTop: 16 }}>
              <div className="stat">
                <span>Latest Compare Uplift</span>
                <strong>{latestCompare?.metrics.uplift.toFixed(3) ?? "-"}</strong>
              </div>
              <div className="stat">
                <span>Compatibility</span>
                <strong>{latestCompatibility ? (latestCompatibility.passed ? "PASS" : "FAIL") : "-"}</strong>
              </div>
              <div className="stat">
                <span>Release Gate</span>
                <strong>{latestGate ? (latestGate.passed ? "PASS" : "FAIL") : "-"}</strong>
              </div>
            </div>
          </div>

          <div className="card">
            <h2>Job Activity</h2>
            <div className="catalog-list">
              {jobs.length ? (
                jobs.map((job) => (
                  <div className="catalog-row" key={job.id}>
                    <div>
                      <strong>
                        {job.name} / {job.status}
                      </strong>
                      <p className="muted">{job.resultSummaryKo ?? job.errorSummary ?? "대기 중"}</p>
                    </div>
                    <div className="catalog-meta">
                      <span className="tag">{job.createdByEmail}</span>
                      {activeJobId === job.id ? <span className="tag">polling</span> : null}
                    </div>
                  </div>
                ))
              ) : (
                <p className="muted">아직 실행한 job이 없습니다.</p>
              )}
            </div>
          </div>

          <div className="card">
            <h2>Usage Totals</h2>
            {usageSummary ? (
              <div className="stats">
                <div className="stat">
                  <span>Impression</span>
                  <strong>{usageSummary.totals.impression}</strong>
                </div>
                <div className="stat">
                  <span>Click</span>
                  <strong>{usageSummary.totals.click}</strong>
                </div>
                <div className="stat">
                  <span>Accept</span>
                  <strong>{usageSummary.totals.accept}</strong>
                </div>
              </div>
            ) : (
              <p className="muted">usage 데이터를 불러오지 못했습니다.</p>
            )}
          </div>
        </div>
      </section>

      <section className="grid" style={{ marginTop: 18 }}>
        <div className="card">
          <h2>Catalog Import/Export</h2>
          <div className="form">
            <div className="actions">
              <button className="button secondary" type="button" onClick={() => void handleExportBundle()}>
                Export Bundle
              </button>
              {canOperate ? (
                <>
                  <label className="file-input">
                    JSON 파일 선택
                    <input type="file" accept="application/json" onChange={(event) => void handleImportFile(event)} />
                  </label>
                  <button className="button" type="button" onClick={() => void handleImportBundle()}>
                    Import Bundle
                  </button>
                </>
              ) : null}
            </div>
            <textarea
              value={importBundleText}
              onChange={(event) => setImportBundleText(event.target.value)}
              placeholder='{"catalogEntries":[...]}'
            />
          </div>
        </div>

        <div className="card">
          <h2>Latest Artifact Preview</h2>
          {latestArtifact ? (
            <pre className="artifact-preview">{latestArtifact.content}</pre>
          ) : (
            <p className="muted">아직 export된 artifact가 없습니다.</p>
          )}
        </div>
      </section>

      <section className="grid" style={{ marginTop: 18 }}>
        <div className="card">
          <h2>Catalog CRUD</h2>
          <div className="form">
            <label>
              Selected Catalog
              <select value={selectedCatalogId} onChange={(event) => setSelectedCatalogId(event.target.value)}>
                {catalog.map((item) => (
                  <option key={item.id} value={item.id}>
                    {item.id}
                  </option>
                ))}
              </select>
            </label>
            <label>
              Summary
              <textarea value={catalogSummaryDraft} onChange={(event) => setCatalogSummaryDraft(event.target.value)} />
            </label>
            <label>
              Freshness
              <input value={catalogFreshnessDraft} onChange={(event) => setCatalogFreshnessDraft(event.target.value)} />
            </label>
            {canOperate ? (
              <div className="actions">
                <button className="button" type="button" onClick={() => void handleSaveCatalog()}>
                  저장
                </button>
                <button className="button secondary" type="button" onClick={() => void handleAddCatalog()}>
                  샘플 MCP 추가
                </button>
                <button className="button secondary" type="button" onClick={() => void handleDeleteCatalog()}>
                  삭제
                </button>
              </div>
            ) : null}
          </div>
        </div>

        <div className="card">
          <h2>Experiment Console</h2>
          <div className="actions">
            {canOperate ? (
              <button className="button" type="button" onClick={() => void handleCreateExperiment()}>
                실험 생성
              </button>
            ) : null}
          </div>
          <div className="catalog-list" style={{ marginTop: 16 }}>
            {experiments.map((experiment) => (
              <div className="catalog-row" key={experiment.id}>
                <div>
                  <strong>{experiment.name}</strong>
                  <p className="muted">{experiment.hypothesisKo}</p>
                </div>
                <div className="catalog-meta">
                  <span className="tag">{experiment.status}</span>
                  <span className="tag">{experiment.trafficSplitPercent}%</span>
                </div>
                {canOperate ? (
                  <div className="actions">
                    <button className="button secondary" type="button" onClick={() => void handleToggleExperiment(experiment)}>
                      상태 토글
                    </button>
                    <button className="button secondary" type="button" onClick={() => void handleDeleteExperiment(experiment.id)}>
                      삭제
                    </button>
                  </div>
                ) : null}
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="grid" style={{ marginTop: 18 }}>
        <div className="card">
          <h2>Release Candidate Console</h2>
          <div className="form">
            <label>
              Selected Release Candidate
              <select
                value={selectedReleaseCandidateId}
                onChange={(event) => setSelectedReleaseCandidateId(event.target.value)}
              >
                {releaseCandidates.map((candidate) => (
                  <option key={candidate.id} value={candidate.id}>
                    {candidate.id}
                  </option>
                ))}
              </select>
            </label>
            {canOperate ? (
              <div className="actions">
                <button className="button" type="button" onClick={() => void handleCreateReleaseCandidate()}>
                  샘플 릴리즈 후보 추가
                </button>
                <button className="button secondary" type="button" onClick={() => void handleDeleteReleaseCandidate()}>
                  삭제
                </button>
              </div>
            ) : null}
          </div>
          <div className="catalog-list" style={{ marginTop: 16 }}>
            {releaseCandidates.map((candidate) => (
              <div className="catalog-row" key={candidate.id}>
                <div>
                  <strong>{candidate.name}</strong>
                  <p className="muted">{candidate.releaseVersion} / {candidate.status}</p>
                </div>
                <div className="catalog-meta">
                  <span className="tag">{candidate.manifestId}</span>
                  <span className="tag">{candidate.targetClientVersion}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="card">
          <h2>Proof Snapshot</h2>
          <div className="stats">
            <div className="stat">
              <span>Eval Top-3 Recall</span>
              <strong>{latestEval ? `${(latestEval.metrics.top3Recall * 100).toFixed(1)}%` : "-"}</strong>
            </div>
            <div className="stat">
              <span>Compare Uplift</span>
              <strong>{latestCompare?.metrics.uplift.toFixed(3) ?? "-"}</strong>
            </div>
            <div className="stat">
              <span>Latest Gate</span>
              <strong>{latestGate ? (latestGate.passed ? "PASS" : "FAIL") : "-"}</strong>
            </div>
          </div>
        </div>
      </section>

      {isOwner ? (
        <section className="grid" style={{ marginTop: 18 }}>
          <div className="card">
            <h2>Instance Settings</h2>
            {settingsDraft ? (
              <div className="form">
                <label>
                  Workspace Name
                  <input
                    value={settingsDraft.workspaceName}
                    onChange={(event) =>
                      setSettingsDraft((current) =>
                        current ? { ...current, workspaceName: event.target.value } : current
                      )
                    }
                  />
                </label>
                <label>
                  Default Locale
                  <input
                    value={settingsDraft.defaultLocale}
                    onChange={(event) =>
                      setSettingsDraft((current) =>
                        current ? { ...current, defaultLocale: event.target.value } : current
                      )
                    }
                  />
                </label>
                <label>
                  Default Client Version
                  <input
                    value={settingsDraft.defaultClientVersion}
                    onChange={(event) =>
                      setSettingsDraft((current) =>
                        current ? { ...current, defaultClientVersion: event.target.value } : current
                      )
                    }
                  />
                </label>
                <label>
                  Eval Min Top-3 Recall
                  <input
                    value={settingsDraft.evalMinTop3Recall}
                    onChange={(event) =>
                      setSettingsDraft((current) =>
                        current
                          ? { ...current, evalMinTop3Recall: Number(event.target.value) }
                          : current
                      )
                    }
                  />
                </label>
                <label>
                  Compare Min Uplift
                  <input
                    value={settingsDraft.compareMinUplift}
                    onChange={(event) =>
                      setSettingsDraft((current) =>
                        current
                          ? { ...current, compareMinUplift: Number(event.target.value) }
                          : current
                      )
                    }
                  />
                </label>
                <button className="button" type="button" onClick={() => void handleSaveSettings()}>
                  설정 저장
                </button>
              </div>
            ) : (
              <p className="muted">설정을 불러오는 중입니다.</p>
            )}
          </div>

          <div className="card">
            <h2>Team Access</h2>
            <div className="form">
              <label>
                Email
                <input value={newUserEmail} onChange={(event) => setNewUserEmail(event.target.value)} />
              </label>
              <label>
                Name
                <input value={newUserName} onChange={(event) => setNewUserName(event.target.value)} />
              </label>
              <label>
                Role
                <select value={newUserRole} onChange={(event) => setNewUserRole(event.target.value as User["role"])}>
                  <option value="owner">owner</option>
                  <option value="operator">operator</option>
                  <option value="viewer">viewer</option>
                </select>
              </label>
              <label>
                Password
                <input
                  type="password"
                  value={newUserPassword}
                  onChange={(event) => setNewUserPassword(event.target.value)}
                />
              </label>
              <button className="button" type="button" onClick={() => void handleCreateUser()}>
                사용자 생성
              </button>
            </div>
            <div className="catalog-list" style={{ marginTop: 16 }}>
              {users.map((user) => (
                <div className="catalog-row" key={user.id}>
                  <div>
                    <strong>{user.name}</strong>
                    <p className="muted">{user.email}</p>
                  </div>
                  <div className="catalog-meta">
                    <span className="tag">{user.role}</span>
                    <span className="tag">{user.isActive ? "active" : "inactive"}</span>
                  </div>
                  <div className="actions">
                    <button
                      className="button secondary"
                      type="button"
                      onClick={() =>
                        void handleUpdateUser({
                          ...user,
                          role: user.role === "viewer" ? "operator" : user.role === "operator" ? "owner" : "viewer"
                        })
                      }
                    >
                      역할 변경
                    </button>
                    <button
                      className="button secondary"
                      type="button"
                      onClick={() => void handleUpdateUser({ ...user, isActive: !user.isActive })}
                    >
                      활성 토글
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
      ) : null}

      {isOwner ? (
        <section className="grid" style={{ marginTop: 18 }}>
          <div className="card">
            <h2>Audit Log</h2>
            <div className="catalog-list">
              {auditLogs.map((event) => (
                <div className="catalog-row" key={event.id}>
                  <div>
                    <strong>{event.action}</strong>
                    <p className="muted">{event.detailKo}</p>
                  </div>
                  <div className="catalog-meta">
                    <span className="tag">{event.actorEmail ?? "system"}</span>
                    <span className="tag">{event.targetType}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
          <div className="card">
            <h2>Status</h2>
            {message ? <p>{message}</p> : <p className="muted">최근 작업 메시지가 없습니다.</p>}
            {error ? <p className="metric-note">{error}</p> : null}
          </div>
        </section>
      ) : (
        <section className="grid" style={{ marginTop: 18 }}>
          <div className="card">
            <h2>Status</h2>
            {message ? <p>{message}</p> : <p className="muted">최근 작업 메시지가 없습니다.</p>}
            {error ? <p className="metric-note">{error}</p> : null}
          </div>
        </section>
      )}
    </div>
  );
}
