import { type OfflineEvalCase, offlineEvalCaseSchema } from "./contracts";

const rawEvalCases: OfflineEvalCase[] = [
  {
    id: "eval-release-checks",
    title: "릴리즈 체크리스트와 changeset 검증",
    query: "배포 전에 changeset 상태와 릴리즈 체크리스트를 같이 확인하고 싶어요",
    desiredCapabilities: ["release-management", "changesets", "changelog"],
    preferredCategories: ["ops"],
    expectedTopIds: ["release-check-bot", "package-registry-guard"],
    forbiddenIds: ["figma-design-context"],
    requiredReasonTypes: ["capabilityMatch", "differentiation", "compatibility"],
    environment: {
      locale: "ko-KR",
      clientVersion: "1.2.0",
      transport: "stdio",
      platform: "node"
    },
    notesKo: "릴리즈 운영 흐름에서 가장 중요한 기준 케이스"
  },
  {
    id: "eval-semver-compat",
    title: "semver 호환성 점검",
    query: "패키지 버전 범위와 semver 충돌을 검토해야 해요",
    desiredCapabilities: ["semver", "compatibility", "dependency-graph"],
    preferredCategories: ["ops"],
    expectedTopIds: ["package-registry-guard", "release-check-bot"],
    forbiddenIds: ["customer-support-faq"],
    requiredReasonTypes: ["capabilityMatch", "compatibility"],
    environment: {
      locale: "ko-KR",
      clientVersion: "1.2.0",
      transport: "http",
      platform: "node"
    },
    notesKo: "호환성 중심 질의는 package registry guard가 먼저 와야 한다"
  },
  {
    id: "eval-korean-docs",
    title: "한국어 문서 검색",
    query: "한글 운영 문서와 위키에서 근거 구간을 빠르게 찾고 싶습니다",
    desiredCapabilities: ["document-search", "korean-search", "reference"],
    preferredCategories: ["docs"],
    expectedTopIds: ["korean-docs-search", "notion-knowledge-sync"],
    forbiddenIds: ["browser-workflow-runner"],
    requiredReasonTypes: ["capabilityMatch", "differentiation"],
    environment: {
      locale: "ko-KR",
      clientVersion: "1.2.0",
      transport: "http",
      platform: "hybrid"
    },
    notesKo: "한국어 문서 탐색이 강한 MCP를 우선 노출해야 한다"
  },
  {
    id: "eval-github-review",
    title: "GitHub 코드 리뷰 준비",
    query: "PR 리뷰 전에 저장소 구조와 commit diff를 같이 보고 싶어요",
    desiredCapabilities: ["git", "pull-request", "diff-analysis"],
    preferredCategories: ["code"],
    expectedTopIds: ["github-repo-inspector"],
    forbiddenIds: ["customer-support-faq"],
    requiredReasonTypes: ["capabilityMatch", "differentiation", "compatibility"],
    environment: {
      locale: "ko-KR",
      clientVersion: "1.1.0",
      transport: "stdio",
      platform: "node"
    },
    notesKo: "코드 리뷰형 질의에서 GitHub 도메인 특화 MCP가 1위여야 한다"
  },
  {
    id: "eval-postgres-migration",
    title: "Postgres 마이그레이션 검토",
    query: "PostgreSQL 테이블 관계와 마이그레이션 위험을 먼저 보고 싶습니다",
    desiredCapabilities: ["database", "schema", "migration"],
    preferredCategories: ["data"],
    expectedTopIds: ["postgres-schema-mapper"],
    forbiddenIds: ["figma-design-context"],
    requiredReasonTypes: ["capabilityMatch", "differentiation"],
    environment: {
      locale: "ko-KR",
      clientVersion: "1.2.0",
      transport: "http",
      platform: "node"
    },
    notesKo: "데이터 모델 탐색은 schema mapper가 우선된다"
  },
  {
    id: "eval-browser-demo",
    title: "브라우저 데모 검증",
    query: "로그인 흐름을 브라우저에서 재현하고 스크린샷도 남기고 싶어요",
    desiredCapabilities: ["browser", "workflow", "screenshot"],
    preferredCategories: ["browser"],
    expectedTopIds: ["browser-workflow-runner"],
    forbiddenIds: ["package-registry-guard"],
    requiredReasonTypes: ["capabilityMatch", "differentiation"],
    environment: {
      locale: "ko-KR",
      clientVersion: "1.2.0",
      transport: "http",
      platform: "hybrid"
    },
    notesKo: "브라우저 재현형 요청은 workflow runner가 1위여야 한다"
  },
  {
    id: "eval-design-handoff",
    title: "디자인 핸드오프",
    query: "Figma 노드와 코드 컴포넌트를 같이 보고 싶습니다",
    desiredCapabilities: ["figma", "component-map", "screenshot"],
    preferredCategories: ["design"],
    expectedTopIds: ["figma-design-context"],
    forbiddenIds: ["server-log-analyzer"],
    requiredReasonTypes: ["capabilityMatch", "compatibility"],
    environment: {
      locale: "ko-KR",
      clientVersion: "1.0.0",
      transport: "stdio",
      platform: "hybrid"
    },
    notesKo: "디자인 문맥 질의는 figma MCP가 맞아야 한다"
  },
  {
    id: "eval-slack-ops",
    title: "운영 알림 연결",
    query: "Slack에서 운영 알림과 승인 요청을 같이 다루고 싶어요",
    desiredCapabilities: ["slack", "alert", "approval"],
    preferredCategories: ["communication", "ops"],
    expectedTopIds: ["slack-ops-bridge"],
    forbiddenIds: ["customer-support-faq"],
    requiredReasonTypes: ["capabilityMatch", "differentiation"],
    environment: {
      locale: "ko-KR",
      clientVersion: "1.2.0",
      transport: "http",
      platform: "hybrid"
    },
    notesKo: "운영 알림 흐름은 slack ops bridge가 잘 맞는다"
  },
  {
    id: "eval-notion-sync",
    title: "노션 운영 문서 갱신",
    query: "운영 문서와 체크리스트를 Notion에서 바로 업데이트하고 싶어요",
    desiredCapabilities: ["notion", "page-update", "comment"],
    preferredCategories: ["productivity", "docs"],
    expectedTopIds: ["notion-knowledge-sync", "korean-docs-search"],
    forbiddenIds: ["server-log-analyzer"],
    requiredReasonTypes: ["capabilityMatch", "differentiation"],
    environment: {
      locale: "ko-KR",
      clientVersion: "1.2.0",
      transport: "http",
      platform: "hybrid"
    },
    notesKo: "운영 문서 갱신은 notion sync가 가장 적절하다"
  },
  {
    id: "eval-support-faq",
    title: "고객지원 FAQ 검색",
    query: "한국어 FAQ와 정책 문서를 함께 검색해서 고객지원 답변을 준비하고 싶어요",
    desiredCapabilities: ["faq", "support", "policy"],
    preferredCategories: ["support", "docs"],
    expectedTopIds: ["customer-support-faq", "korean-docs-search"],
    forbiddenIds: ["release-check-bot"],
    requiredReasonTypes: ["capabilityMatch", "differentiation"],
    environment: {
      locale: "ko-KR",
      clientVersion: "1.2.0",
      transport: "http",
      platform: "hybrid"
    },
    notesKo: "고객지원형 질의는 support FAQ가 앞서야 한다"
  },
  {
    id: "eval-analytics",
    title: "비교 차트 생성",
    query: "실험 전후 지표를 차트와 한글 요약으로 정리하고 싶어요",
    desiredCapabilities: ["chart", "analytics", "compare"],
    preferredCategories: ["analytics"],
    expectedTopIds: ["data-visualization-studio"],
    forbiddenIds: ["github-repo-inspector"],
    requiredReasonTypes: ["capabilityMatch", "differentiation"],
    environment: {
      locale: "ko-KR",
      clientVersion: "1.2.0",
      transport: "http",
      platform: "hybrid"
    },
    notesKo: "분석 리포트 질의는 visualization studio가 잘 맞는다"
  },
  {
    id: "eval-log-analysis",
    title: "로그 기반 장애 분석",
    query: "서버 로그 패턴과 에러 원인을 한국어로 빠르게 보고 싶습니다",
    desiredCapabilities: ["logs", "error-analysis", "pattern"],
    preferredCategories: ["ops"],
    expectedTopIds: ["server-log-analyzer", "slack-ops-bridge"],
    forbiddenIds: ["figma-design-context"],
    requiredReasonTypes: ["capabilityMatch", "differentiation", "compatibility"],
    environment: {
      locale: "ko-KR",
      clientVersion: "1.2.0",
      transport: "stdio",
      platform: "node"
    },
    notesKo: "장애 로그 요약은 server log analyzer가 우선된다"
  }
];

export const offlineEvalCases = rawEvalCases.map((item) => offlineEvalCaseSchema.parse(item));
