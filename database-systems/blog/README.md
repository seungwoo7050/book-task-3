# Database Systems Blog Index

`database-systems/README.md`가 전체 지도를 보여 준다면, 이 디렉터리는 실제 구현 순서와 판단 전환을 따라가며 다시 읽는 입구다. 저장 엔진 내부와 분산 시스템 경계를 코드, 테스트, CLI 기준으로만 붙잡았다.

## 어디서부터 읽으면 좋은가

- 저장 엔진 내부 흐름부터 보고 싶다면 `Database Internals` 트랙으로 들어간다.
- 분산 시스템 경로를 따라가고 싶다면 `DDIA Distributed Systems` 트랙으로 들어간다.
- 작은 구현으로 빠르게 훑고 싶다면 Python 쪽이, 더 잘게 쪼갠 단계형 구성을 원하면 Go 쪽이 잘 맞는다.

## 언어별 인덱스

- [Python Blog Index](python/README.md) — 9개 프로젝트를 작은 구현 중심으로 묶은 입구
- [Go Blog Index](go/README.md) — 16개 프로젝트를 더 잘게 나눈 단계형 입구

## 읽는 순서

1. 먼저 상위 `database-systems/README.md`에서 전체 트랙 맥락을 확인한다.
2. 언어와 트랙을 고른 뒤 각 프로젝트의 `00-series-map.md`로 들어간다.
3. 본문은 `10 -> 20 -> 30` 순서로 읽는다.
4. 더 세밀한 작업 메모가 필요할 때만 `_evidence-ledger.md`, `_structure-outline.md`를 참고한다.
