> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Release Compatibility & Quality Gates — 개발 타임라인

## 1단계: compatibility-service.ts

```bash
cd 08-capstone-submission/v2-submission-polish/node/src/services
touch compatibility-service.ts
```

구현 순서:
1. RC의 toolId와 candidateVersion 파싱
2. catalog에서 현재 버전 조회
3. semver diff 계산 (major/minor/patch)
4. 의존 도구 호환성 확인

```bash
pnpm test  # compatibility-service.test.ts 실행
```

## 2단계: release-gate-service.ts

```bash
touch release-gate-service.ts
```

구현 순서:
1. compatibility gate 실행 → breaking change 확인
2. eval 실행 → threshold 통과 확인
3. deprecated dependency 확인
4. 전체 PASS/FAIL 판정

## 3단계: artifact-service.ts

```bash
touch artifact-service.ts
```

gate 결과를 JSON으로 직렬화하여 파일로 저장:

```bash
mkdir -p artifacts
pnpm artifact:export rc-release-check-bot-1-5-0
# → artifacts/rc-release-check-bot-1-5-0.json
```

## 4단계: CLI 스크립트 추가

```json
{
  "scripts": {
    "compatibility": "tsx src/scripts/run-compatibility.ts",
    "release:gate": "tsx src/scripts/run-release-gate.ts",
    "artifact:export": "tsx src/scripts/run-artifact-export.ts"
  }
}
```

각 스크립트는 RC ID를 CLI 인자로 받는다.

## 5단계: 테스트

```bash
pnpm test
```

compatibility-service.test.ts:
- minor 버전 변경 → compatible
- major 버전 변경 → breaking change 경고

release-gate-service.test.ts:
- 모든 검사 통과 → PASS
- breaking change 있음 → FAIL
- deprecated dependency → WARN

## 6단계: 통합 실행

```bash
pnpm compatibility rc-release-check-bot-1-5-0
pnpm release:gate rc-release-check-bot-1-5-0
pnpm artifact:export rc-release-check-bot-1-5-0
```

이 순서로 실행하면 RC의 전체 gate 과정이 완료된다.

## 비고

- 이 stage는 v2 capstone에서 구현된다. v0/v1에는 gate 기능이 없다.
- artifact 파일은 artifacts/ 디렉터리에 저장되며, .gitignore에 포함시키지 않는다 (증거 문서).
- v3에서는 gate 실행이 background job으로 처리되고 audit log에 기록된다.
