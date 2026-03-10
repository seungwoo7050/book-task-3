# 보안 정책

이 저장소는 학습용 저장소이지만, [`chat-qa-ops/08-capstone-submission/v3-self-hosted-oss/`](./chat-qa-ops/08-capstone-submission/v3-self-hosted-oss/)는 self-hosted 참고 OSS로 함께 공개한다.

## 범위

- 보안 이슈는 공개 issue에 민감정보를 남기지 말고 재현 단계만 최소로 적는다.
- API key, DB credential, session secret은 절대 저장소에 커밋하지 않는다.
- sample transcript와 KB는 데모 전용이며 실제 개인정보를 포함하지 않는다.

## 지원 버전

- self-host 지원 대상: `chat-qa-ops/08-capstone-submission/v3-self-hosted-oss`
- 보존용 데모 버전: `chat-qa-ops/08-capstone-submission/v0-initial-demo`
- 보존용 데모 버전: `chat-qa-ops/08-capstone-submission/v1-regression-hardening`
- 보존용 데모 버전: `chat-qa-ops/08-capstone-submission/v2-submission-polish`

## 제보 방법

민감한 취약점은 공개 issue보다 별도 비공개 경로로 공유하는 것이 안전하다. 재현에 필요한 최소 정보만 남기고, 실제 credential이나 production data는 포함하지 않는다.
