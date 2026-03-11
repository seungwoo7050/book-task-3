# MCP 추천 Capstone

이 capstone은 stage에서 분리해 익힌 계약과 실험을 실제 제출 가능한 추천 시스템으로 다시 묶는 자리다. 공식 제출 답은 `v2-submission-polish`, 제품화 확장 답은 `v3-oss-hardening`으로 고정한다.

## 버전 표

| 버전 | 역할 | 상태 |
| --- | --- | --- |
| `v0-initial-demo` | baseline selector, manifest validation, offline eval이 처음 연결된 기준선 | `baseline` |
| `v1-ranking-hardening` | reranker, usage logs, feedback loop, compare가 추가된 hardening 버전 | `hardening` |
| `v2-submission-polish` | compatibility gate, release gate, artifact export를 갖춘 공식 제출 답 | `official answer` |
| `v3-oss-hardening` | auth, jobs, audit log, Compose packaging을 더한 self-hosted 확장 답 | `extension` |

## 읽는 순서

1. [`problem/README.md`](./problem/README.md)
2. [`docs/README.md`](./docs/README.md)
3. [`v2-submission-polish/README.md`](./v2-submission-polish/README.md)
4. [`v3-oss-hardening/README.md`](./v3-oss-hardening/README.md)
5. 필요하면 `v1`, `v0`로 내려가 개선 이전 기준선을 확인한다.

## 검증 기준

- 공식 제출 답은 `v2-submission-polish` 기준으로 판단한다.
- `v3`는 공식 답을 대체하지 않고, self-hosted productization 방향을 추가로 보여 준다.
- 자세한 명령은 [`../docs/verification-matrix.md`](../docs/verification-matrix.md)와 각 버전 README를 따른다.

## 현재 한계

- 이 capstone은 제출/포트폴리오 설명에 최적화되어 있고 production 운영 보증을 목표로 하지 않는다.
- `v3`도 학습용 OSS 후보 버전이라 multi-tenant SaaS 범위를 포함하지 않는다.
