# 03-rule-and-guardrail-engine 재현 타임라인

## 이 문서의 역할

이 문서는 과거의 시간순 일지를 복원하는 대신, 지금 저장소 기준으로 같은 결과를 다시 확인하는 순서를 남긴다. 학습자는 이 순서를 따라가며 어떤 파일을 먼저 읽고, 어떤 명령을 실행하고, 어떤 결과를 근거로 삼아야 하는지 바로 파악할 수 있어야 한다.

## 재현 전에 준비할 것

- 상담 품질 평가가 단순 친절도보다 안전성과 정책 준수를 우선해야 함을 이해해야 한다.

## 재현 순서

1. stage `README.md`, `problem/README.md`, `docs/README.md`를 먼저 읽어 문제 해석과 완료 기준을 고정한다.
2. 아래 핵심 경로를 위에서 아래 순서로 열어 구현과 문서가 같은 뜻을 가리키는지 확인한다.

- `python/data/rules.json`
- `python/src/stage03/guardrails.py`
- `python/tests/test_guardrails.py`

3. 아래 검증 명령을 그대로 실행해 현재 저장소 상태가 문서 설명과 맞는지 확인한다.

```bash
cd python
UV_PYTHON=python3.12 uv sync
UV_PYTHON=python3.12 uv run pytest -q
```

4. 테스트나 실행 결과를 아래 증거와 대조한다.

- `python/tests/test_guardrails.py`가 네 가지 규칙을 각각 분리 검증한다.
- 룰은 JSON 파일로 분리되어 정책 변경이 코드 diff 없이도 보인다.

5. 결과가 다르면 `02-debug-log.md`와 `notion-archive/`를 함께 열어 어떤 가정이 바뀌었는지 추적한다.

## 재현 체크포인트

- mandatory notice, unsupported claim, PII exposure, escalation miss가 각각 독립 코드로 검출된다.
- LLM 없이도 재현 가능한 deterministic regression이 가능하다.
- 후속 score merge에서 compliance 축을 해석할 수 있다.

## 막히면 먼저 볼 것

- 민원 또는 분쟁 표현이 들어와도 상담원 이관 부재가 따로 보이지 않을 수 있었다. -> 확인 기준: `test_escalation_rule`이 `ESCALATION_MISS`를 직접 기대한다.

## 자기 포트폴리오 레포로 옮길 때

- 이 문서의 순서를 그대로 유지하되, 경로만 내 저장소 구조에 맞게 바꾼다.
- `README.md`에는 문제 해석, 현재 상태, 실행 명령만 남기고 더 긴 판단 과정은 `notion/`으로 보낸다.
- `docs/README.md`에는 검증 기준, proof artifact, 오래 남길 개념만 남긴다.
- 새 노트를 다시 쓰고 싶다면 기존 `notion/`을 `notion-archive/`로 옮겨 예전 판단을 보존한다.
- 발표나 제출용 README를 만들 때는 이 문서의 체크포인트를 그대로 acceptance checklist로 재사용한다.
