# 보안 정책

이 저장소는 학습용 아카이브지만, self-hosted 참고 버전도 함께 공개한다. 현재 보안 이슈 대응 범위는 [`projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/`](./projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/README.md)와 [`projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/`](./projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/README.md)를 중심으로 본다.

## 범위

- 공개 issue에는 민감정보 대신 최소 재현 단계만 남긴다.
- API key, DB credential, session secret, real customer data는 커밋하지 않는다.
- sample transcript, KB, catalog seed는 데모 전용 자료만 사용한다.

## 지원 버전

- self-host 지원 대상: `projects/02-chat-qa-ops/capstone/v3-self-hosted-oss`
- self-host 지원 대상: `projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening`
- 공식 제출 답 보존 버전: `projects/02-chat-qa-ops/capstone/v2-submission-polish`
- 공식 제출 답 보존 버전: `projects/01-mcp-recommendation-demo/capstone/v2-submission-polish`

## 제보 방법

민감한 취약점은 공개 issue보다 비공개 경로로 공유하는 편이 안전하다. 실제 credential, production data, 개인식별정보는 포함하지 말고 재현에 필요한 최소 정보만 남긴다.
