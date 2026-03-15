# ranking proof와 release gate

앞 단계에서 catalog contract와 explanation trace를 세웠다면, 여기서부터 이 프로젝트는 추천 데모보다 제출 proof 시스템처럼 보이기 시작한다. 핵심 질문은 "candidate가 더 좋아 보이는가"가 아니라 "candidate를 release 가능한 상태라고 deterministic하게 말할 수 있는가"다. 그 답은 `compare-service.ts`, `release-gate-service.ts`, `export-artifact.ts`를 이어 읽을 때 드러난다.

## compare는 순위 비교만이 아니라 candidate uplift를 숫자로 남기는 장치다

`runCompare()`는 각 eval case에서 baseline recommendation과 reranked candidate를 모두 계산한 뒤 nDCG@3, top1 hit rate, average score를 집계한다. 여기서 눈에 띄는 부분은 uplift 계산이다.

```ts
const rankingUplift = candidateNdcg3 - baselineNdcg3;
const scoreUplift =
  baselineAverageScore === 0 ? 0 : (candidateAverageScore - baselineAverageScore) / baselineAverageScore;
...
uplift: Math.max(rankingUplift, scoreUplift)
```

즉 이 프로젝트에서 uplift는 "nDCG가 얼마나 올랐는가" 하나로만 결정되지 않는다. ranking이 같더라도 candidate score 체계가 더 강해졌다면 uplift가 남는다. 2026-03-14 재실행 결과가 정확히 그 예였다. release gate가 읽은 metrics는 `baselineNdcg3 0.9758684958518087`, `candidateNdcg3 0.9758684958518087`, `uplift 0.11464081369730995`였다. 순위 nDCG는 같지만 score uplift가 비교 threshold를 넘긴 것이다.

이건 약점이라기보다 현재 프로젝트의 철학을 드러낸다. compare는 "무조건 랭킹이 더 좋아져야 한다"보다 "candidate가 deterministic하게 더 강한 제안인가"를 본다. 그래서 이 단계의 pass/fail은 strict rerank victory보다 "non-regression on ranking + stronger score evidence"에 더 가깝다.

## release gate는 quality signal과 제출 completeness를 한 번에 묶는다

`release-gate-service.ts`는 compare metric만 보지 않는다. compatibility pass, eval acceptance, compare uplift, required docs/artifacts, release note completeness를 모두 검사한다.

```ts
if (!(candidateNdcg3 >= baselineNdcg3 && uplift >= 0.02)) {
  reasons.push("candidate compare uplift가 임계값 0.02를 넘지 못했거나 baseline보다 낮습니다.");
}

if (!requiredPathsExist(candidate.requiredDocs) || !requiredPathsExist(candidate.requiredArtifacts)) {
  reasons.push("제출용 docs 또는 artifact 파일이 누락되었습니다.");
}
```

좋은 점은 release 판단이 모델 수치만으로 끝나지 않는다는 것이다. 이 프로젝트에서 "릴리즈 가능"은 다음이 동시에 충족되어야 한다.

- 호환성 게이트를 통과했는가
- offline eval acceptance를 통과했는가
- compare uplift가 최소 threshold를 넘는가
- 제출에 필요한 docs/artifact가 실제로 존재하는가
- release note가 `변경 요약 / 검증 / 리스크` 섹션을 갖췄는가

즉 추천 시스템을 실제 운영 승인이나 제출 직전 체크리스트처럼 읽게 만드는 부분이 바로 여기다.

여기서 특히 중요하게 남겨 둘 점은 gate가 ranking delta만을 승인 근거로 쓰지 않는다는 사실이다. 2026-03-14 rerun은 `baseline nDCG@3 == candidate nDCG@3`였지만 gate는 통과했다. 다시 말해 이 프로젝트의 release proof는 "순위가 더 좋아졌는가"보다 "후보안이 baseline보다 뒤로 가지 않았고, score/explanation/compatibility/doc completeness까지 포함한 제출 증거가 충분한가"를 묻는다.

## artifact export는 proof를 사람이 읽을 수 있는 문서로 바꾸는 마지막 단계다

`export-artifact.ts`는 latest compatibility, latest gate, latest eval, latest compare를 읽어서 `buildSubmissionArtifact()` 결과를 저장하고 콘솔로도 출력한다.

```ts
const artifact = buildSubmissionArtifact(
  candidate,
  compatibilityReport,
  gateReport,
  latestEval,
  latestCompare
);
console.log(artifact.content);
```

이 단계가 중요한 이유는 proof chain의 마지막 결과가 JSON row가 아니라 Markdown artifact라는 점이다. 운영자나 심사자가 DB를 다시 조회할 필요 없이, 현재 candidate가 왜 통과했는지 한 문서로 읽을 수 있다.

이번 재실행에서도 실제로 다음 출력이 나왔다.

- `compatibility passed: true`
- `release gate passed: true`
- `Offline Eval`: `top3 recall 0.958`, `explanation completeness 1.000`, `forbidden hit rate 0.000`
- `Compare Snapshot`: `baseline nDCG@3 0.976`, `candidate nDCG@3 0.976`, `uplift 0.115`
- `Compatibility Issues`: `none`
- `Release Gate Reasons`: `none`

## 이번 단계의 검증 신호

```bash
cd /Users/woopinbell/work/book-task-3/infobank/projects/01-mcp-recommendation-demo/capstone/v2-submission-polish
pnpm compatibility rc-release-check-bot-1-5-0
pnpm release:gate rc-release-check-bot-1-5-0
pnpm artifact:export rc-release-check-bot-1-5-0
```

재실행 결과:

- compatibility: 5개 check 모두 pass
- release gate: pass, reasons 없음
- artifact export: release candidate, eval, compare, gate 결과를 묶은 Markdown 생성

이 단계의 결론은 분명하다. 이 프로젝트는 추천 품질을 수치로만 주장하지 않는다. release proof와 문서 completeness까지 묶어 deterministic submission path로 바꾼다.
