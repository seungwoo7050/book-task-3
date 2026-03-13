# G-ops-lab

이 글은 기능 구현보다 운영 질문을 먼저 드러내는 마지막 단일 서비스 랩이다. G 랩은 health, ready, metrics, CI target shape를 나중의 부록이 아니라 제품이 반드시 남겨야 할 표면으로 다룬다.

## 이 글이 붙잡는 질문
health, readiness, metrics, automation을 제품 기능 뒤로 미루지 않고도 작은 서비스에 맞는 운영 surface로 설명할 수 있는가가 이 글의 질문이다.

## 왜 이 프로젝트를 따로 읽어야 하나
README와 docs가 운영 관찰 가능성을 별도 주제로 삼고, 테스트와 probe는 live/ready/metrics를 직접 검증한다. 덕분에 이 프로젝트는 "마지막 점검"이 아니라 운영 입구를 읽는 독립 랩이 된다.

## 이번 글에서 따라갈 흐름
1. 운영성을 기능의 뒷정리가 아니라 설계 질문으로 올린다.
2. health와 metrics가 어떤 질문에 답하는지 route와 exporter에서 본다.
3. probe와 smoke를 테스트 회귀선으로 묶는다.
4. 재검증 기록으로 단일 서비스 학습 트랙을 닫는다.

## 마지막에 확인할 근거
- 코드: `labs/G-ops-lab/fastapi/app/api/v1/routes/ops.py::metrics`
- 테스트/런타임: `labs/G-ops-lab/fastapi/tests/integration/test_ops.py::test_live_ready_and_metrics`
- CLI: `python3 -m compileall app tests`, `make lint`, `make test`, `make smoke`, `./tools/compose_probe.sh labs/G-ops-lab/fastapi 8005`

## 이 글을 다 읽고 나면
- live와 ready가 서로 다른 실패를 어떻게 드러내는지 보게 된다.
- 최소 metrics만으로도 어떤 운영 질문을 읽을 수 있는지 감이 잡힌다.
- CI surface와 로컬 probe가 왜 같은 문서에 있어야 하는지 이해하게 된다.
- 검증 기록: 2026-03-09에 compile, lint, test, smoke, Compose live/ready probe가 모두 통과했다.
- 다음으로 이어 볼 대상: workspace-backend
