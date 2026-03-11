# 00 문제 프레이밍

## 프로젝트 정의
- 프로젝트: `UDP Pinger`
- 상태: `verified`
- 기준 검증: `make -C study/01-Application-Protocols-and-Sockets/udp-pinger/problem test`
- 문제 배경: 제공된 손실 서버를 대상으로 UDP RTT와 패킷 손실을 체감하는 클라이언트 구현 프로젝트다.

## 이번 범위
- 지정한 서버로 `PING` 메시지를 10번 보내고 응답 RTT를 측정한다.
- 1초 안에 응답이 없으면 손실로 간주한다.
- 최소/최대/평균 RTT와 손실 개수를 요약한다.

## 제약과 전제
- UDP는 연결도, 재전송도 보장하지 않으므로 손실 판단은 애플리케이션 타임아웃에 의존한다.
- 테스트 서버는 일부 요청을 의도적으로 버리고, 응답은 대문자로 바꿔 돌려준다.
- 구현 목표는 측정과 관찰이지 신뢰 전송 프로토콜 구현이 아니다.

## 성공 기준
- 서버가 살아 있을 때 여러 RTT 샘플을 출력한다.
- 손실이 발생해도 프로그램이 중간에 죽지 않고 전체 10회를 마친다.
- `make -C study/01-Application-Protocols-and-Sockets/udp-pinger/problem test`가 통과한다.

## 공개 문서
- [`../README.md`](../README.md)
- [`../problem/README.md`](../problem/README.md)
- [`../python/README.md`](../python/README.md)
- [`../docs/README.md`](../docs/README.md)
- [`../docs/references/README.md`](../docs/references/README.md)

## 이번에 일부러 제외한 것
- ICMP 수준의 실제 `ping` 복제는 목표가 아니다.
- 재전송, 슬라이딩 윈도, 지터 그래프는 이 단계에서 다루지 않는다.
- 서버와 클라이언트 간 시계 동기화는 가정하지 않는다.
