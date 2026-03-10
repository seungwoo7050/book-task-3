# Commerce Backend V2 — Notion 문서 가이드

## 읽는 순서

| 순서 | 문서 | 핵심 질문 |
|------|------|----------|
| 1 | [00-problem-framing.md](00-problem-framing.md) | v1의 한계를 넘어 면접에서 설명 가능한 커머스 백엔드란 무엇인가? |
| 2 | [01-approach-log.md](01-approach-log.md) | 네 가지 선택지 중 모듈형 모놀리스를 고른 이유는? |
| 3 | [02-debug-log.md](02-debug-log.md) | 스키마-entity 불일치, Jackson 충돌, placeholder 실패에서 무엇을 배웠나? |
| 4 | [03-retrospective.md](03-retrospective.md) | 메모리 데모에서 저장소 기반 흐름으로 가면서 무엇이 좋아지고 무엇이 약해졌나? |
| 5 | [04-knowledge-index.md](04-knowledge-index.md) | refresh token hashing, optimistic locking, idempotency key, outbox pattern, selective Redis란? |
| 6 | [05-timeline.md](05-timeline.md) | Docker Compose 5개 서비스, 12개 테이블 migration, 멀티스테이지 빌드는 어떻게 구성했나? |

## 이 프로젝트의 위치

`commerce-backend-v2`는 7개 랩(A-auth ~ G-ops)과 baseline 캡스톤(commerce-backend)을 모두 거친 뒤, 최종 통합 캡스톤으로 구현한 프로젝트이다. 랩에서 개별적으로 다룬 인증, 페더레이션, 인가, JPA, 이벤트, 캐시/동시성, 운영 개념을 하나의 커머스 도메인에서 저장소 기반 흐름으로 연결한다.

## 핵심 차별점 (v1 대비)

- **인증**: stub → JWT + DB-hashed refresh token + CSRF + mocked OAuth
- **장바구니**: 인메모리 → Redis 기반 CartStore 추상화
- **주문**: 단순 생성 → checkout 트랜잭션 + @Version 낙관적 락 재고 예약
- **결제**: 없음 → idempotency key 기반 mock payment + outbox event
- **알림**: 없음 → outbox → Kafka → notification 테이블 저장
- **테스트**: 기본 → Testcontainers Kafka 통합 테스트 추가

## 빠른 검증

```bash
make test   # 전체 테스트 (Docker 필요)
make lint   # Spotless + Checkstyle
make smoke  # SmokeTest만
```
