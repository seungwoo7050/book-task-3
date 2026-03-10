# 02-domain-fixtures-and-chat-harness 지식 인덱스

## 핵심 개념

- seeded KB 설계
- deterministic replay harness
- expected evidence document 확인 방식

## 참고 경로

## 리플레이 하네스
- 제목: Replay Harness
- 경로: chat-qa-ops/08-capstone-submission/v0-initial-demo/python/backend/src/evaluator/replay_harness.py
- 확인 날짜: 2026-03-07
- 참고 이유: capstone의 재생 경로를 축소 구현할 때 어떤 계약이 핵심인지 확인하기 위해 읽었다.
- 배운 점: fixture 구조가 안정적이어야 regression과 dashboard 수치가 같은 입력을 공유할 수 있다.
- 현재 프로젝트에 준 영향: stage02는 KB와 replay JSON을 별도 파일로 분리했다.
