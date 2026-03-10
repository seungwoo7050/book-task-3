# Selective Repeat 문제 안내

## 이 문서의 역할

이 문서는 `Selective Repeat`를 시작하기 전에 읽는 현재 저장소 기준 문제 사양입니다. 구현 세부와 공개 구현 경로는 상위 프로젝트 README가 연결하는 경로를 따라가면 됩니다.

## 문제 목표

`rdt-protocol`과 같은 비신뢰 채널 위에 `Selective Repeat`를 구현해, timeout이 난 패킷만 재전송하고 수신 측은 out-of-order 패킷을 버퍼링하도록 만듭니다.

## 구현해야 할 동작

### 송신자 동작

- sender window와 per-packet timer를 유지합니다.
- 개별 ACK를 받으면 해당 패킷만 확인 처리합니다.
- timeout이 난 패킷만 선택적으로 재전송합니다.

### 수신자 동작

- receiver window 안의 패킷은 순서가 어긋나도 버퍼링합니다.
- 빠진 앞선 패킷이 오면 버퍼를 비우며 in-order delivery를 수행합니다.
- 유효한 패킷은 앞선 결손이 있어도 개별 ACK를 보냅니다.

### 공유 계약 유지

- `channel.py`, `packet.py`의 인터페이스는 바꾸지 않습니다.
- 기본 window size는 현재 과제에서 `4`를 기준으로 합니다.

## 제공 자료와 실행 환경

- helper: `code/channel.py`, `code/packet.py`
- starter code: `code/selective_repeat_skeleton.py`
- 테스트 데이터: `data/test_messages.txt`
- 검증 스크립트: `script/test_selective_repeat.sh`

## 제약과 해석 기준

- Python 3 표준 라이브러리만 사용합니다.
- 기존 helper를 그대로 재사용합니다.
- `make test`는 root 권한 없이 로컬 SR 전송 검사를 수행해야 합니다.

## 성공 기준

| 항목 | 내용 |
| :--- | :--- |
| 선택 재전송 | timeout이 난 패킷만 다시 전송합니다. |
| 수신 버퍼링 | out-of-order 패킷을 버퍼링하고 순서대로 전달합니다. |
| ACK 처리 | 개별 ACK로 sender 상태를 정확히 갱신합니다. |
| 공유 helper 재사용 | 기존 packet/channel 계약을 깨지 않습니다. |
| 코드 품질 | GBN과 비교해 읽기 쉬운 구조로 정리합니다. |
