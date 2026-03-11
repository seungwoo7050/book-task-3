# 학습 로드맵

이 레포의 순서는 `입력과 판단 규칙 만들기 -> finding과 운영 흐름 만들기 -> control plane으로 통합하기`로 고정합니다.
앞의 프로젝트는 뒤 프로젝트의 입력 형식이나 판단 기준을 준비하므로, 순서를 바꾸기보다 연결을 의식하며 읽는 편이 좋습니다.

## 00 AWS Security Foundations

| ID | 질문 | 내가 만드는 답 | 다음 프로젝트에 넘기는 것 |
| --- | --- | --- | --- |
| 01 | IAM 정책은 왜 allow 또는 deny 되는가 | statement match와 `explicit deny` 우선순위를 가진 평가 엔진 | 04번 least privilege finding 설계의 판단 기반 |
| 02 | Terraform을 배포 도구가 아니라 보안 분석 입력으로 읽으려면 무엇을 봐야 하는가 | insecure/secure 실습 쌍과 plan JSON 생성 흐름 | 05번 CSPM 규칙 엔진의 직접 입력 |
| 03 | 원본 로그를 어떻게 queryable한 이벤트 구조로 바꾸는가 | 공통 이벤트 모델과 DuckDB/Parquet 적재 흐름 | 07번 security lake와 10번 캡스톤의 적재 기반 |

트랙 인덱스: [00-aws-security-foundations/README.md](../00-aws-security-foundations/README.md)

## 01 Cloud Security Core

| ID | 질문 | 내가 만드는 답 | 다음 프로젝트에 넘기는 것 |
| --- | --- | --- | --- |
| 04 | 정책이 단순히 맞다/틀리다를 넘어 얼마나 위험한지 어떻게 설명하는가 | IAM risk finding analyzer | 06번 remediation과 10번 캡스톤의 IAM finding |
| 05 | 어떤 misconfiguration을 triage 가능한 finding으로 바꿀 것인가 | Terraform plan + snapshot 규칙 엔진 | 06번 remediation과 10번 캡스톤의 인프라 finding |
| 06 | finding 이후의 조치 제안을 어떻게 운영 가능한 단위로 표현할 것인가 | dry-run remediation runner | 10번 캡스톤의 remediation worker 모델 |
| 07 | 적재된 로그에서 어떤 detection query를 어떻게 반복 실행할 것인가 | local security lake와 preset alert query | 10번 캡스톤의 CloudTrail ingestion 흐름 |
| 08 | 클러스터 없이도 manifest와 image metadata에서 무엇을 검토할 수 있는가 | k8s manifest와 image metadata scanner | 10번 캡스톤의 k8s 입력 처리 |
| 09 | finding, exception, evidence, audit 이력을 어떤 흐름으로 연결할 것인가 | 작은 거버넌스 모델과 append-only audit trail | 10번 캡스톤의 예외와 감사 모델 |

트랙 인덱스: [01-cloud-security-core/README.md](../01-cloud-security-core/README.md)

## 02 Capstone

| ID | 질문 | 내가 만드는 답 | 최종 결과 |
| --- | --- | --- | --- |
| 10 | 앞선 프로젝트의 판단 로직을 하나의 API, worker, 상태 저장소, 보고 체계로 어떻게 통합할 것인가 | local cloud security control plane | scan, finding, exception, remediation, report를 한 흐름으로 보여 주는 데모 |

트랙 인덱스: [02-capstone/README.md](../02-capstone/README.md)

## 추천 읽기 방식

- 처음 시작한다면 `01 -> 02 -> 03`까지 먼저 따라간 뒤 코어 트랙으로 넘어갑니다.
- 이미 AWS 기초가 있다면 `04 -> 05 -> 06`을 먼저 보고, 필요할 때 foundations로 돌아와도 됩니다.
- 공개 포트폴리오 관점에서는 `10`만 크게 보여 주기보다, 앞선 01~09가 어떤 입력과 판단을 준비했는지 함께 설명하는 편이 더 설득력 있습니다.
