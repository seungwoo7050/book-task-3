# Release Compatibility & Quality Gates — 접근 기록

## compatibility-service.ts 구현

semver 분석 + 호환성 판정 로직:

1. 현재 catalog에서 도구의 현재 버전을 조회
2. release candidate의 버전과 비교
3. semver diff 분석: major/minor/patch
4. 의존 도구들의 버전과 호환성 확인

출력 형태:

```typescript
{
  rcId: "rc-release-check-bot-1-5-0",
  toolId: "release-check-bot",
  currentVersion: "1.4.0",
  candidateVersion: "1.5.0",
  semverDiff: "minor",
  breakingChanges: [],
  compatibilityStatus: "compatible",
  dependencyChecks: [...]
}
```

## release-gate-service.ts 구현

release gate는 여러 검사를 순차적으로 실행한다:

1. compatibility gate 결과 확인 → breaking change가 있으면 FAIL
2. eval 실행 → threshold 통과 여부 확인
3. deprecated dependency 확인 → 있으면 WARN
4. 모든 항목 통과 → PASS

각 검사 결과를 `checks[]` 배열에 기록하고,
하나라도 FAIL이면 전체 결과가 FAIL이 된다.

## artifact-service.ts 구현

gate 실행 결과를 JSON 파일로 내보내는 서비스:

```bash
pnpm artifact:export rc-release-check-bot-1-5-0
# → artifacts/rc-release-check-bot-1-5-0.json
```

artifact에 포함되는 정보:
- RC 메타데이터 (toolId, version, timestamp)
- compatibility report
- release gate report (checks + overall status)
- eval summary

이 artifact가 배포 승인의 증거 문서가 된다.

## CLI 명령어 설계

v2에서 세 가지 CLI 명령어를 추가했다:

```bash
pnpm compatibility <rc-id>     # compatibility gate 실행
pnpm release:gate <rc-id>      # release gate 실행
pnpm artifact:export <rc-id>   # artifact 내보내기
```

각 명령어는 독립적으로 실행 가능하지만,
보통 compatibility → release:gate → artifact:export 순서로 실행한다.
