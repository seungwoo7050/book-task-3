# 13 Distributed Log Core Structure

## 이 글이 답할 질문

- 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- 파일 포맷과 segment lifecycle을 먼저 구현해 분산 복제 이전의 로컬 불변식을 학습하게 했다.
- 어떤 CLI와 어떤 검증 신호가 이 구간을 닫았는가

## 본문 배치

- 도입: `02-distributed-systems/13-distributed-log-core` 안에서 `30-tests-and-bench-evidence.md`가 맡는 구간과 이전 글에서 이어지는 지점을 짧게 고정한다.
- 구현 순서 요약: 7단계: 전체 테스트 및 검증 -> 8단계: go.work 등록
- 세션 본문: `solution/go/log/log_test.go, solution/go/log/segment_test.go` 순서로 구현 흐름을 복원한다.
- 코드 앵커 1: `solution/go/log/log_test.go`
- 코드 앵커 2: `solution/go/log/segment_test.go`
- 코드 설명 초점: 이 테스트나 재현 스크립트는 프로젝트의 공개 표면을 말이 아니라 입력과 결과로 고정한다. 최종 글에서 이 증거를 빼면 구현은 보여도 완료 기준은 흐려진다.
- 개념 설명: segment는 store와 index를 묶은 관리 단위다.
- 마지막 단락: replication layer는 study 본선 범위에서 제외했다.
