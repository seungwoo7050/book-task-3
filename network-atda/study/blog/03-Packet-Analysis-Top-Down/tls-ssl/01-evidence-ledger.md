# TLS Packet Analysis Evidence Ledger

## 이번에 읽은 자료

- 문제 사양: `study/03-Packet-Analysis-Top-Down/tls-ssl/problem/README.md`
- 답안 엔트리: `study/03-Packet-Analysis-Top-Down/tls-ssl/analysis/src/tls-ssl-analysis.md`
- 검증 스크립트: `study/03-Packet-Analysis-Top-Down/tls-ssl/problem/script/verify_answers.sh`
- 실행 표면: `study/03-Packet-Analysis-Top-Down/tls-ssl/problem/Makefile`

## 핵심 근거

- `client-hello` 출력:
  - frame `4`
  - `tls.handshake.version=0x0303`
  - `tls.handshake.ciphersuite=0x1301,0x1302`
  - SNI empty
- `server-hello` 출력:
  - frame `5`
  - `tls.handshake.version=0x0303`
  - selected suite `0x1301`
- `app-data` 출력:
  - frame `6`
  - record length `1,32`
- `records` 출력:
  - one line with `22,22`
  - one line with `22`
  - one line with `20,23`
- `docs/concepts/wireshark-tls.md`는 certificate extraction 예시로 `x509sat.utf8String`, `x509ce.dNSName`를 제안한다.
- 이번 로컬 확인 `tshark -G fields | rg 'x509'`에서는 `x509af.*` 계열은 보였지만 `x509sat.utf8String`는 확인되지 않았다.
- `analysis/src/tls-ssl-analysis.md`:
  - certificate detail is malformed/truncated
  - TLS 1.3-style cipher suite IDs coexist with `0x0303` version field

## 테스트 근거

`make -C network-atda/study/03-Packet-Analysis-Top-Down/tls-ssl/problem test`

결과:

- `PASS: tls-ssl answer file passed content verification`

보조 실행 이슈:

- `make certs`는 현재 `tshark` build에서 `x509sat.utf8String` field를 인식하지 못해 실패했다.
- 즉 answer markdown의 certificate-detail 한계는 trace malformed 문제와 local dissector field availability 문제가 같이 겹친 결과다.

## 이번에 고정한 해석

- 이 lab는 certificate subject를 끝까지 읽는 과제라기보다, handshake visibility가 어디까지 유지되는지 보는 과제다.
- 현재 trace는 TLS 1.3-style suite IDs와 `0x0303` version field가 함께 있어 textbook one-to-one mapping보다 synthetic teaching artifact에 가깝다.
- encryption 이후 application protocol은 context로 짐작할 수는 있어도 plaintext로 직접 읽을 수는 없다.
- certificate detail 공백은 "답을 덜 썼다"가 아니라, trace와 local toolchain이 동시에 주는 가시성 한계다.
