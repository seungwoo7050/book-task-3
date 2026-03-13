# TLS Packet Analysis 개발 타임라인

## Day 1 — 보이는 handshake와 보이지 않는 내부를 분리하기

### Session 1

- 목표: TLS trace에서 실제로 보이는 message sequence부터 고정한다.
- 진행: `handshake`와 `client-hello`, `server-hello`를 먼저 돌렸다. TCP handshake 세 frame 뒤에 TLS-bearing frame이 세 개 나온다. frame 4는 ClientHello, frame 5는 ServerHello와 Certificate, frame 6은 ChangeCipherSpec와 Application Data다.
- 이슈: 처음에는 TLS라면 더 긴 handshake를 기대했다. 하지만 이 synthetic trace는 아주 짧다. 여기서 없는 message를 상상으로 채우기 시작하면, 실제 capture보다 교과서 일반론이 더 커져 버린다.

CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/tls-ssl/problem handshake
4   192.168.0.2      93.184.216.34   1
5   93.184.216.34    192.168.0.2     2,11
```

```bash
$ make -C study/03-Packet-Analysis-Top-Down/tls-ssl/problem client-hello
4   0x0303   0x1301,0x1302
```

- 메모: 이 단계에서 가장 중요한 건 frame 4, 5, 6이라는 최소 순서였다. TLS를 설명하는 기준점이 이 세 frame으로 줄었다.

### Session 2

- 목표: ClientHello/ServerHello에서 말할 수 있는 것과 certificate에서 말할 수 없는 것을 분리한다.
- 진행: ClientHello는 `0x0303`, cipher suites `0x1301`, `0x1302`, 그리고 extension length 0이라는 점이 보인다. ServerHello는 `0x1301`을 선택한다. 반면 frame 5의 certificate 부분은 malformed로 표시되어 subject, issuer, validity를 끝까지 복구할 수 없다.
- 이슈: certificate 관련 질문은 항상 더 많이 쓰고 싶어진다. 하지만 지금 trace는 딱 여기서 멈춘다. malformed evidence를 무시하고 일반적인 X.509 설명을 길게 붙이는 건, 이 capture를 읽은 결과가 아니다.

CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/tls-ssl/problem server-hello
5   0x0303   0x1301
```

```bash
$ make -C study/03-Packet-Analysis-Top-Down/tls-ssl/problem certs
5   24
```

- 메모: `certs` 출력이 이렇게 짧다는 사실 자체가 중요한 정보였다. certificate blob은 존재하지만, 사람이 원하는 subject/issuer 수준까지는 풀리지 않는다.

### Session 3

- 목표: 암호화 이후에도 packet에서 남는 메타데이터를 정리한다.
- 진행: `records`를 보니 handshake record, ChangeCipherSpec, Application Data가 각각 존재한다. frame 6의 Application Data는 길이 32로 보이지만, 평문 내용은 보이지 않는다. 포트 443, record type, 길이 정도만 남는다.
- 이슈: 처음엔 Wireshark가 HTTP를 보여 줄 수도 있지 않을까 기대했다. 하지만 key log가 없는 상태에서 이 trace가 보여 주는 건 encrypted record의 외형뿐이다.

CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/tls-ssl/problem records
2  22
1  23
1  20
```

```bash
$ make -C study/03-Packet-Analysis-Top-Down/tls-ssl/problem test
bash script/verify_answers.sh
TLS/SSL analysis answers look complete.
```

- 정리:
	- 이 trace에서 확실한 건 frame 4, 5, 6의 짧은 handshake sequence였다.
	- version과 cipher suite는 말할 수 있었지만, certificate detail은 malformed 지점에서 멈춰야 했다.
	- 암호화 이후에도 record type과 length는 남지만, application payload는 보이지 않는다.
