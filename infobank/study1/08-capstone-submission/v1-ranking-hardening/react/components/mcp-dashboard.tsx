"use client";

import type { CatalogEntry, ExperimentConfig, RecommendationResult } from "@study1-v0/shared";
import React, { useEffect, useMemo, useState } from "react";

const apiBaseUrl =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:3101";

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
    name: `Signal ${seed.name}`,
    version: "1.0.0",
    summaryKo: `${seed.summaryKo} signal-rerank 실험용 변형 엔트리`,
    descriptionKo: `${seed.descriptionKo} signal-rerank 실험에서 catalog CRUD 흐름을 확인하기 위한 샘플 엔트리입니다.`,
    exposure: {
      ...seed.exposure,
      userFacingSummaryKo: `${seed.exposure.userFacingSummaryKo} (실험용)`
    }
  };
}

export function MpcDashboard() {
  const [catalog, setCatalog] = useState<CatalogEntry[]>([]);
  const [experiments, setExperiments] = useState<ExperimentConfig[]>([]);
  const [baselineRecommendation, setBaselineRecommendation] = useState<RecommendationResult | null>(
    null
  );
  const [candidateRecommendation, setCandidateRecommendation] = useState<RecommendationResult | null>(
    null
  );
  const [latestEval, setLatestEval] = useState<EvalSummary | null>(null);
  const [latestCompare, setLatestCompare] = useState<CompareSummary | null>(null);
  const [usageSummary, setUsageSummary] = useState<UsageSummary | null>(null);
  const [query, setQuery] = useState("배포 전에 manifest 호환성과 changeset 릴리즈 체크를 같이 보고 싶어요");
  const [desiredCapabilities, setDesiredCapabilities] = useState<string[]>([
    "release-management",
    "changesets",
    "semver"
  ]);
  const [selectedCatalogId, setSelectedCatalogId] = useState<string>("release-check-bot");
  const [catalogSummaryDraft, setCatalogSummaryDraft] = useState("");
  const [catalogFreshnessDraft, setCatalogFreshnessDraft] = useState("0.95");
  const [experimentName, setExperimentName] = useState("signal-rerank-ko");
  const [experimentHypothesis, setExperimentHypothesis] = useState(
    "usage + feedback 신호를 넣으면 top1 정렬이 좋아진다."
  );
  const [feedbackCatalogId, setFeedbackCatalogId] = useState("release-check-bot");
  const [feedbackNote, setFeedbackNote] = useState("candidate 정렬이 더 납득 가능했습니다.");
  const [feedbackDelta, setFeedbackDelta] = useState("2");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const selectedCatalog = useMemo(
    () => catalog.find((item) => item.id === selectedCatalogId) ?? null,
    [catalog, selectedCatalogId]
  );

  useEffect(() => {
    if (selectedCatalog) {
      setCatalogSummaryDraft(selectedCatalog.summaryKo);
      setCatalogFreshnessDraft(String(selectedCatalog.freshnessScore));
    }
  }, [selectedCatalog]);

  async function loadAll() {
    const [catalogResponse, evalResponse, compareResponse, experimentResponse, usageResponse] =
      await Promise.all([
        apiFetch<{ items: CatalogEntry[] }>("/api/catalog"),
        apiFetch<{ latest: EvalSummary | null }>("/api/evals/latest"),
        apiFetch<{ latest: CompareSummary | null }>("/api/compare/latest"),
        apiFetch<{ items: ExperimentConfig[] }>("/api/experiments"),
        apiFetch<UsageSummary>("/api/usage-events")
      ]);

    setCatalog(catalogResponse.items);
    setLatestEval(evalResponse.latest);
    setLatestCompare(compareResponse.latest);
    setExperiments(experimentResponse.items);
    setUsageSummary(usageResponse);
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
          recommendationRunId: candidateRecommendation?.requestId ?? baselineRecommendation?.requestId ?? "manual",
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
        recommendationRunId: candidateRecommendation?.requestId ?? baselineRecommendation?.requestId ?? "manual",
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
      body: JSON.stringify(buildSampleCatalogEntry(seed, `signal-${Date.now()}`))
    });
    await loadAll();
  }

  async function removeCatalog() {
    if (!selectedCatalog) return;
    await apiFetch(`/api/catalog/${selectedCatalog.id}`, { method: "DELETE" });
    setSelectedCatalogId("release-check-bot");
    await loadAll();
  }

  return (
    <div className="shell">
      <section className="hero">
        <div className="hero-card">
          <span className="pill">Study1 v1 Ranking Hardening</span>
          <h1>MCP 실험 콘솔</h1>
          <p>
            baseline selector 위에 usage logs, feedback loop, candidate reranker를 얹고
            baseline/candidate compare를 운영자 시점에서 확인합니다.
          </p>
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
                    <button className="button secondary" type="button" onClick={() => void trackAccept(candidate.catalogId)}>
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
    </div>
  );
}
