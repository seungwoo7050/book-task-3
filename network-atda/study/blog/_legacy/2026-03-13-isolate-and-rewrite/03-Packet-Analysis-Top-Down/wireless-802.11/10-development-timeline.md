# 802.11 Wireless Packet Analysis 개발 타임라인

## Day 1 — management frame sequence를 먼저 붙잡기

### Session 1

- 목표: data frame보다 먼저 AP 발견과 선택 절차를 읽는다.
- 진행: `beacons`를 먼저 보니 두 개의 SSID가 나온다. `30 Munroe St`, `linksys12`다. 이어서 `probes`를 보니 station은 `30 Munroe St`를 대상으로 probe request를 보내고, 그 AP가 probe response를 돌려준다.
- 이슈: 처음에는 beacon이 이미 AP 정보를 모두 주니까 probe는 부가 자료라고 생각했다. 실제로는 beacon은 "누가 주변에 있는가", probe는 "내가 선택한 SSID에 누가 응답했는가"를 보여 준다. 역할이 다르다.

CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/wireless-802.11/problem beacons
1   00:16:b6:f7:1d:51   30 Munroe St   100
2   00:14:bf:b1:7c:54   linksys12      100
```

```bash
$ make -C study/03-Packet-Analysis-Top-Down/wireless-802.11/problem probes
3   0x04   00:12:f0:1c:3e:82   ff:ff:ff:ff:ff:ff   30 Munroe St
4   0x05   00:16:b6:f7:1d:51   00:12:f0:1c:3e:82   30 Munroe St
```

- 메모: 여기서 비로소 "station이 수동적으로 beacon만 듣는 게 아니라, 원하는 SSID를 향해 직접 물어본다"는 흐름이 잡혔다.

### Session 2

- 목표: 연결 성립 조건을 authentication과 association로 나눠 본다.
- 진행: `auth`와 `assoc`를 보면 request/response가 각각 한 쌍씩 있다. authentication은 Open System이고 status code는 성공이다. association response는 `AID=0x0001`을 준다.
- 이슈: 처음에는 auth와 assoc가 거의 같은 단계처럼 보였다. 하지만 auth는 "들어와도 되나", assoc는 "정식으로 이 BSS에 붙었나"에 더 가깝다. AID가 association response에서만 등장하는 이유도 그래서 이해됐다.

CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/wireless-802.11/problem auth
5   00:12:f0:1c:3e:82   00:16:b6:f7:1d:51   0   
6   00:16:b6:f7:1d:51   00:12:f0:1c:3e:82   0   0x0000
```

```bash
$ make -C study/03-Packet-Analysis-Top-Down/wireless-802.11/problem assoc
7   0x00   00:12:f0:1c:3e:82   00:16:b6:f7:1d:51          
8   0x01   00:16:b6:f7:1d:51   00:12:f0:1c:3e:82   0x0000   0x0001
```

- 메모: frame 8의 AID를 보고 나서야 "연결이 됐다"는 표현에 실제 근거가 생겼다. 그 전까지는 단지 절차가 흘러가는 것처럼만 보였다.

### Session 3

- 목표: 연결 이후 data/ACK가 어떻게 이어지는지 확인하고, synthetic trace의 단순화를 인정한다.
- 진행: `data`와 `ack`를 보니 frame 9는 `To DS=1`, `From DS=0`인 data frame이고, frame 10은 station을 향한 ACK다. capability/privacy bit는 beacon에서 일부 보이지만, real capture에서 기대할 RSN/WPA detail은 거의 없다.
- 이슈: 무선 trace를 보면 보안 세부까지 더 많이 써야 할 것 같은 압박이 생긴다. 하지만 이 trace는 intentionally compact하다. 여기서 중요한 건 연결 절차와 마지막 ACK 관계이지, 존재하지 않는 IE를 상상해 채우는 게 아니다.

CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/wireless-802.11/problem data
9   00:12:f0:1c:3e:82   00:16:b6:f7:1d:51   00:16:b6:f7:1d:51   1   0
```

```bash
$ make -C study/03-Packet-Analysis-Top-Down/wireless-802.11/problem ack
10   00:12:f0:1c:3e:82   0
```

```bash
$ make -C study/03-Packet-Analysis-Top-Down/wireless-802.11/problem test
bash script/verify_answers.sh
802.11 wireless analysis answers look complete.
```

- 정리:
	- beacon과 probe를 분리해서 보니 AP 발견과 선택의 차이가 보였다.
	- auth와 assoc는 비슷해 보여도 역할이 달랐고, AID가 그 경계를 분명히 했다.
	- data/ACK 두 frame은 연결 이후 실제 전송 시작을 보여 주는 마침표였다.
	- synthetic trace의 단순화는 숨길 게 아니라, 이 프로젝트의 해석 한계로 분명히 적어야 했다.
