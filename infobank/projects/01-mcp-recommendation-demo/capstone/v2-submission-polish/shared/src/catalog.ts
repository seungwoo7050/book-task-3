import { type CatalogEntry, catalogEntrySchema } from "./contracts";

const rawCatalog: CatalogEntry[] = [
  {
    id: "github-repo-inspector",
    slug: "github-repo-inspector",
    name: "GitHub Repo Inspector",
    version: "1.4.0",
    toolCategory: "code",
    summaryKo: "GitHub 저장소 구조와 PR/commit 변화를 근거까지 함께 보여주는 코드 탐색 MCP",
    descriptionKo:
      "저장소 구조, PR, commit diff, 코드 소유자 단서를 함께 묶어 코드 변경 영향과 리뷰 포인트를 빠르게 파악하게 돕습니다.",
    capabilities: ["git", "repository", "pull-request", "code-search", "diff-analysis"],
    koreanUseCases: ["PR 리뷰 준비", "레거시 저장소 구조 파악", "변경 영향 범위 확인"],
    differentiationPoints: [
      "PR과 commit 근거를 같은 응답에 묶어 보여줍니다.",
      "코드 소유자와 변경 히스토리를 함께 노출해 리뷰 준비 시간을 줄입니다."
    ],
    supportedLocales: ["ko-KR", "en-US"],
    runtime: {
      protocolVersion: "1.0",
      nodeRange: ">=20 <26",
      transports: ["stdio", "http"],
      platforms: ["node", "hybrid"]
    },
    maturity: { stage: "production", score: 90 },
    compatibility: {
      minimumClientVersion: "1.0.0",
      maximumClientVersion: "2.0.0",
      testedClientVersions: ["1.0.0", "1.1.0", "1.2.0"],
      deprecatedClientVersions: [],
      breakingChanges: []
    },
    operational: {
      maintainer: "Platform Engineering",
      slaTier: "business",
      securityReview: true,
      releaseChannel: "stable"
    },
    tags: ["코드", "깃허브", "리뷰"],
    freshnessScore: 0.84,
    exposure: {
      userFacingSummaryKo: "코드 변경 이유와 근거를 바로 보여주는 저장소 분석기",
      recommendedFor: ["코드 리뷰 준비", "레거시 구조 파악"],
      cautionKo: "private repo 권한이 필요합니다."
    }
  },
  {
    id: "postgres-schema-mapper",
    slug: "postgres-schema-mapper",
    name: "Postgres Schema Mapper",
    version: "1.3.2",
    toolCategory: "data",
    summaryKo: "PostgreSQL 스키마, 테이블 관계, 마이그레이션 후보를 정리하는 데이터 MCP",
    descriptionKo:
      "테이블 구조, 외래키 관계, 쿼리 샘플을 한 번에 정리해 데이터 탐색과 마이그레이션 검토를 빠르게 수행할 수 있게 돕습니다.",
    capabilities: ["sql", "database", "schema", "migration", "query-analysis"],
    koreanUseCases: ["DB 구조 탐색", "마이그레이션 전 영향 검토", "데이터 모델 문서화"],
    differentiationPoints: [
      "테이블 관계와 쿼리 예시를 함께 보여줍니다.",
      "마이그레이션 위험 포인트를 한국어 메모로 정리합니다."
    ],
    supportedLocales: ["ko-KR", "en-US"],
    runtime: {
      protocolVersion: "1.0",
      nodeRange: ">=20 <26",
      transports: ["stdio", "http"],
      platforms: ["node", "hybrid"]
    },
    maturity: { stage: "validated", score: 86 },
    compatibility: {
      minimumClientVersion: "1.0.0",
      maximumClientVersion: "2.0.0",
      testedClientVersions: ["1.0.0", "1.2.0"],
      deprecatedClientVersions: [],
      breakingChanges: []
    },
    operational: {
      maintainer: "Data Platform",
      slaTier: "business",
      securityReview: true,
      releaseChannel: "stable"
    },
    tags: ["데이터", "postgres", "스키마"],
    freshnessScore: 0.78,
    exposure: {
      userFacingSummaryKo: "스키마 관계와 마이그레이션 위험을 한 번에 보는 데이터 도우미",
      recommendedFor: ["DB 점검", "마이그레이션 검토"],
      cautionKo: "읽기 전용 계정 연결을 권장합니다."
    }
  },
  {
    id: "korean-docs-search",
    slug: "korean-docs-search",
    name: "Korean Docs Search",
    version: "1.1.5",
    toolCategory: "docs",
    summaryKo: "한국어 기술 문서와 사내 위키를 자연어로 탐색하는 문서 검색 MCP",
    descriptionKo:
      "한국어 질의와 문서 제목, 섹션 요약, 관련 링크를 함께 반환해 운영자와 개발자가 빠르게 문서 근거를 찾게 합니다.",
    capabilities: ["document-search", "wiki", "korean-search", "knowledge-base", "reference"],
    koreanUseCases: ["사내 위키 검색", "운영 문서 근거 찾기", "한글 문서 탐색"],
    differentiationPoints: [
      "한국어 질의어를 그대로 유지한 채 관련 섹션 요약을 제공합니다.",
      "운영 문서 링크와 근거 문장을 함께 노출해 설명 가능성을 높입니다."
    ],
    supportedLocales: ["ko-KR"],
    runtime: {
      protocolVersion: "1.0",
      nodeRange: ">=20 <26",
      transports: ["stdio", "http"],
      platforms: ["node", "hybrid"]
    },
    maturity: { stage: "production", score: 92 },
    compatibility: {
      minimumClientVersion: "1.0.0",
      maximumClientVersion: "2.0.0",
      testedClientVersions: ["1.0.0", "1.1.0", "1.2.0"],
      deprecatedClientVersions: [],
      breakingChanges: []
    },
    operational: {
      maintainer: "Knowledge Ops",
      slaTier: "business",
      securityReview: true,
      releaseChannel: "stable"
    },
    tags: ["문서", "한국어", "검색"],
    freshnessScore: 0.91,
    exposure: {
      userFacingSummaryKo: "한국어 기술 문서의 근거 구간을 바로 찾는 검색 MCP",
      recommendedFor: ["한국어 문서 검색", "운영 근거 확인"],
      cautionKo: "색인 지연 시 최신 문서가 늦게 반영될 수 있습니다."
    }
  },
  {
    id: "browser-workflow-runner",
    slug: "browser-workflow-runner",
    name: "Browser Workflow Runner",
    version: "1.2.1",
    toolCategory: "browser",
    summaryKo: "브라우저 기반 검증, 로그인 흐름 재현, 폼 점검을 자동화하는 MCP",
    descriptionKo:
      "브라우저 자동화와 스크린샷 캡처를 함께 제공해 운영 시나리오 재현과 UI 회귀 점검에 적합합니다.",
    capabilities: ["browser", "workflow", "screenshot", "automation", "qa"],
    koreanUseCases: ["UI 회귀 점검", "로그인 흐름 재현", "운영 화면 데모 검증"],
    differentiationPoints: [
      "스크린샷과 단계 로그를 함께 남겨 운영 설명에 유리합니다.",
      "재현 시나리오를 한국어 체크리스트로 저장할 수 있습니다."
    ],
    supportedLocales: ["ko-KR", "en-US"],
    runtime: {
      protocolVersion: "1.0",
      nodeRange: ">=20 <26",
      transports: ["stdio", "http"],
      platforms: ["node", "hybrid"]
    },
    maturity: { stage: "validated", score: 82 },
    compatibility: {
      minimumClientVersion: "1.0.0",
      maximumClientVersion: "2.0.0",
      testedClientVersions: ["1.0.0", "1.2.0"],
      deprecatedClientVersions: [],
      breakingChanges: []
    },
    operational: {
      maintainer: "QA Enablement",
      slaTier: "business",
      securityReview: true,
      releaseChannel: "stable"
    },
    tags: ["브라우저", "자동화", "qa"],
    freshnessScore: 0.73,
    exposure: {
      userFacingSummaryKo: "브라우저 시나리오를 캡처와 함께 재현하는 QA MCP",
      recommendedFor: ["브라우저 데모", "회귀 점검"],
      cautionKo: "인증이 필요한 환경은 별도 비밀값 주입이 필요합니다."
    }
  },
  {
    id: "figma-design-context",
    slug: "figma-design-context",
    name: "Figma Design Context",
    version: "1.0.4",
    toolCategory: "design",
    summaryKo: "Figma 노드와 디자인 문맥을 코드 구현 단위로 매핑하는 MCP",
    descriptionKo:
      "디자인 노드, 스크린샷, 컴포넌트 후보를 함께 반환해 디자인-코드 연결 작업을 단축합니다.",
    capabilities: ["figma", "design", "component-map", "screenshot", "handoff"],
    koreanUseCases: ["디자인 핸드오프", "컴포넌트 맵핑", "스크린샷 확인"],
    differentiationPoints: [
      "노드 컨텍스트와 코드 후보를 같이 보여줍니다.",
      "디자인 근거 스크린샷을 함께 남겨 리뷰 설명에 유리합니다."
    ],
    supportedLocales: ["ko-KR", "en-US"],
    runtime: {
      protocolVersion: "1.0",
      nodeRange: ">=20 <26",
      transports: ["stdio", "http"],
      platforms: ["node", "hybrid"]
    },
    maturity: { stage: "validated", score: 79 },
    compatibility: {
      minimumClientVersion: "1.0.0",
      maximumClientVersion: "2.0.0",
      testedClientVersions: ["1.0.0", "1.2.0"],
      deprecatedClientVersions: [],
      breakingChanges: []
    },
    operational: {
      maintainer: "Design Systems",
      slaTier: "community",
      securityReview: false,
      releaseChannel: "preview"
    },
    tags: ["figma", "디자인", "핸드오프"],
    freshnessScore: 0.67,
    exposure: {
      userFacingSummaryKo: "디자인 노드를 코드 구현 맥락으로 연결하는 Figma MCP",
      recommendedFor: ["디자인 컨텍스트 확인", "컴포넌트 맵핑"],
      cautionKo: "preview 채널 기능은 문서화가 불완전할 수 있습니다."
    }
  },
  {
    id: "slack-ops-bridge",
    slug: "slack-ops-bridge",
    name: "Slack Ops Bridge",
    version: "1.2.3",
    toolCategory: "communication",
    summaryKo: "Slack 채널, 알림, 운영 액션을 연결하는 커뮤니케이션 MCP",
    descriptionKo:
      "운영 알림, 승인 요청, 채널 검색을 하나의 인터페이스로 제공해 운영자 액션 연결을 빠르게 수행합니다.",
    capabilities: ["slack", "alert", "approval", "chatops", "search"],
    koreanUseCases: ["장애 알림 확인", "승인 요청 전파", "운영 채널 검색"],
    differentiationPoints: [
      "알림과 승인 액션을 같은 흐름으로 묶어 보여줍니다.",
      "운영용 채널 컨텍스트를 바로 검색해 후속 조치를 줄입니다."
    ],
    supportedLocales: ["ko-KR", "en-US"],
    runtime: {
      protocolVersion: "1.0",
      nodeRange: ">=20 <26",
      transports: ["stdio", "http"],
      platforms: ["node", "hybrid"]
    },
    maturity: { stage: "production", score: 87 },
    compatibility: {
      minimumClientVersion: "1.0.0",
      maximumClientVersion: "2.0.0",
      testedClientVersions: ["1.0.0", "1.2.0"],
      deprecatedClientVersions: [],
      breakingChanges: []
    },
    operational: {
      maintainer: "SRE",
      slaTier: "mission-critical",
      securityReview: true,
      releaseChannel: "stable"
    },
    tags: ["슬랙", "운영", "알림"],
    freshnessScore: 0.8,
    exposure: {
      userFacingSummaryKo: "운영 알림과 승인 요청을 연결하는 Slack MCP",
      recommendedFor: ["장애 대응", "알림 연결"],
      cautionKo: "워크스페이스 승인 범위를 확인해야 합니다."
    }
  },
  {
    id: "notion-knowledge-sync",
    slug: "notion-knowledge-sync",
    name: "Notion Knowledge Sync",
    version: "1.1.2",
    toolCategory: "productivity",
    summaryKo: "Notion 페이지, 데이터베이스, 코멘트를 운영 흐름과 연결하는 지식 관리 MCP",
    descriptionKo:
      "페이지 검색과 업데이트, 데이터베이스 조회를 함께 제공해 운영 문서와 작업 상태를 빠르게 연결합니다.",
    capabilities: ["notion", "page-update", "database-query", "comment", "knowledge-sync"],
    koreanUseCases: ["운영 문서 업데이트", "체크리스트 유지", "노션 데이터 조회"],
    differentiationPoints: [
      "페이지 업데이트와 댓글 흐름을 한 번에 다룹니다.",
      "운영 메모와 상태 업데이트를 같은 응답으로 묶어줍니다."
    ],
    supportedLocales: ["ko-KR", "en-US"],
    runtime: {
      protocolVersion: "1.0",
      nodeRange: ">=20 <26",
      transports: ["stdio", "http"],
      platforms: ["node", "hybrid"]
    },
    maturity: { stage: "production", score: 88 },
    compatibility: {
      minimumClientVersion: "1.0.0",
      maximumClientVersion: "2.0.0",
      testedClientVersions: ["1.0.0", "1.2.0"],
      deprecatedClientVersions: [],
      breakingChanges: []
    },
    operational: {
      maintainer: "Knowledge Ops",
      slaTier: "business",
      securityReview: true,
      releaseChannel: "stable"
    },
    tags: ["노션", "문서", "운영"],
    freshnessScore: 0.83,
    exposure: {
      userFacingSummaryKo: "운영 문서와 상태 관리를 Notion에서 바로 이어주는 MCP",
      recommendedFor: ["운영 문서화", "체크리스트 관리"],
      cautionKo: "권한이 없는 페이지는 조회되지 않습니다."
    }
  },
  {
    id: "release-check-bot",
    slug: "release-check-bot",
    name: "Release Check Bot",
    version: "1.5.0",
    toolCategory: "ops",
    summaryKo: "Changesets, changelog, 릴리즈 체크리스트를 함께 점검하는 배포 운영 MCP",
    descriptionKo:
      "changeset 상태, changelog 누락, 릴리즈 후보 체크리스트를 한 흐름으로 묶어 dry-run 배포 검증을 돕습니다.",
    capabilities: [
      "release-management",
      "changesets",
      "changelog",
      "semver",
      "compatibility",
      "manifest-validation",
      "ci",
      "approval"
    ],
    koreanUseCases: ["릴리즈 후보 점검", "changeset 검증", "manifest 호환성 확인", "배포 승인 체크"],
    differentiationPoints: [
      "changeset 상태와 릴리즈 체크리스트를 같이 보여줍니다.",
      "dry-run 배포 증빙용 로그를 바로 남길 수 있습니다."
    ],
    supportedLocales: ["ko-KR", "en-US"],
    runtime: {
      protocolVersion: "1.0",
      nodeRange: ">=20 <26",
      transports: ["stdio", "http"],
      platforms: ["node", "hybrid"]
    },
    maturity: { stage: "production", score: 94 },
    compatibility: {
      minimumClientVersion: "1.0.0",
      maximumClientVersion: "2.0.0",
      testedClientVersions: ["1.0.0", "1.1.0", "1.2.0"],
      deprecatedClientVersions: [],
      breakingChanges: []
    },
    operational: {
      maintainer: "Release Engineering",
      slaTier: "mission-critical",
      securityReview: true,
      releaseChannel: "stable"
    },
    tags: ["릴리즈", "changesets", "운영", "manifest", "compatibility"],
    freshnessScore: 0.95,
    exposure: {
      userFacingSummaryKo: "changeset과 릴리즈 체크리스트를 함께 검증하는 배포 MCP",
      recommendedFor: ["릴리즈 점검", "changeset 검증"],
      cautionKo: "실제 publish는 수행하지 않고 dry-run만 지원합니다."
    }
  },
  {
    id: "package-registry-guard",
    slug: "package-registry-guard",
    name: "Package Registry Guard",
    version: "1.2.4",
    toolCategory: "ops",
    summaryKo: "패키지 버전 범위와 semver 충돌을 검증하는 호환성 점검 MCP",
    descriptionKo:
      "패키지 버전 범위, peer dependency, semver breaking 가능성을 빠르게 요약해 릴리즈 전 호환성 점검에 유리합니다.",
    capabilities: ["semver", "package-registry", "compatibility", "dependency-graph", "release-management"],
    koreanUseCases: ["semver 점검", "패키지 호환성 확인", "릴리즈 전 버전 검토"],
    differentiationPoints: [
      "semver 충돌과 peer dependency 위험을 함께 보여줍니다.",
      "호환성 근거를 패키지별로 나눠 설명해 릴리즈 판단이 쉽습니다."
    ],
    supportedLocales: ["ko-KR", "en-US"],
    runtime: {
      protocolVersion: "1.0",
      nodeRange: ">=20 <26",
      transports: ["stdio", "http"],
      platforms: ["node", "hybrid"]
    },
    maturity: { stage: "production", score: 91 },
    compatibility: {
      minimumClientVersion: "1.0.0",
      maximumClientVersion: "2.0.0",
      testedClientVersions: ["1.0.0", "1.1.0", "1.2.0"],
      deprecatedClientVersions: [],
      breakingChanges: []
    },
    operational: {
      maintainer: "Release Engineering",
      slaTier: "business",
      securityReview: true,
      releaseChannel: "stable"
    },
    tags: ["semver", "호환성", "패키지"],
    freshnessScore: 0.89,
    exposure: {
      userFacingSummaryKo: "semver 충돌과 패키지 호환성을 빠르게 검증하는 MCP",
      recommendedFor: ["호환성 점검", "패키지 릴리즈 검토"],
      cautionKo: "사설 레지스트리는 별도 인증이 필요합니다."
    }
  },
  {
    id: "customer-support-faq",
    slug: "customer-support-faq",
    name: "Customer Support FAQ",
    version: "1.0.9",
    toolCategory: "support",
    summaryKo: "한국어 고객지원 FAQ와 정책 문서를 검색하는 지원 MCP",
    descriptionKo:
      "정책 문서와 FAQ를 함께 조회해 고객지원 질의에 대한 근거 기반 답변 초안을 빠르게 준비합니다.",
    capabilities: ["faq", "support", "policy", "korean-search", "reference"],
    koreanUseCases: ["고객지원 정책 확인", "한글 FAQ 검색", "지원 문서 근거 확인"],
    differentiationPoints: [
      "FAQ와 정책 문서를 같이 찾아 근거를 강화합니다.",
      "고객지원 표현을 한국어 톤으로 정리해 바로 활용하기 쉽습니다."
    ],
    supportedLocales: ["ko-KR"],
    runtime: {
      protocolVersion: "1.0",
      nodeRange: ">=20 <26",
      transports: ["stdio", "http"],
      platforms: ["node", "hybrid"]
    },
    maturity: { stage: "validated", score: 80 },
    compatibility: {
      minimumClientVersion: "1.0.0",
      maximumClientVersion: "2.0.0",
      testedClientVersions: ["1.0.0", "1.2.0"],
      deprecatedClientVersions: [],
      breakingChanges: []
    },
    operational: {
      maintainer: "Customer Ops",
      slaTier: "business",
      securityReview: true,
      releaseChannel: "stable"
    },
    tags: ["faq", "고객지원", "정책"],
    freshnessScore: 0.74,
    exposure: {
      userFacingSummaryKo: "한국어 FAQ와 정책 문서를 같이 찾는 지원 MCP",
      recommendedFor: ["고객지원 답변 준비", "정책 확인"],
      cautionKo: "최신 공지 반영 전에는 사람 검토가 필요합니다."
    }
  },
  {
    id: "data-visualization-studio",
    slug: "data-visualization-studio",
    name: "Data Visualization Studio",
    version: "1.1.1",
    toolCategory: "analytics",
    summaryKo: "지표를 차트와 간단한 서술로 요약하는 분석 MCP",
    descriptionKo:
      "기본 차트 생성과 지표 요약을 함께 제공해 운영 실험 비교와 리뷰 자료 준비를 빠르게 돕습니다.",
    capabilities: ["chart", "analytics", "dashboard", "report", "compare"],
    koreanUseCases: ["실험 지표 시각화", "운영 리포트 정리", "비교 차트 생성"],
    differentiationPoints: [
      "차트와 요약 서술을 동시에 제공합니다.",
      "비교 실험의 전후 차이를 한글 요약으로 정리합니다."
    ],
    supportedLocales: ["ko-KR", "en-US"],
    runtime: {
      protocolVersion: "1.0",
      nodeRange: ">=20 <26",
      transports: ["stdio", "http"],
      platforms: ["node", "hybrid"]
    },
    maturity: { stage: "validated", score: 81 },
    compatibility: {
      minimumClientVersion: "1.0.0",
      maximumClientVersion: "2.0.0",
      testedClientVersions: ["1.0.0", "1.2.0"],
      deprecatedClientVersions: [],
      breakingChanges: []
    },
    operational: {
      maintainer: "Analytics Platform",
      slaTier: "community",
      securityReview: false,
      releaseChannel: "stable"
    },
    tags: ["차트", "분석", "대시보드"],
    freshnessScore: 0.72,
    exposure: {
      userFacingSummaryKo: "지표를 차트와 한글 요약으로 묶는 분석 MCP",
      recommendedFor: ["지표 비교", "리포트 작성"],
      cautionKo: "대량 데이터는 사전 집계가 필요합니다."
    }
  },
  {
    id: "server-log-analyzer",
    slug: "server-log-analyzer",
    name: "Server Log Analyzer",
    version: "1.3.0",
    toolCategory: "ops",
    summaryKo: "서버 로그와 에러 패턴을 요약하는 운영 로그 MCP",
    descriptionKo:
      "로그 패턴, 에러 빈도, 관련 서비스명을 함께 묶어 장애 분석의 첫 단계를 빠르게 지원합니다.",
    capabilities: ["logs", "error-analysis", "alert", "pattern", "ops"],
    koreanUseCases: ["장애 1차 분석", "로그 패턴 확인", "서비스 오류 요약"],
    differentiationPoints: [
      "에러 패턴과 영향 서비스를 같이 보여줍니다.",
      "운영자 설명용 한국어 요약을 함께 제공합니다."
    ],
    supportedLocales: ["ko-KR", "en-US"],
    runtime: {
      protocolVersion: "1.0",
      nodeRange: ">=20 <26",
      transports: ["stdio", "http"],
      platforms: ["node", "hybrid"]
    },
    maturity: { stage: "production", score: 89 },
    compatibility: {
      minimumClientVersion: "1.0.0",
      maximumClientVersion: "2.0.0",
      testedClientVersions: ["1.0.0", "1.2.0"],
      deprecatedClientVersions: [],
      breakingChanges: []
    },
    operational: {
      maintainer: "SRE",
      slaTier: "mission-critical",
      securityReview: true,
      releaseChannel: "stable"
    },
    tags: ["로그", "운영", "장애"],
    freshnessScore: 0.87,
    exposure: {
      userFacingSummaryKo: "로그 패턴과 에러 원인을 빠르게 요약하는 운영 MCP",
      recommendedFor: ["장애 분석", "로그 점검"],
      cautionKo: "민감정보 마스킹 정책을 먼저 확인해야 합니다."
    }
  }
];

export const catalogSeeds = rawCatalog.map((entry) => catalogEntrySchema.parse(entry));
