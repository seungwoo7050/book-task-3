# ip-icmp 문제지

## 왜 중요한가

이 문서는 IP and ICMP Packet Analysis를 시작하기 전에 읽는 현재 저장소 기준 문제 사양입니다. 답안을 먼저 보기보다 trace 범위와 질문을 먼저 이해하는 데 초점을 둡니다.

## 목표

시작 위치의 구현을 완성해 정확성: 정확한 packet/frame 번호와 field 값을 사용합니다, 완결성: 모든 질문에 근거를 포함해 답합니다, 이해도: 프로토콜 메커니즘을 이해한 설명을 제시합니다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/03-Packet-Analysis-Top-Down/ip-icmp/problem/data/ip-fragmentation.pcapng`
- `../study/03-Packet-Analysis-Top-Down/ip-icmp/problem/data/ip-traceroute.pcapng`
- `../study/03-Packet-Analysis-Top-Down/ip-icmp/problem/script/verify_answers.sh`
- `../study/03-Packet-Analysis-Top-Down/ip-icmp/problem/Makefile`

## starter code / 입력 계약

- `../study/03-Packet-Analysis-Top-Down/ip-icmp/problem/data/ip-fragmentation.pcapng`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 정확성: 정확한 packet/frame 번호와 field 값을 사용합니다.
- 완결성: 모든 질문에 근거를 포함해 답합니다.
- 이해도: 프로토콜 메커니즘을 이해한 설명을 제시합니다.
- 근거성: Wireshark field와 trace evidence를 직접 인용합니다.

## 제외 범위

- `../study/03-Packet-Analysis-Top-Down/ip-icmp/problem/data/ip-fragmentation.pcapng` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 상위 카탈로그 요약만 보고 세부 산출물 계약을 생략하지 않는다.
- 검증 명령이 통과한다고 해서 입력 계약과 경계 조건까지 자동으로 맞는다고 가정하지 않는다.

## 성공 체크리스트

- `../study/03-Packet-Analysis-Top-Down/ip-icmp/problem/data/ip-fragmentation.pcapng` 등 fixture/trace 기준으로 결과를 대조했다.
- `make -C /Users/woopinbell/work/book-task-3/network-atda/study/03-Packet-Analysis-Top-Down/ip-icmp/problem test`가 통과한다.

## 검증 방법

```bash
make -C /Users/woopinbell/work/book-task-3/network-atda/study/03-Packet-Analysis-Top-Down/ip-icmp/problem test
```

```bash
bash /Users/woopinbell/work/book-task-3/network-atda/study/03-Packet-Analysis-Top-Down/ip-icmp/problem/script/verify_answers.sh
```

- `ip-icmp`의 Makefile이 호출하는 하위 toolchain이 현재 셸에서 동작해야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`ip-icmp_answer.md`](ip-icmp_answer.md)에서 확인한다.
