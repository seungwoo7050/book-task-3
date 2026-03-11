# 00 문제 프레이밍

## 프로젝트 정의
- 프로젝트: `Tactical Arena Server`
- 상태: `verified`
- 기준 검증: `make -C study/05-Game-Server-Capstone/tactical-arena-server/problem test`
- 문제 배경: 앞선 9개 프로젝트에서 따로 배운 TCP, UDP, 신뢰 전송, 라우팅 감각을 하나의 실시간 게임 서버 아키텍처로 모아 본 캡스톤 프로젝트다.

## 이번 범위
- TCP 제어 채널과 UDP 실시간 채널을 함께 사용하는 authoritative game server를 구현한다.
- 로그인, 방 생성/참가, 준비, 매치 시작, reconnect, 결과 저장까지 포함한다.
- C++20 + Boost.Asio + SQLite3 기반으로 빌드와 테스트 자동화를 갖춘다.

## 제약과 전제
- 제어 메시지는 텍스트 라인 프로토콜, 실시간 입력/스냅샷은 바이너리 UDP 패킷으로 분리한다.
- 시뮬레이션은 20Hz tick, 10Hz snapshot 기준으로 돌아간다.
- 학습용 서버이므로 이름 기반 로그인과 로컬 실행 중심 검증을 전제로 한다.

## 성공 기준
- CTest 단위 테스트, Python integration test, load smoke test가 모두 통과한다.
- reconnect, forfeit, out-of-order UDP 같은 시나리오를 자동화된 스크립트로 재현할 수 있다.
- `make -C study/05-Game-Server-Capstone/tactical-arena-server/problem test`가 통과한다.

## 공개 문서
- [`../README.md`](../README.md)
- [`../problem/README.md`](../problem/README.md)
- [`../cpp/README.md`](../cpp/README.md)
- [`../docs/README.md`](../docs/README.md)
- [`../docs/references/README.md`](../docs/references/README.md)

## 이번에 일부러 제외한 것
- 실서비스 인증, 보안 하드닝, anti-cheat, 글로벌 배포는 범위 밖이다.
- 클라이언트 렌더링/UI는 서버 학습을 위한 최소 봇과 테스트 스크립트로 대체한다.
