"use client";

import type {
  ArtifactExport,
  CatalogEntry,
  CompatibilityReport,
  ExperimentConfig,
  RecommendationResult,
  ReleaseCandidate,
  ReleaseGateReport
} from "@study1-v0/shared";
import React, { useEffect, useMemo, useState } from "react";

const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:3102";

type EvalSummary = {
  id: string;
  metrics: {
    top3Recall: number;
    explanationCompleteness: number;
    forbiddenHitRate: number;
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
    cache: "no-store"
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }

  return (await response.json()) as T;
}

function buildSampleCatalogEntry(seed: CatalogEntry, id: string): CatalogEntry {
  return {
    ...seed,
    id,
    slug: id,
    name: `Submission ${seed.name}`,
    version: "1.0.0",
    summaryKo: `${seed.summaryKo} submission polish 실험용 엔트리`,
    descriptionKo: `${seed.descriptionKo} submission polish 단계에서 catalog CRUD와 compatibility gate를 검증하기 위한 엔트리입니다.`,
    exposure: {
      ...seed.exposure,
      userFacingSummaryKo: `${seed.exposure.userFacingSummaryKo} (submission demo)`
    }
  };
}

function buildSampleReleaseCandidate(seed: CatalogEntry): ReleaseCandidate {
  const timestamp = Date.now();
  return {
    id: `rc-${seed.id}-${timestamp}`,
    name: `${seed.id} release candidate`,
    manifestId: seed.id,
    previousVersion: seed.version,
    releaseVersion: seed.version,
    targetClientVersion: seed.compatibility.testedClientVersions[0] ?? "1.2.0",
    releaseNotesKo:
      "변경 요약: submission demo 기준의 dry-run release candidate를 생성했습니다.\n검증: eval, compare, compatibility, release gate를 다시 실행합니다.\n리스크: tested version 밖 런타임은 별도 확인이 필요합니다.",
    requiredDocs: [
      "docs/README.md",
      "docs/runbook.md",
      "docs/eval-proof.md",
      "docs/compare-report.md",
      "docs/compatibility-report.md",
      "docs/release-gate-proof.md",
      "docs/korean-market-fit.md"
    ],
    requiredArtifacts: [
      ".changeset/config.json",
      ".changeset/mcp-v2-demo.md",
      "../../../../.github/workflows/mcp-v2-dry-run.yml"
    ],
    deprecatedFieldsUsed: [],
    owner: "dashboard-operator",
    status: "candidate",
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  };
}

export function MpcDashboard() {
  const [catalog, setCatalog] = useState<CatalogEntry[]>([]);
  const [experiments, setExperiments] = useState<ExperimentConfig[]>([]);
  const [releaseCandidates, setReleaseCandidates] = useState<ReleaseCandidate[]>([]);
  const [baselineRecommendation, setBaselineRecommendation] = useState<RecommendationResult | null>(
    null
  );
  const [candidateRecommendation, setCandidateRecommendation] = useState<RecommendationResult | null>(
    null
  );
  const [latestEval, setLatestEval] = useState<EvalSummary | null>(null);
  const [latestCompare, setLatestCompare] = useState<CompareSummary | null>(null);
  const [usageSummary, setUsageSummary] = useState<UsageSummary | null>(null);
  const [latestCompatibility, setLatestCompatibility] = useState<CompatibilityReport | null>(null);
  const [latestGate, setLatestGate] = useState<ReleaseGateReport | null>(null);
  const [latestArtifact, setLatestArtifact] = useState<ArtifactExport | null>(null);
  const [query, setQuery] = useState("배포 전에 manifest 호환성과 changeset 릴리즈 체크를 같이 보고 싶어요");
  const [desiredCapabilities, setDesiredCapabilities] = useState<string[]>([
    "release-management",
    "changesets",
    "semver"
  ]);
  const [selectedCatalogId, setSelectedCatalogId] = useState("release-check-bot");
  const [catalogSummaryDraft, setCatalogSummaryDraft] = useState("");
  const [catalogFreshnessDraft, setCatalogFreshnessDraft] = useState("0.95");
  const [experimentName, setExperimentName] = useState("submission-rerank-ko");
  const [experimentHypothesis, setExperimentHypothesis] = useState(
    "feedback와 usage signal을 유지한 채 release gate까지 붙이면 운영 증빙이 매끄럽다."
  );
  const [feedbackCatalogId, setFeedbackCatalogId] = useState("release-check-bot");
  const [feedbackNote, setFeedbackNote] = useState("submission-ready gate까지 이어지는 설명이 깔끔했습니다.");
  const [feedbackDelta, setFeedbackDelta] = useState("2");
  const [selectedReleaseCandidateId, setSelectedReleaseCandidateId] = useState(
    "rc-release-check-bot-1-5-0"
  );
  const [releaseVersionDraft, setReleaseVersionDraft] = useState("1.5.0");
  const [releaseOwnerDraft, setReleaseOwnerDraft] = useState("release-ops");
  const [releaseNotesDraft, setReleaseNotesDraft] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const selectedCatalog = useMemo(
    () => catalog.find((item) => item.id === selectedCatalogId) ?? null,
    [catalog, selectedCatalogId]
  );
  const selectedReleaseCandidate = useMemo(
    () => releaseCandidates.find((item) => item.id === selectedReleaseCandidateId) ?? null,
    [releaseCandidates, selectedReleaseCandidateId]
  );

  useEffect(() => {
    if (selectedCatalog) {
      setCatalogSummaryDraft(selectedCatalog.summaryKo);
      setCatalogFreshnessDraft(String(selectedCatalog.freshnessScore));
    }
  }, [selectedCatalog]);

  useEffect(() => {
    if (selectedReleaseCandidate) {
      setReleaseVersionDraft(selectedReleaseCandidate.releaseVersion);
      setReleaseOwnerDraft(selectedReleaseCandidate.owner);
      setReleaseNotesDraft(selectedReleaseCandidate.releaseNotesKo);
    }
  }, [selectedReleaseCandidate]);

  async function loadAll() {
    const [
      catalogResponse,
      evalResponse,
      compareResponse,
      experimentResponse,
      usageResponse,
      releaseCandidateResponse,
      compatibilityResponse,
      gateResponse,
      artifactResponse
    ] = await Promise.all([
      apiFetch<{ items: CatalogEntry[] }>("/api/catalog"),
      apiFetch<{ latest: EvalSummary | null }>("/api/evals/latest"),
      apiFetch<{ latest: CompareSummary | null }>("/api/compare/latest"),
      apiFetch<{ items: ExperimentConfig[] }>("/api/experiments"),
      apiFetch<UsageSummary>("/api/usage-events"),
      apiFetch<{ items: ReleaseCandidate[] }>("/api/release-candidates"),
      apiFetch<{ latest: CompatibilityReport | null }>("/api/compatibility/latest"),
      apiFetch<{ latest: ReleaseGateReport | null }>("/api/release-gate/latest"),
      apiFetch<{ latest: ArtifactExport | null }>("/api/submission/latest")
    ]);

    setCatalog(catalogResponse.items);
    setLatestEval(evalResponse.latest);
    setLatestCompare(compareResponse.latest);
    setExperiments(experimentResponse.items);
    setUsageSummary(usageResponse);
    setReleaseCandidates(releaseCandidateResponse.items);
    setLatestCompatibility(compatibilityResponse.latest);
    setLatestGate(gateResponse.latest);
    setLatestArtifact(artifactResponse.latest);
  }

  useEffect(() => {
    void loadAll().catch((loadError) => {
      setError(loadError instanceof Error ? loadError.message : "초기 데이터를 불러오지 못했습니다.");
    });
  }, []);

  async function runRecommendation(mode: "baseline" | "candidate") {
    setLoading(true);
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
              locale: "ko-KR",
              clientVersion: "1.2.0",
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
      setLoading(false);
    }
  }

  async function runEvalAndCompare() {
    setLoading(true);
    setError(null);
    try {
      const [evalSummary, compareSummary] = await Promise.all([
        apiFetch<EvalSummary>("/api/evals/run", { method: "POST", body: JSON.stringify({}) }),
        apiFetch<CompareSummary>("/api/compare/run", {
          method: "POST",
          body: JSON.stringify({ experimentId: experiments[0]?.id })
        })
      ]);

      setLatestEval(evalSummary);
      setLatestCompare(compareSummary);
    } catch (actionError) {
      setError(actionError instanceof Error ? actionError.message : "평가/비교를 실행하지 못했습니다.");
    } finally {
      setLoading(false);
    }
  }

  async function submitFeedback() {
    setLoading(true);
    setError(null);
    try {
      await apiFetch("/api/feedback", {
        method: "POST",
        body: JSON.stringify({
          id: crypto.randomUUID(),
          recommendationRunId:
            candidateRecommendation?.requestId ?? baselineRecommendation?.requestId ?? "manual",
          catalogId: feedbackCatalogId,
          scoreDelta: Number(feedbackDelta),
          noteKo: feedbackNote,
          reviewer: "dashboard-operator",
          createdAt: new Date().toISOString()
        })
      });

      await loadAll();
    } catch (feedbackError) {
      setError(feedbackError instanceof Error ? feedbackError.message : "피드백을 저장하지 못했습니다.");
    } finally {
      setLoading(false);
    }
  }

  async function trackAccept(catalogId: string) {
    await apiFetch("/api/usage-events", {
      method: "POST",
      body: JSON.stringify({
        id: crypto.randomUUID(),
        recommendationRunId:
          candidateRecommendation?.requestId ?? baselineRecommendation?.requestId ?? "manual",
        catalogId,
        action: "accept",
        actor: "operator",
        createdAt: new Date().toISOString(),
        metadata: { source: "dashboard" }
      })
    });
    await loadAll();
  }

  async function saveExperiment() {
    setLoading(true);
    setError(null);
    try {
      await apiFetch("/api/experiments", {
        method: "POST",
        body: JSON.stringify({
          id: `exp-${experimentName.replace(/[^a-z0-9]+/gi, "-").toLowerCase()}`,
          name: experimentName,
          baselineStrategy: "weighted-baseline-v0",
          candidateStrategy: "signal-rerank-v1",
          trafficSplitPercent: 50,
          status: "draft",
          hypothesisKo: experimentHypothesis
        })
      });
      await loadAll();
    } finally {
      setLoading(false);
    }
  }

  async function toggleExperiment(experiment: ExperimentConfig) {
    await apiFetch(`/api/experiments/${experiment.id}`, {
      method: "PUT",
      body: JSON.stringify({
        ...experiment,
        status: experiment.status === "running" ? "completed" : "running"
      })
    });
    await loadAll();
  }

  async function removeExperiment(experimentId: string) {
    await apiFetch(`/api/experiments/${experimentId}`, { method: "DELETE" });
    await loadAll();
  }

  async function saveCatalog() {
    if (!selectedCatalog) return;
    await apiFetch(`/api/catalog/${selectedCatalog.id}`, {
      method: "PUT",
      body: JSON.stringify({
        ...selectedCatalog,
        summaryKo: catalogSummaryDraft,
        freshnessScore: Number(catalogFreshnessDraft)
      })
    });
    await loadAll();
  }

  async function createCatalog() {
    const seed = selectedCatalog ?? catalog[0];
    if (!seed) return;
    await apiFetch("/api/catalog", {
      method: "POST",
      body: JSON.stringify(buildSampleCatalogEntry(seed, `submission-${Date.now()}`))
    });
    await loadAll();
  }

  async function removeCatalog() {
    if (!selectedCatalog) return;
    await apiFetch(`/api/catalog/${selectedCatalog.id}`, { method: "DELETE" });
    setSelectedCatalogId("release-check-bot");
    await loadAll();
  }

  async function saveReleaseCandidate() {
    if (!selectedReleaseCandidate) return;
    await apiFetch(`/api/release-candidates/${selectedReleaseCandidate.id}`, {
      method: "PUT",
      body: JSON.stringify({
        ...selectedReleaseCandidate,
        releaseVersion: releaseVersionDraft,
        owner: releaseOwnerDraft,
        releaseNotesKo: releaseNotesDraft,
        updatedAt: new Date().toISOString()
      })
    });
    await loadAll();
  }

  async function createReleaseCandidate() {
    const seed = selectedCatalog ?? catalog[0];
    if (!seed) return;
    await apiFetch("/api/release-candidates", {
      method: "POST",
      body: JSON.stringify(buildSampleReleaseCandidate(seed))
    });
    await loadAll();
  }

  async function removeReleaseCandidate() {
    if (!selectedReleaseCandidate) return;
    await apiFetch(`/api/release-candidates/${selectedReleaseCandidate.id}`, {
      method: "DELETE"
    });
    setSelectedReleaseCandidateId("rc-release-check-bot-1-5-0");
    await loadAll();
  }

  async function runReleaseWorkflow() {
    if (!selectedReleaseCandidate) return;
    setLoading(true);
    setError(null);
    try {
      const [evalSummary, compareSummary] = await Promise.all([
        apiFetch<EvalSummary>("/api/evals/run", { method: "POST", body: JSON.stringify({}) }),
        apiFetch<CompareSummary>("/api/compare/run", {
          method: "POST",
          body: JSON.stringify({ experimentId: experiments[0]?.id })
        })
      ]);
      const compatibility = await apiFetch<CompatibilityReport>("/api/compatibility/run", {
        method: "POST",
        body: JSON.stringify({ releaseCandidateId: selectedReleaseCandidate.id })
      });
      const gate = await apiFetch<ReleaseGateReport>("/api/release-gate/run", {
        method: "POST",
        body: JSON.stringify({ releaseCandidateId: selectedReleaseCandidate.id })
      });
      const artifact = await apiFetch<ArtifactExport>("/api/submission/export", {
        method: "POST",
        body: JSON.stringify({ releaseCandidateId: selectedReleaseCandidate.id })
      });

      setLatestEval(evalSummary);
      setLatestCompare(compareSummary);
      setLatestCompatibility(compatibility);
      setLatestGate(gate);
      setLatestArtifact(artifact);
    } catch (workflowError) {
      setError(
        workflowError instanceof Error
          ? workflowError.message
          : "release workflow를 실행하지 못했습니다."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="shell">
      <section className="hero">
        <div className="hero-card">
          <span className="pill">Study1 v2 Submission Polish</span>
          <h1>MCP 제출 운영 콘솔</h1>
          <p>
            reranking 운영 콘솔 위에 compatibility gate, release gate, submission artifact export를
            올려 submission-ready 데모로 마감한 화면입니다.
          </p>
        </div>
        <div className="hero-grid">
          <div className="card">
            <h2>Submission Gate</h2>
            <p className="muted">offline eval, compare uplift, semver/compatibility, docs artifact를 한 번에 봅니다.</p>
          </div>
          <div className="card">
            <h2>CRUD 범위</h2>
            <p className="muted">catalog, experiment, release candidate를 모두 이 콘솔에서 수정할 수 있습니다.</p>
          </div>
        </div>
      </section>

      <section className="grid">
        <div className="card">
          <h2>추천 실험</h2>
          <div className="form">
            <label>
              추천 질의
              <textarea value={query} onChange={(event) => setQuery(event.target.value)} />
            </label>
            <div className="checkbox-grid">
              {["release-management", "changesets", "semver", "document-search", "notion", "logs"].map(
                (capability) => (
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
                )
              )}
            </div>
            <div className="actions">
              <button className="button" type="button" onClick={() => void runRecommendation("baseline")}>
                Baseline 실행
              </button>
              <button
                className="button secondary"
                type="button"
                onClick={() => void runRecommendation("candidate")}
              >
                Candidate 실행
              </button>
              <button className="button secondary" type="button" onClick={() => void runEvalAndCompare()}>
                Compare 갱신
              </button>
            </div>
            {error ? <p className="metric-note">{error}</p> : null}
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
              )) ?? <p className="muted">아직 baseline을 실행하지 않았습니다.</p>}
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
                  <div className="actions">
                    <button
                      className="button secondary"
                      type="button"
                      onClick={() => void trackAccept(candidate.catalogId)}
                    >
                      채택 로그 남기기
                    </button>
                  </div>
                </article>
              )) ?? <p className="muted">아직 candidate를 실행하지 않았습니다.</p>}
            </div>
          </div>
        </div>

        <div style={{ display: "grid", gap: 18 }}>
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
              <p className="muted">usage log를 불러오는 중입니다.</p>
            )}
          </div>

          <div className="card">
            <h2>Compare Snapshot</h2>
            {latestCompare ? (
              <div className="stats">
                <div className="stat">
                  <span>Baseline nDCG@3</span>
                  <strong>{latestCompare.metrics.baselineNdcg3.toFixed(3)}</strong>
                </div>
                <div className="stat">
                  <span>Candidate nDCG@3</span>
                  <strong>{latestCompare.metrics.candidateNdcg3.toFixed(3)}</strong>
                </div>
                <div className="stat">
                  <span>Uplift</span>
                  <strong>{latestCompare.metrics.uplift.toFixed(3)}</strong>
                </div>
              </div>
            ) : (
              <p className="muted">아직 compare 결과가 없습니다.</p>
            )}
            {latestEval ? (
              <p className="muted" style={{ marginTop: 12 }}>
                latest eval top3 recall {(latestEval.metrics.top3Recall * 100).toFixed(1)}%
              </p>
            ) : null}
          </div>

          <div className="card">
            <h2>Feedback Loop</h2>
            <div className="form">
              <label>
                Catalog
                <select value={feedbackCatalogId} onChange={(event) => setFeedbackCatalogId(event.target.value)}>
                  {catalog.map((item) => (
                    <option key={item.id} value={item.id}>
                      {item.id}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                Score Delta
                <input value={feedbackDelta} onChange={(event) => setFeedbackDelta(event.target.value)} />
              </label>
              <label>
                Note
                <textarea value={feedbackNote} onChange={(event) => setFeedbackNote(event.target.value)} />
              </label>
              <button className="button" type="button" onClick={() => void submitFeedback()}>
                피드백 저장
              </button>
            </div>
          </div>
        </div>
      </section>

      <section className="grid" style={{ marginTop: 18 }}>
        <div className="card">
          <h2>Experiment Console</h2>
          <div className="form">
            <label>
              Experiment Name
              <input value={experimentName} onChange={(event) => setExperimentName(event.target.value)} />
            </label>
            <label>
              Hypothesis
              <textarea value={experimentHypothesis} onChange={(event) => setExperimentHypothesis(event.target.value)} />
            </label>
            <button className="button" type="button" onClick={() => void saveExperiment()}>
              실험 생성
            </button>
          </div>
          <div className="catalog-list" style={{ marginTop: 18 }}>
            {experiments.map((experiment) => (
              <div className="catalog-row" key={experiment.id}>
                <strong>{experiment.name}</strong>
                <p className="muted">{experiment.hypothesisKo}</p>
                <div className="actions">
                  <button className="button secondary" type="button" onClick={() => void toggleExperiment(experiment)}>
                    상태 토글
                  </button>
                  <button className="button secondary" type="button" onClick={() => void removeExperiment(experiment.id)}>
                    삭제
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

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
            <div className="actions">
              <button className="button" type="button" onClick={() => void saveCatalog()}>
                저장
              </button>
              <button className="button secondary" type="button" onClick={() => void createCatalog()}>
                샘플 MCP 추가
              </button>
              <button className="button secondary" type="button" onClick={() => void removeCatalog()}>
                삭제
              </button>
            </div>
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
            <label>
              Release Version
              <input value={releaseVersionDraft} onChange={(event) => setReleaseVersionDraft(event.target.value)} />
            </label>
            <label>
              Owner
              <input value={releaseOwnerDraft} onChange={(event) => setReleaseOwnerDraft(event.target.value)} />
            </label>
            <label>
              Release Notes
              <textarea value={releaseNotesDraft} onChange={(event) => setReleaseNotesDraft(event.target.value)} />
            </label>
            <div className="actions">
              <button className="button" type="button" onClick={() => void saveReleaseCandidate()}>
                릴리즈 후보 저장
              </button>
              <button className="button secondary" type="button" onClick={() => void createReleaseCandidate()}>
                릴리즈 후보 추가
              </button>
              <button className="button secondary" type="button" onClick={() => void removeReleaseCandidate()}>
                릴리즈 후보 삭제
              </button>
            </div>
          </div>

          <div className="catalog-list" style={{ marginTop: 18 }}>
            {releaseCandidates.map((candidate) => (
              <div className="catalog-row" key={candidate.id}>
                <strong>{candidate.name}</strong>
                <p className="muted">
                  {candidate.manifestId} · {candidate.releaseVersion} · {candidate.status}
                </p>
              </div>
            ))}
          </div>
        </div>

        <div style={{ display: "grid", gap: 18 }}>
          <div className="card">
            <h2>Release Quality</h2>
            <div className="actions">
              <button className="button" type="button" onClick={() => void runReleaseWorkflow()} disabled={loading}>
                Release Gate 실행
              </button>
            </div>
            <div className="stats" style={{ marginTop: 16 }}>
              <div className="stat">
                <span>Compatibility</span>
                <strong>{latestCompatibility?.passed ? "PASS" : "PENDING"}</strong>
              </div>
              <div className="stat">
                <span>Release Gate</span>
                <strong>{latestGate?.passed ? "PASS" : "PENDING"}</strong>
              </div>
              <div className="stat">
                <span>Artifact</span>
                <strong>{latestArtifact ? latestArtifact.format.toUpperCase() : "NONE"}</strong>
              </div>
            </div>
            {latestCompatibility ? (
              <p className="muted" style={{ marginTop: 12 }}>
                compatibility issues {latestCompatibility.issues.length}
              </p>
            ) : null}
            {latestGate ? (
              <p className="muted">
                gate uplift {(latestGate.metrics.uplift * 100).toFixed(1)}%, top3 recall{" "}
                {(latestGate.metrics.top3Recall * 100).toFixed(1)}%
              </p>
            ) : null}
          </div>

          <div className="card">
            <h2>Submission Artifact Preview</h2>
            {latestArtifact ? (
              <pre className="metric-note" style={{ whiteSpace: "pre-wrap" }}>
                {latestArtifact.content}
              </pre>
            ) : (
              <p className="muted">아직 export된 artifact가 없습니다.</p>
            )}
          </div>
        </div>
      </section>
    </div>
  );
}
