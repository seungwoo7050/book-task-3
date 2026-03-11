# capstone 재현 타임라인

## 이 문서의 역할

이 문서는 과거의 시간순 일지를 복원하는 대신, 지금 저장소 기준으로 같은 결과를 다시 확인하는 순서를 남긴다. 학습자는 이 순서를 따라가며 어떤 파일을 먼저 읽고, 어떤 명령을 실행하고, 어떤 결과를 근거로 삼아야 하는지 바로 파악할 수 있어야 한다.

## 재현 전에 준비할 것

- Python 3.12 환경과 `uv`, `pnpm`, Docker가 있으면 검증을 재현하기 쉽다.
- live Upstage/OpenAI/Langfuse 자격증명이 없어도 mock/no-op 경로로 테스트는 가능하다.

## 재현 순서

1. stage `README.md`, `problem/README.md`, `docs/README.md`를 먼저 읽어 문제 해석과 완료 기준을 고정한다.
2. 아래 핵심 경로를 위에서 아래 순서로 열어 구현과 문서가 같은 뜻을 가리키는지 확인한다.

- `projects/02-chat-qa-ops/capstone/README.md`
- `projects/02-chat-qa-ops/capstone/docs/release-readiness.md`
- `projects/02-chat-qa-ops/capstone/v0-initial-demo`
- `projects/02-chat-qa-ops/capstone/v1-regression-hardening`
- `projects/02-chat-qa-ops/capstone/v2-submission-polish`

3. 아래 검증 명령을 그대로 실행해 현재 저장소 상태가 문서 설명과 맞는지 확인한다.

```bash
cd v0-initial-demo/python && UV_PYTHON=python3.12 make gate-all
cd v1-regression-hardening/python && UV_PYTHON=python3.12 make gate-all
cd v1-regression-hardening/python && UV_PYTHON=python3.12 make smoke-postgres
cd v2-submission-polish/python && UV_PYTHON=python3.12 make gate-all
cd v2-submission-polish/python && UV_PYTHON=python3.12 make smoke-postgres
```

4. 테스트나 실행 결과를 아래 증거와 대조한다.

- `projects/02-chat-qa-ops/capstone/docs/release-readiness.md`에 실제 실행 명령과 결과가 정리되어 있다.
- `v2-submission-polish/docs/demo/proof-artifacts` 아래에 compare/output artifacts가 저장되어 있다.

5. 결과가 다르면 `02-debug-log.md`와 `notion-archive/`를 함께 열어 어떤 가정이 바뀌었는지 추적한다.

## 재현 체크포인트

- v0, v1, v2가 각자 독립적으로 runnable하고 역할이 다르다.
- compare는 같은 dataset과 run label 위에서 baseline 대비 개선을 증빙한다.
- fallback, dependency health, dashboard, proof artifact가 공개 저장소 기준으로 재현 가능하다.

## 막히면 먼저 볼 것

- `make gate-all`이 기본 Python 3.14 환경에서 `chromadb` import 문제로 깨졌다. -> 확인 기준: v0, v1, v2 모두 `UV_PYTHON=python3.12 make gate-all`을 통과했다.
- baseline 실패 원인 중 `MISSING_REQUIRED_EVIDENCE_DOC` 비중이 높았다. -> 확인 기준: v2 compare 결과에서 fail count가 14에서 11로 줄고 critical count가 2에서 0으로 감소했다.

## 자기 포트폴리오 레포로 옮길 때

- 이 문서의 순서를 그대로 유지하되, 경로만 내 저장소 구조에 맞게 바꾼다.
- `README.md`에는 문제 해석, 현재 상태, 실행 명령만 남기고 더 긴 판단 과정은 `notion/`으로 보낸다.
- `docs/README.md`에는 검증 기준, proof artifact, 오래 남길 개념만 남긴다.
- 새 노트를 다시 쓰고 싶다면 기존 `notion/`을 `notion-archive/`로 옮겨 예전 판단을 보존한다.
- 발표나 제출용 README를 만들 때는 이 문서의 체크포인트를 그대로 acceptance checklist로 재사용한다.
