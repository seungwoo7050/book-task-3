# 07 운영 대시보드와 리뷰 콘솔

## 이 stage의 문제

평가 결과와 trace를 운영 콘솔에서 어떻게 읽히는 형태로 보여줄지 정리한다.

## 입력/제약

- 입력: overview, failures, session review, eval runner, version compare 화면 요구
- 제약: 실제 DB persistence 없이도 UI contract와 API surface를 검증 가능해야 한다.

## 이 stage의 답

- FastAPI snapshot endpoint와 React dashboard page를 묶어 콘솔 계약을 분리한다.
- 운영자가 실패와 근거 추적을 같은 화면 흐름에서 읽게 만드는 구조를 제시한다.

## capstone 연결 증거

- `projects/02-chat-qa-ops/stages/07-monitoring-dashboard-and-review-console/python/src/stage07/app.py`
- `projects/02-chat-qa-ops/stages/07-monitoring-dashboard-and-review-console/react/src/pages/Overview.tsx`
- `projects/02-chat-qa-ops/capstone/v1-regression-hardening/react/src/pages/Overview.tsx`

## 검증 명령

```bash
cd python
UV_PYTHON=python3.12 uv run pytest -q
cd ../react
pnpm test --run
```

## 현재 한계

- 실제 persistence와 job orchestration은 `v3`에서 다룬다.
- 운영 UI가 실서비스 observability 전부를 대체하지는 않는다.
