> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Release Compatibility & Quality Gates — 문제 정의

## 풀어야 하는 문제

MCP 도구가 업데이트되면 두 가지 위험이 있다:

1. **호환성 문제**: 새 버전이 기존 도구/시스템과 호환되지 않을 수 있다
2. **품질 하락**: 업데이트 후 추천 품질이 떨어질 수 있다

이걸 사람이 매번 확인하는 건 실수 가능성이 높다.
**자동화된 gate**가 필요하다.

## 두 가지 gate

### Compatibility Gate
도구의 semver 버전을 분석하여 호환성을 판정한다.

규칙:
- major 버전 변경: **breaking change** → 경고
- minor 버전 변경: **new feature** → 정보
- patch 버전 변경: **bug fix** → 안전

추가로 의존하는 다른 도구와의 호환성도 확인한다.

### Release Gate
배포를 승인하기 전에 품질 기준을 자동으로 검증한다.

확인 항목:
- eval 통과율이 threshold 이상인지
- compatibility gate에서 breaking change가 없는지
- deprecated 도구를 의존하지 않는지

모든 항목이 통과하면 `PASS`, 하나라도 실패하면 `FAIL` + 사유를 반환한다.

## release candidate 모델

release candidate(RC)는 "아직 배포되지 않았지만 배포 준비가 된" 도구 버전이다.
RC에 대해 compatibility gate와 release gate를 실행하고,
모두 통과하면 실제 배포로 승격한다.

## artifact export

gate 실행 결과를 JSON 파일로 내보내는 기능이다.
이 파일이 "이 버전을 배포해도 되는가?"의 증거 문서가 된다.
