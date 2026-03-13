# Traceroute 시리즈 지도

이 프로젝트를 한 줄로: TTL을 단계적으로 올려 보내는 UDP probe와 ICMP reply 안에 박힌 embedded port를 매칭해서 경로를 추적하는 도구를 raw socket부터 직접 구현한 기록.

## 파일 구성

| 파일 | 역할 |
|------|------|
| `problem/code/traceroute_skeleton.py` | 제공된 스켈레톤 |
| `python/src/traceroute.py` | 직접 작성한 구현 |
| `python/tests/test_traceroute.py` | 비권한 합성 경로 테스트 |
| `problem/Makefile` | `test` / `run-solution` 진입점 |

## canonical verification

```bash
# 비권한 단위 테스트
make -C study/04-Network-Diagnostics-and-Routing/traceroute/problem test

# live 경로 추적 (root 권한 필요)
sudo make -C study/04-Network-Diagnostics-and-Routing/traceroute/problem run-solution HOST=8.8.8.8
```

## 이 시리즈에서 따라갈 질문

1. `build_probe_port(ttl, probe_index, probes_per_hop, base_port)`는 어떤 공식으로 port를 결정하며, probe마다 다른 port가 필요한 이유는 무엇인가?
2. ICMP `Time Exceeded` 패킷 안에 들어 있는 embedded IP + embedded UDP header는 어느 offset에서 꺼내는가?
3. `Time Exceeded (11/0)`와 `Port Unreachable (3/3)`을 각각 어떻게 처리하며, 루프 종료 조건은 무엇인가?
4. `FakeRecvSocket` / `FakeSendSocket`은 무엇을 대체하고, 어떤 테스트를 가능하게 하는가?

## 글 파일

- [10-development-timeline.md](10-development-timeline.md)
