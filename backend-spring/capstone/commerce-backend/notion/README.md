# commerce-backend — Notion 문서 가이드

이 디렉토리는 커머스 백엔드 baseline 캡스톤의 학습 과정을 기록한 문서들을 담고 있다.

## 문서 구성

| 순서 | 파일 | 내용 |
|------|------|------|
| 0 | [00-problem-framing.md](./00-problem-framing.md) | 왜 통합 캡스톤이 필요하고, baseline의 역할은 무엇인지 |
| 1 | [01-approach-log.md](./01-approach-log.md) | 커머스 도메인 선택, 모듈형 모놀리스 설계, checkout 트랜잭션 |
| 2 | [02-debug-log.md](./02-debug-log.md) | feature surface가 넓으면 완성도가 높아 보이는 문제 |
| 3 | [03-retrospective.md](./03-retrospective.md) | 통합 기준점의 가치, 인증/결제/이벤트의 얕음 |
| 4 | [04-knowledge-index.md](./04-knowledge-index.md) | Baseline Capstone, 모듈형 모놀리스, Checkout, @Version, Upgrade Path |
| 5 | [05-timeline.md](./05-timeline.md) | Docker Compose, Flyway, 테스트 시나리오 등 소스코드에 없는 작업 기록 |

## 읽는 순서

처음이라면 **00 → 01 → 03** 순서로 읽으면 "왜 baseline을 별도로 유지하고, 무엇이 v2에서 개선되는지"를 빠르게 파악할 수 있다.

## 이 캡스톤의 핵심 포인트

- **7개 랩의 개념을 커머스 도메인 하나로 통합**한 baseline
- 상품 → 장바구니 → 주문으로 이어지는 **checkout 트랜잭션**이 핵심 비즈니스 로직
- 인증 stub, 결제 없음, 이벤트 미연결 — **v2에서 개선할 축이 명확**
- **"왜 v2를 만들었는가?"를 설명하기 위한 비교 기준점**

## 관련 문서

- [docs/README.md](../docs/README.md) — 구현 범위, simplification, 모듈형 모놀리스 선택 이유
- [problem/README.md](../problem/README.md) — 캡스톤 출제 의도
- [commerce-backend-v2/](../../commerce-backend-v2/) — 이 baseline을 개선한 portfolio-grade 버전
