# Approach Log

## Options considered

- ops를 capstone 부록으로만 두는 방식은 자연스럽지만 독립 skill로 학습하기 어렵다.
- full observability stack을 랩에 넣는 방식은 풍부하지만 범위를 넘는다.
- documentation-first AWS note는 실제 배포 증거는 약하지만 학습 저장소에는 적합하다.

## Chosen direction

- package structure:
  - product domain 없이 ops surface만 중심으로 둔다
- persistence choice:
  - 데이터 모델보다 health/log/metric contract에 집중한다
- security boundary:
  - trace ID와 request visibility를 먼저 강조한다
- integration style:
  - Compose와 CI를 같은 검증 체인으로 둔다
- why this is the right choice:
  - 운영을 “나중에 붙는 것”이 아니라 backend 기본기로 설명하기 좋다

## Rejected ideas

- alerting, tracing, dashboard full stack을 core 범위로 두는 방식은 폐기했다
- AWS live deploy를 필수로 두는 방식은 폐기했다

## Evidence

- `/Users/woopinbell/work/web-pong/study2/labs/G-ops-observability-lab/spring/README.md`
- `/Users/woopinbell/work/web-pong/study2/labs/G-ops-observability-lab/docs/README.md`
- `.github/workflows/study2-spring.yml`

