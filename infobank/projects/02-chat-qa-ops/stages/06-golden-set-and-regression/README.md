# 06 골든셋과 회귀 검증

## 이 stage의 문제

개선 실험이 실제 품질 향상인지 어떤 데이터셋과 manifest로 증빙할지 정리한다.

## 입력/제약

- 입력: golden case, replay summary, compare manifest
- 제약: 개선 주장은 재실행 가능한 assertion과 함께 남아야 한다.

## 이 stage의 답

- golden assertion, replay summary, version compare input manifest를 분리한다.
- compare proof를 수치와 fixture 양쪽에서 다시 확인할 수 있게 만든다.

## capstone 연결 증거

- `projects/02-chat-qa-ops/stages/06-golden-set-and-regression/python/src/stage06/regression.py`
- `projects/02-chat-qa-ops/capstone/v2-submission-polish/docs/demo/proof-artifacts/improvement-report.json`

## 검증 명령

```bash
cd python
UV_PYTHON=python3.12 uv run pytest -q
```

## 현재 한계

- DB-backed dashboard와 artifact browsing은 아직 없다.
- golden set 관리의 조직 운영 문제는 범위 밖이다.
