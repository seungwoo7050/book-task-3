# 02 Capstone 읽기 안내

이 캡스톤은 앞선 아홉 프로젝트를 한 서비스의 상태 흐름으로 묶는 단계다. 새로운 scanner를 많이 추가하는 글이 아니라, 이미 만든 판단을 같은 API, 같은 저장소, 같은 report 흐름 위에 올리는 글이라고 생각하면 읽기가 훨씬 쉽다.

그래서 이 트랙은 phase가 네 개로 나뉜다. API 표면을 먼저 세우고, worker를 붙이고, remediation/report를 닫고, 마지막에 demo capture로 end-to-end 재현성을 남기는 순서가 capstone 전체의 핵심이다.

| 프로젝트 | 시리즈 지도 | evidence | outline | 최종 글 | 대표 검증 |
| --- | --- | --- | --- | --- | --- |
| 10 Cloud Security Control Plane | [00-series-map](10-cloud-security-control-plane/00-series-map.md) | [05-evidence-ledger](10-cloud-security-control-plane/05-evidence-ledger.md) | [_structure-outline](10-cloud-security-control-plane/_structure-outline.md) | [10-development-timeline](10-cloud-security-control-plane/10-development-timeline.md) | `make test-capstone`, `make demo-capstone` |

## 읽을 때 먼저 볼 포인트

- Phase 1에서는 왜 scanner 로직보다 API와 session factory를 먼저 세웠는지 본다.
- Phase 2와 3에서는 pending/completed 상태, remediation, report가 어떻게 한 흐름으로 묶이는지 본다.
- 마지막 phase에서는 demo capture가 왜 capstone의 신뢰도를 끌어올리는지 본다.

legacy 격리 원칙은 [`../_legacy/2026-03-13-isolate-and-rewrite/02-capstone`](../_legacy/2026-03-13-isolate-and-rewrite/02-capstone)에서 확인할 수 있다.
