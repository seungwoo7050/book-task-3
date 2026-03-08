# Legacy Audit

`legacy/`는 React Native 학습 트리의 기준선이지만, 그대로는 안정적인 학습 저장소로 쓰기 어렵다.

## Verified Findings

- 2026-03-07 기준 `legacy`에는 `study/` 대응 구조가 없다.
- `legacy/workspace`와 `legacy/workspace.prev.20260227031148`는 비어 있다.
- `make -C legacy verify`는 모든 과제가 스캐폴드 검사만 통과한다.
- `bash legacy/scripts/docs_quality_check.sh`는 상대 링크 69건 실패로 종료 코드 1을 반환한다.
- 실제 TypeScript 구현은 `legacy/04-capstone/mobile-product-capstone/solve/solution/server`와 `legacy/04-capstone/mobile-product-capstone/solve/solution/shared/contracts.ts`에만 있다.

## Weaknesses In Legacy

- 대부분 과제는 `solve/solution`과 `solve/test`가 사실상 빈 디렉터리다.
- 공용 `workspace/` 모델에 의존하지만 실제 워크스페이스가 비어 있어 문서와 실행 상태가 어긋난다.
- `devlog`와 `solve/analysis.md`는 추정 중심 기록이 많아 공개 인덱스로 쓰기 어렵다.
- 루트 문서 일부는 실제 존재하지 않는 경로와 아티팩트에 링크한다.

## Migration Decisions

- `legacy/`는 읽기 전용으로 유지한다.
- `study/`는 프로젝트별 독립 `react-native/` 구현 디렉터리를 사용한다.
- 캡스톤만 `react-native/`와 `node-server/`를 함께 둔다.
- `offline-sync-foundations`를 새 프로젝트로 추가한다.
- 재현 불가능한 증빙은 `study/`의 공식 근거로 승격하지 않는다.

## Evidence

검사에 사용한 명령:

```bash
make -C legacy verify
bash legacy/scripts/docs_quality_check.sh
find legacy -path '*/solve/solution/*' -type f | sort
du -sh legacy/workspace legacy/workspace.prev.20260227031148
```
