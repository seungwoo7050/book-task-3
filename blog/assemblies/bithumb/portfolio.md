# Bithumb Portfolio

> PDF/Notion 제출용 조립본입니다. 기준일: 2026년 3월 13일

| 항목 | 내용 |
| --- | --- |
| 포지션 | Backend / Platform / Security Engineering for Bithumb-style Assignment |
| 한 줄 포지셔닝 | scan, finding, exception, remediation, report를 하나의 local control plane으로 통합하는 개발자 |
| 핵심 스택 | Python, FastAPI, PostgreSQL, SQLite fallback, worker, report pipeline |
| 대표 프로젝트 | `Cloud Security Control Plane`, `backend-common`, `Cloud Security Core` |
| 링크 | [bithumb](../../../bithumb/README.md) · [backend-fastapi](../../../backend-fastapi/README.md) |

## 공통 코어 요약

- 42서울 정규과정과 공통 코어 프로젝트로 시스템 기반을 다졌습니다.
- `ft_transcendence`의 Django 백엔드, 42 OAuth, JWT, TOTP 기반 2FA 경험은 인증/인가 공통 근거로 사용합니다.

## backend-common 요약

FastAPI 기반 `workspace-backend` 계열을 통해 인증/인가, API 경계, async flow, verification report 구조를 공통 백엔드 기반으로 다졌습니다.

## 대표 프로젝트 1. Cloud Security Control Plane

Terraform plan, IAM policy, CloudTrail fixture, Kubernetes manifest를 공통 finding 흐름으로 통합한 capstone입니다. FastAPI API, scan worker, remediation worker, 상태 저장소, markdown report를 한 서비스 레이어에서 연결했고, Docker가 없어도 SQLite fallback으로 demo를 재현할 수 있게 했습니다.

![cloud security control plane evidence](../../assets/captures/bithumb/cloud-security-control-plane-evidence.png)

## 대표 프로젝트 2. Cloud Security Core

IAM Policy Analyzer, CSPM Rule Engine, Exception and Evidence Manager를 개별 프로젝트로 학습한 뒤 capstone에서 하나의 운영 흐름으로 재통합했습니다.

## 마무리

이 제출본은 개별 보안 판단 로직을 하나의 운영 흐름으로 묶어 설명하는 경험을 보여 줍니다. scan, finding, exception, remediation, report, audit trail을 함께 보는 플랫폼/백엔드 감각이 핵심입니다.
