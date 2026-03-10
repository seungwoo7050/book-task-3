# Selective Repeat 노트

이 디렉터리는 공개 README에서 다 담지 않은 판단 근거와 재현 메모를 보관한다. 이번 개편에서는 `05-development-timeline.md`를 가장 먼저 읽는 문서로 두고, 나머지 노트는 그 실행 흐름을 설명하는 근거 문서로 배치했다.

## 먼저 읽을 문서
- [05-development-timeline.md](05-development-timeline.md): 처음부터 `verified`까지 따라가는 재현 가이드. SR의 버퍼와 per-packet timer를 재현하는 데 가장 중요하다.

## 읽는 순서
- [00-problem-framing.md](00-problem-framing.md): 문제 범위, 제약, 성공 기준
- [01-approach-log.md](01-approach-log.md): 핵심 설계 선택과 버린 선택지
- [02-debug-log.md](02-debug-log.md): 현재 코드와 테스트로 다시 확인 가능한 오류 사례
- [03-retrospective.md](03-retrospective.md): 무엇을 배웠고 무엇이 아직 약한지
- [04-knowledge-index.md](04-knowledge-index.md): 다시 볼 파일, 용어, 확인 명령

## 이 프로젝트에서 특히 남긴 주제
- per-packet timer가 왜 필요한지
- receiver 버퍼와 in-order flush
- GBN 대비 selective retransmission의 차이
- SR을 현재 테스트 기준으로 재현하는 가장 짧은 순서

## 함께 볼 공개 문서
- [`../README.md`](../README.md)
- [`../problem/README.md`](../problem/README.md)
- [`../python/README.md`](../python/README.md)
- [`../docs/README.md`](../docs/README.md)
- [`../docs/references/README.md`](../docs/references/README.md)

## 백업 노트
- 이전 형식의 장문 기록은 [`../notion-archive/`](../notion-archive/)에 보존했다.
- 현재 `notion/`은 재현 가이드와 판단 근거를 나눠 보관한다.
