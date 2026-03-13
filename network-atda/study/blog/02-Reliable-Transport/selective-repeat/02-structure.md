# Selective Repeat structure guide

## 이 글의 중심 질문

- 개별 ACK과 수신 버퍼링이 Go-Back-N 다음 단계에서 어떤 차이를 만드는가?
- 한 줄 답: Go-Back-N`의 한계를 보강하기 위해 추가한 선택 재전송 프로젝트입니다.

## 권장 흐름

1. 실행 표면과 entrypoint를 먼저 고정하기
2. window, 버퍼, timer를 Selective Repeat 규칙으로 묶기
3. 테스트와 남은 범위를 정리하기

## 꼭 살릴 근거

- `problem/Makefile`의 공개 target과 `make -C study/02-Reliable-Transport/selective-repeat/problem test`
- `study/02-Reliable-Transport/selective-repeat/python/src/selective_repeat.py`의 `recv_buffer`
- `study/02-Reliable-Transport/selective-repeat/python/tests/test_selective_repeat.py`의 `def test_selective_repeat_delivers_all_messages_without_loss`

## 리라이트 주의점

- `Selective Repeat`를 개념 강의처럼 풀지 말고, 실제 파일과 CLI 순서로 보여 준다.
- 전체 로그를 덤프하지 말고 판단을 바꾼 줄만 남긴다.
- 마지막에는 실제 병렬 스레드 모델은 아닙니다. 같은 남은 경계를 사람 말로 다시 정리한다.
