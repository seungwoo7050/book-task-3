# Debug Log

## Failure

- failing command or request:
  - test validation path
- exact symptom:
  - real Redis cache 없이도 테스트는 통과하지만, 그 상태를 설명하지 않으면 cache lab이 과장된다
- first incorrect assumption:
  - `@Cacheable` 같은 annotation이 보이면 Redis behavior까지 충분히 증명된다고 생각하기 쉽다
- evidence collected:
  - verification report는 이 랩이 local in-memory `CacheManager`를 강제한 뒤 통과했다고 적는다

## Root cause

테스트 안정성과 학습 범위를 위해 in-memory cache를 썼지만, 이름은 Redis/cache lab이라 implementation depth와 label 사이 간극이 생긴다.

## Fix and verification

- code or config change made:
  - 검증 문서에 in-memory cache usage를 명시했다
- why that change addresses the cause:
  - 현재 무엇이 증명되었고 무엇이 아직 아닌지 구분된다
- command, test, or log line that proved the fix:
  - `make test`
  - `study2/docs/verification-report.md`

## Follow-up debt

- selected flow를 real Redis assertion으로 옮길 수 있다
- Redisson distributed lock을 실제로 추가해야 한다

