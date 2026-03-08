
# Project-Set Audit

## 유지한 강점

- 응용, 전송, 네트워크, 링크, 보안으로 이어지는 범위가 넓습니다.
- 대부분 과제는 `problem/Makefile test` 또는 답안 검증 스크립트를 이미 갖고 있습니다.
- Wireshark 랩은 재현 가능한 trace 파일을 함께 보유하고 있습니다.

## 레거시 셋의 약점

- `rdt-protocol`이 Go-Back-N까지만 구현되어 있고, 문서에서 직접 언급한 Selective Repeat 실습이 비어 있습니다.
- `icmp-pinger`와 `routing` 사이를 잇는 구현 과제가 없어, TTL/ICMP 이론이 경로 발견 도구로 이어지지 않습니다.
- 일부 구현 과제는 canonical 검증이 `make test`인데, 공개 테스트 파일은 서버 선기동을 요구해 학습자에게 혼선을 줍니다.
- 패킷 랩은 답안이 존재하지만 공개 인덱스보다 답안 파일이 먼저 보이는 구조였습니다.

## 보강 결정

- `selective-repeat` 추가: GBN의 한계를 코드 수준에서 비교 가능한 다음 단계 프로젝트가 필요합니다.
- `traceroute` 추가: `icmp-pinger`와 `routing` 사이의 bridge project로 TTL/ICMP를 실제 도구 구현에 연결합니다.
- canonical 검증 기준 고정: 구현 과제는 `problem/Makefile test`, 패킷 랩은 `problem/script/verify_answers.sh`를 래핑한 `make test`로 표준화합니다.
- `tactical-arena-server` 추가: 기존 과제만으로는 "프로토콜 조각을 실제 서버 설계로 묶는 능력"을 보여주기 어려워, TCP/UDP, fixed tick, reconnect, persistence, load smoke를 통합하는 capstone을 별도 트랙으로 추가합니다.
