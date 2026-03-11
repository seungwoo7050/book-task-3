# 05 judge 결과와 점수 병합

## 이 stage의 문제

응답 품질 판단과 최종 score 계산을 어떻게 나누어야 회귀 비교와 모델 교체가 쉬운지 정리한다.

## 입력/제약

- 입력: heuristic judge output, weighted score contract
- 제약: judge가 바뀌어도 merge contract는 유지돼야 한다.

## 이 stage의 답

- judge output과 weighted score merge를 분리한다.
- provider 교체와 score contract 고정을 서로 다른 책임으로 나눈다.

## capstone 연결 증거

- `projects/02-chat-qa-ops/stages/05-judge-and-score-merge/python/src/stage05/judge.py`
- `projects/02-chat-qa-ops/capstone/v1-regression-hardening/python/backend/src/evaluator/llm_judge.py`

## 검증 명령

```bash
cd python
UV_PYTHON=python3.12 uv run pytest -q
```

## 현재 한계

- 실제 LLM adapter는 stage에 포함하지 않는다.
- prompt tuning과 judge model 평가 자체는 후속 capstone 증빙에 의존한다.
