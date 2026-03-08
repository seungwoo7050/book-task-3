"use client";

import type { CatalogEntry, RecommendationResult } from "@study1-v0/shared";
import React, { useEffect, useState } from "react";

const capabilityOptions = [
  "release-management",
  "semver",
  "document-search",
  "git",
  "database",
  "browser",
  "notion",
  "slack",
  "logs",
  "chart",
  "faq"
];

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
  cases: Array<{
    caseId: string;
    topIds: string[];
    matchedExpected: string[];
    forbiddenHits: string[];
    explanationPass: boolean;
  }>;
};

const apiBaseUrl =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:3100";

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

export function MpcDashboard() {
  const [catalog, setCatalog] = useState<CatalogEntry[]>([]);
  const [recommendation, setRecommendation] = useState<RecommendationResult | null>(null);
  const [latestEval, setLatestEval] = useState<EvalSummary | null>(null);
  const [query, setQuery] = useState("배포 전에 manifest 호환성과 changeset 릴리즈 체크를 같이 보고 싶어요");
  const [desiredCapabilities, setDesiredCapabilities] = useState<string[]>([
    "release-management",
    "semver"
  ]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadInitial() {
      try {
        const [catalogResponse, evalResponse] = await Promise.all([
          apiFetch<{ items: CatalogEntry[] }>("/api/catalog"),
          apiFetch<{ latest: EvalSummary | null }>("/api/evals/latest")
        ]);

        setCatalog(catalogResponse.items);
        setLatestEval(evalResponse.latest);
      } catch (loadError) {
        setError(loadError instanceof Error ? loadError.message : "초기 데이터를 불러오지 못했습니다.");
      }
    }

    void loadInitial();
  }, []);

  async function handleRecommend() {
    setLoading(true);
    setError(null);

    try {
      const result = await apiFetch<RecommendationResult>("/api/recommendations", {
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
      });

      setRecommendation(result);
    } catch (recommendError) {
      setError(
        recommendError instanceof Error ? recommendError.message : "추천을 실행하지 못했습니다."
      );
    } finally {
      setLoading(false);
    }
  }

  async function handleRunEval() {
    setLoading(true);
    setError(null);

    try {
      const summary = await apiFetch<EvalSummary>("/api/evals/run", {
        method: "POST",
        body: JSON.stringify({})
      });

      setLatestEval(summary);
    } catch (evalError) {
      setError(evalError instanceof Error ? evalError.message : "평가를 실행하지 못했습니다.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="shell">
      <section className="hero">
        <div className="hero-card">
          <span className="pill">Study1 v0 Initial Demo</span>
          <h1>MCP 추천 운영 데모</h1>
          <p>
            registry seed, manifest validation, baseline selector, 한국어 추천 근거, offline eval을
            한 화면에서 확인하는 deterministic 추천 데모입니다.
          </p>
        </div>
        <div className="hero-grid">
          <div className="card">
            <h2>v0 최소 약속</h2>
            <p className="muted">manifest 유효성, 카탈로그 조회, 추천 trace, 오프라인 평가를 바로 재현합니다.</p>
          </div>
          <div className="card">
            <h2>운영 설명 포인트</h2>
            <p className="muted">capability, differentiation, compatibility 세 축으로 한국어 추천 이유를 고정합니다.</p>
          </div>
        </div>
      </section>

      <section className="grid">
        <div className="card">
          <h2>추천 실행</h2>
          <p className="muted">릴리즈/호환성 질의가 기본값으로 들어 있습니다. capability를 바꿔 다른 추천을 시도해 보세요.</p>
          <div className="form">
            <label>
              추천 질의
              <textarea value={query} onChange={(event) => setQuery(event.target.value)} />
            </label>

            <div>
              <strong>Desired capabilities</strong>
              <div className="checkbox-grid">
                {capabilityOptions.map((capability) => (
                  <label key={capability} htmlFor={capability}>
                    <input
                      id={capability}
                      type="checkbox"
                      checked={desiredCapabilities.includes(capability)}
                      onChange={(event) => {
                        setDesiredCapabilities((current) =>
                          event.target.checked
                            ? [...current, capability]
                            : current.filter((item) => item !== capability)
                        );
                      }}
                    />
                    {capability}
                  </label>
                ))}
              </div>
            </div>

            <div className="actions">
              <button className="button" type="button" onClick={handleRecommend} disabled={loading}>
                추천 실행
              </button>
              <button
                className="button secondary"
                type="button"
                onClick={handleRunEval}
                disabled={loading}
              >
                오프라인 평가 실행
              </button>
            </div>

            {error ? <p className="metric-note">{error}</p> : null}
          </div>

          {recommendation ? (
            <div className="recommendation-list" style={{ marginTop: 18 }}>
              {recommendation.topCandidates.map((candidate) => {
                const entry = catalog.find((item) => item.id === candidate.catalogId);
                return (
                  <article className="candidate" key={candidate.catalogId}>
                    <header>
                      <div>
                        <strong>
                          #{candidate.rank} {candidate.catalogId}
                        </strong>
                        <small>{entry?.summaryKo}</small>
                      </div>
                      <strong>{candidate.score.toFixed(1)}</strong>
                    </header>
                    <p>{candidate.explanationKo}</p>
                    <div className="tags">
                      {candidate.trace.reasons.slice(0, 3).map((reason) => (
                        <span className="tag" key={`${candidate.catalogId}-${reason.type}`}>
                          {reason.type}
                        </span>
                      ))}
                    </div>
                  </article>
                );
              })}
            </div>
          ) : null}
        </div>

        <div style={{ display: "grid", gap: 18 }}>
          <div className="card">
            <h2>오프라인 평가</h2>
            {latestEval ? (
              <>
                <div className="stats">
                  <div className="stat">
                    <span>Top-3 recall</span>
                    <strong>{(latestEval.metrics.top3Recall * 100).toFixed(1)}%</strong>
                  </div>
                  <div className="stat">
                    <span>Explanation completeness</span>
                    <strong>{(latestEval.metrics.explanationCompleteness * 100).toFixed(1)}%</strong>
                  </div>
                  <div className="stat">
                    <span>Forbidden hit rate</span>
                    <strong>{(latestEval.metrics.forbiddenHitRate * 100).toFixed(1)}%</strong>
                  </div>
                </div>
                <p className="muted" style={{ marginTop: 12 }}>
                  acceptance: top3 {String(latestEval.acceptance.top3RecallPass)}, explanation{" "}
                  {String(latestEval.acceptance.explanationPass)}, forbidden{" "}
                  {String(latestEval.acceptance.forbiddenPass)}
                </p>
              </>
            ) : (
              <p className="muted">아직 평가를 실행하지 않았습니다.</p>
            )}
          </div>

          <div className="card">
            <h2>카탈로그 샘플</h2>
            <div className="catalog-list">
              {catalog.slice(0, 6).map((entry) => (
                <div className="catalog-row" key={entry.id}>
                  <div>
                    <strong>{entry.name}</strong>
                    <p className="muted">{entry.summaryKo}</p>
                  </div>
                  <div className="catalog-meta">
                    <span className="tag">{entry.toolCategory}</span>
                    <span className="tag">maturity {entry.maturity.score}</span>
                    <span className="tag">{entry.operational.releaseChannel}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
