# ranking proof와 release gate

앞 글에서 봤듯이 이 프로젝트는 추천 후보를 잘 설명할 수 있는 contract와 ranking loop를 먼저 만들었다. 이번 글에서 다룰 질문은 그다음이다. 그렇게 만든 추천 결과를, 어떻게 "릴리즈해도 되는 후보"라는 판단까지 끌고 갔을까?

이 구간은 `v2-submission-polish`의 핵심을 보여 준다. 기능이 하나 더 늘어난 것이 아니라, compare와 compatibility, release 판단, artifact export가 하나의 승인 경로로 이어진다. 다시 말해 추천 품질 개선이 운영 결정과 문서 산출물까지 닿기 시작한다.

가장 먼저 눈에 띄는 문서는 `docs/compare-report.md`다. 여기에는 compare가 어떤 기준으로 통과되는지가 아주 분명하게 적혀 있다. `candidateNdcg3 >= baselineNdcg3`, 그리고 `uplift >= 0.02`. 좋은 점은 "좀 더 나아 보인다" 같은 모호한 설명을 허용하지 않고, 비교가 반드시 수치와 임계값으로 남게 했다는 점이다.

이 compare 결과를 실제로 받아서 최종 판정으로 바꾸는 곳이 `node/src/services/release-gate-service.ts`다.

이 코드가 중요한 이유는, compare 수치만 보고 끝내지 않기 때문이다. 여기서는 점수 개선뿐 아니라 제출용 문서와 artifact가 실제로 존재하는지도 같이 본다. 즉 이 프로젝트의 마지막 판단이 "추천이 좋아졌다"가 아니라 "이 후보가 제출 가능한 상태다"로 바뀐다.

```ts
if (!(candidateNdcg3 >= baselineNdcg3 && uplift >= 0.02)) {
  reasons.push("candidate compare uplift가 임계값 0.02를 넘지 못했거나 baseline보다 낮습니다.");
}

if (!requiredPathsExist(candidate.requiredDocs) || !requiredPathsExist(candidate.requiredArtifacts)) {
  reasons.push("제출용 docs 또는 artifact 파일이 누락되었습니다.");
}
```

`docs/release-gate-proof.md`를 함께 읽으면 이 판단 기준이 더 또렷해진다. 여기서 gate는 compatibility pass, offline eval acceptance, compare uplift, required docs/artifacts, release note completeness까지 한 번에 검사한다. 중요한 이유는, 추천 시스템이 여기서부터 모델 점수만 보는 데모가 아니라 실제 제출 절차를 닮은 도구로 읽히기 시작하기 때문이다.

이제 마지막 한 칸이 남는다. `node/src/scripts/export-artifact.ts`는 최신 compatibility, release gate, eval, compare 결과를 모아 artifact markdown을 만든다. 그래서 artifact export는 단순한 부가 기능이 아니라, release gate가 통과한 결과를 사람이 바로 읽을 수 있는 문서로 바꾸는 단계다.

아래 CLI 재실행 결과를 보면 이 흐름이 한 번에 잡힌다.

```bash
pnpm compatibility rc-release-check-bot-1-5-0
pnpm release:gate rc-release-check-bot-1-5-0
pnpm artifact:export rc-release-check-bot-1-5-0
```

```text
compatibility passed: true
release gate passed: true
top3Recall: 0.9583333333333334
uplift: 0.11464081369730995

# release-check-bot v1.5.0
- compatibility passed: true
- release gate passed: true
## Release Notes
변경 요약 ...
검증 ...
리스크 ...
```

이 출력이 증명하는 것은 세 가지다. 첫째, candidate가 compare와 compatibility를 동시에 통과했다. 둘째, offline eval과 uplift 수치가 release 판단까지 그대로 이어졌다. 셋째, 최종 결과가 다시 사람 읽을 수 있는 Markdown artifact로 정리됐다. CLI가 끝난 뒤 운영자가 JSON 조각을 다시 꿰맞출 필요가 없다는 뜻이다.

좋은 점은 이 단계에서 프로젝트의 무게중심이 분명해진다는 것이다. `MCP 추천 최적화`는 더 이상 ranking demo가 아니라, 추천 개선을 어떻게 release 판단과 제출 문서로 연결할 것인지 보여 주는 시스템이 된다. `v2`를 공식 답으로 둔 이유도 바로 여기에 있다.

다음 글에서는 이 흐름을 한 걸음 더 밀어붙인다. 이미 만든 gate와 artifact pipeline이 `v3-self-hosted-oss`에서 RBAC, async jobs, audit log, polling UI를 가진 운영자 화면으로 어떻게 바뀌는지 본다.
