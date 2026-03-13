# 01 Cloud Security Core blog

이 트랙의 블로그는 기초 입력 위에 실제 운영자가 읽을 수 있는 finding, remediation, detection, governance 흐름을 어떻게 쌓았는지 추적합니다.

## 이 트랙이 다루는 질문

- broad permission과 misconfiguration을 어떤 finding 구조로 바꿔야 triage 가능한가
- finding 이후의 조치 제안과 승인 경계를 어떻게 분리해야 하는가
- 로그 기반 detection, 컨테이너 guardrail, 예외와 증적 흐름을 왜 별도 프로젝트로 분리해야 하는가

## 프로젝트 인덱스

1. [04 IAM Policy Analyzer](04-iam-policy-analyzer/00-series-map.md)
2. [05 CSPM Rule Engine](05-cspm-rule-engine/00-series-map.md)
3. [06 Remediation Pack Runner](06-remediation-pack-runner/00-series-map.md)
4. [07 Security Lake Mini](07-security-lake-mini/00-series-map.md)
5. [08 Container Guardrails](08-container-guardrails/00-series-map.md)
6. [09 Exception and Evidence Manager](09-exception-and-evidence-manager/00-series-map.md)

## 권장 읽기 순서

1. 04와 05를 먼저 읽어 finding 생성 경로를 두 갈래로 잡습니다.
2. 06에서 finding 이후의 dry-run remediation 경계를 확인합니다.
3. 07과 08에서 로그와 컨테이너 입력이 각각 어떤 alert/finding으로 바뀌는지 읽습니다.
4. 09에서 suppression, evidence, audit trail이 왜 별도 모델이어야 하는지 봅니다.

## 공통 검증 경로

```bash
make test-unit
```
