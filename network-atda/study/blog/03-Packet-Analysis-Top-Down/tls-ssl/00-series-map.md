# TLS Packet Analysis 시리즈 맵

이 lab의 중심 질문은 "TLS trace에서 무엇이 보이고, 무엇이 encryption boundary 뒤로 사라지는가"다. 현재 답안은 `ClientHello`에서 cipher suites와 version field를 읽고, `ServerHello`에서 선택된 suite를 확인하고, 이후 `ChangeCipherSpec + Application Data`부터는 plaintext를 잃는다. 동시에 synthetic trace 특성 때문에 certificate detail과 extension richness도 제한된다.

## 이 lab를 읽는 질문

- handshake 단계에서는 어떤 협상 정보가 평문처럼 드러나는가
- `0x1301`, `0x1302`, `0x0303` 같은 값은 TLS 1.2/1.3 경계를 어떻게 애매하게 만들 수 있는가
- malformed certificate와 encrypted application data 앞에서 분석을 어디서 멈춰야 하는가

## 이번에 사용한 근거

- `problem/README.md`
- `analysis/src/tls-ssl-analysis.md`
- `problem/Makefile`
- `problem/script/verify_answers.sh`
- 2026-03-14 재실행한 `client-hello`, `server-hello`, `app-data`, `records`

## 이번 재실행에서 고정한 사실

- frame `4` ClientHello는 `version 0x0303`, cipher suites `0x1301,0x1302`, empty SNI를 보여 준다.
- frame `5` ServerHello는 selected cipher `0x1301`과 certificate handshake를 함께 담는다.
- frame `6`은 `ChangeCipherSpec` 뒤 `Application Data`를 담고, plaintext는 더 이상 보이지 않는다.
- `records` 출력은 `22`, `20`, `23` record types가 공존함을 보여 준다.
