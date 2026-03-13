# 02 Capstone

이 트랙은 앞선 아홉 개 프로젝트의 판단 로직과 데이터 모델을 하나의 local security platform 흐름으로 묶는 단계입니다.

## 이 트랙이 답하려는 큰 질문

개별 스캐너와 규칙 엔진을 어떻게 API, worker, DB, 보고 흐름으로 통합할 것인가?

## 프로젝트 맵

| ID | 프로젝트 | 문제 | 답 | 검증 | 다음 단계 연결 |
| --- | --- | --- | --- | --- | --- |
| 10 | [Cloud Security Control Plane](10-cloud-security-control-plane/README.md)<br>[문제](10-cloud-security-control-plane/problem/README.md) | Terraform, IAM, CloudTrail, Kubernetes 입력을 한 운영 흐름으로 통합하기 | API, worker, state store, remediation, report를 가진 local control plane 구현 | `make test-capstone`, `make demo-capstone` | 앞선 01~09의 개별 답을 하나의 학습용 플랫폼으로 묶는 최종 단계 |

## 추천 읽기 순서

1. 이 프로젝트 README에서 문제, 답, 검증을 먼저 확인합니다.
2. `problem/README.md`로 캡스톤이 통합하는 입력과 출력 범위를 확인합니다.
3. `docs/demo-walkthrough.md`와 `python/README.md`로 API와 worker 흐름을 따라갑니다.
4. source-first 흐름이 필요하면 [../blog/02-capstone/README.md](../blog/02-capstone/README.md)로 이동합니다.

## 이 트랙을 끝내면 설명할 수 있어야 하는 것

- 왜 API, worker, DB, lake, report를 한 파일이 아니라 여러 레이어로 나눴는지 설명할 수 있어야 합니다.
- 앞선 프로젝트의 어떤 판단 로직이 캡스톤에서 재사용되는지 말할 수 있어야 합니다.
- local demo가 어떤 범위를 검증하고 무엇을 의도적으로 비워 두는지 설명할 수 있어야 합니다.
