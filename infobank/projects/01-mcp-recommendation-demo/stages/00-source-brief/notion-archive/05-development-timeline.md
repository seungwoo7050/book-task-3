> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Source Brief — 개발 타임라인

## 1단계: 모노레포 초기화

```bash
mkdir -p mcp-recommendation-demo
cd mcp-recommendation-demo
pnpm init
```

### pnpm workspace 설정

```bash
cat > pnpm-workspace.yaml << 'EOF'
packages:
  - "shared"
  - "08-capstone-submission/*/shared"
  - "08-capstone-submission/*/node"
  - "08-capstone-submission/*/react"
EOF
```

pnpm workspace를 쓰는 이유: shared/ 패키지를 모든 capstone 버전에서 공유하기 위해서다.

## 2단계: shared/ 패키지 생성

```bash
mkdir -p shared/src
cd shared
pnpm init
```

### TypeScript 설정

```bash
pnpm add -D typescript
cat > tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "strict": true,
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "declaration": true,
    "outDir": "dist"
  },
  "include": ["src"]
}
EOF
```

### Zod 설치

```bash
pnpm add zod
```

Zod를 선택한 이유: TypeScript 타입과 런타임 검증을 동시에 제공한다.
JSON Schema나 io-ts보다 API가 직관적이다.

## 3단계: contracts.ts 작성

```bash
touch shared/src/contracts.ts
```

Zod 스키마 정의 순서:
1. `mcpManifestSchema` — 도구 메타데이터 (name, version, category, inputs, outputs)
2. `catalogEntrySchema` — catalog 항목 (manifest + 한국어 노출 + status)
3. `recommendationRequestSchema` — 추천 요청 (query, context, limit)
4. `reasonTraceSchema` — 추천 근거 추적 (도구 선택 이유)
5. `recommendationTraceSchema` — 전체 추천 기록
6. `offlineEvalCaseSchema` — 오프라인 평가 케이스

## 4단계: catalog.ts 작성

```bash
touch shared/src/catalog.ts
```

10+ MCP 도구를 seed 데이터로 정의했다.
각 도구에 한국어 exposure 필드를 포함시켰다.

## 5단계: eval.ts 작성

```bash
touch shared/src/eval.ts
```

offline eval case를 정의했다:
- release checks, semver compatibility, korean docs 등 다양한 시나리오
- 각 case에 기대 도구 ID와 순위를 포함

## 6단계: reference 문서 작성

```bash
mkdir -p docs
touch docs/reference-spine.md
touch docs/project-selection-rationale.md
```

## 7단계: stage 디렉터리 스캐폴딩

```bash
for i in $(seq -w 0 8); do
  mkdir -p "${i}-*/"{problem,docs}
done
```

당시에는 별도 스캐폴딩 스크립트로 stage 디렉터리를 자동 생성했다.

## 비고

- 이 stage에서 코드 구현은 shared/ 패키지 내 3개 파일(contracts.ts, catalog.ts, eval.ts)이다.
- 나머지 stage(01~07)는 문서만 있고, 실제 구현은 08-capstone-submission의 v0~v3에 있다.
