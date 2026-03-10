# 학습 로드맵

이 트랙의 순서는 `기초 개념 이해 -> 작은 보안 도구 구현 -> 통합 control plane`으로 고정합니다.
앞의 프로젝트는 뒤 프로젝트의 입력 형식이나 판단 기준을 준비하는 역할을 하므로, 순서를 바꾸기보다 연결을
의식하면서 따라가는 편이 좋습니다.

## 00 AWS Security Foundations

### 01 AWS Security Primitives

질문: IAM 정책은 왜 허용되거나 거부되는가?
다음 단계 연결: `04-iam-policy-analyzer`에서 broad permission과 escalation finding을 만들기 위한 기반입니다.

### 02 Terraform AWS Lab

질문: Terraform을 배포 도구가 아니라 보안 분석 입력으로 읽으려면 무엇을 봐야 하는가?
다음 단계 연결: `05-cspm-rule-engine`이 바로 이 프로젝트의 plan JSON 감각을 사용합니다.

### 03 CloudTrail Log Basics

질문: 원본 로그를 어떻게 queryable한 이벤트 구조로 바꾸는가?
다음 단계 연결: `07-security-lake-mini`와 캡스톤의 로그 적재 흐름으로 이어집니다.

## 01 Cloud Security Core

### 04 IAM Policy Analyzer

질문: 정책이 단순히 “맞다/틀리다”를 넘어 얼마나 위험한지 어떻게 설명하는가?

### 05 CSPM Rule Engine

질문: 어떤 misconfiguration을 triage 가능한 finding으로 바꿀 것인가?

### 06 Remediation Pack Runner

질문: finding 이후의 조치 제안을 어떻게 자동화 가능한 단위로 표현할 것인가?

### 07 Security Lake Mini

질문: 적재된 로그에서 어떤 detection query를 어떻게 반복 실행할 것인가?

### 08 Container Guardrails

질문: 클러스터를 직접 띄우지 않아도 manifest와 이미지 메타데이터에서 무엇을 검토할 수 있는가?

### 09 Exception and Evidence Manager

질문: finding, 예외, 증적, 감사 이력을 어떤 흐름으로 연결할 것인가?

## 02 Capstone

### 10 Cloud Security Control Plane

질문: 앞선 프로젝트의 판단 로직을 하나의 API, worker, 상태 저장소, 보고 체계로 어떻게 통합할 것인가?

## 추천 읽기 방식

- 처음 시작한다면 `01 -> 02 -> 03`까지 먼저 따라간 뒤 코어 트랙으로 넘어갑니다.
- 이미 AWS 기초가 있다면 `04 -> 05 -> 06`을 먼저 보고, 필요할 때 foundations로 돌아와도 됩니다.
- 포트폴리오 관점에서는 `10`만 따로 보지 말고, 그 전에 어떤 작은 문제들을 해결했는지 함께 설명하는 편이 더 설득력 있습니다.
