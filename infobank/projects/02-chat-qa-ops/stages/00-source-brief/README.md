# 00 문제 정의와 방향 고정

## 이 stage의 문제

이 트랙이 무엇을 만들고 어떤 sequence와 stack을 따르는지 코드를 통해 먼저 고정한다.

## 입력/제약

- 입력: reference spine, project selection rationale, baseline version, primary stack
- 제약: capstone runtime을 직접 만들지 않고 기준 문서와 코드 계약만 남긴다.

## 이 stage의 답

- `SourceBrief` 객체로 topic, baseline, stack, reference spine을 고정한다.
- 이후 stage와 capstone README가 따라야 할 공통 vocabulary를 만든다.

## capstone 연결 증거

- `projects/02-chat-qa-ops/stages/00-source-brief/python/src/stage00/source_brief.py`
- `projects/02-chat-qa-ops/capstone/v0-initial-demo/README.md`

## 검증 명령

```bash
cd python
UV_PYTHON=python3.12 uv run pytest -q
```

## 현재 한계

- 실제 평가 파이프라인은 아직 포함하지 않는다.
- 이 stage는 navigation contract와 baseline contract에 집중한다.
