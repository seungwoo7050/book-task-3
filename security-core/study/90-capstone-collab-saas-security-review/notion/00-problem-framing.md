# 문제 정의

- 앞선 foundations 프로젝트는 각각의 control vocabulary를 분리해 설명했다.
- capstone에서는 이 vocabulary를 한 서비스 review 문서로 다시 묶어야 한다.
- 목표는 기능 구현이 아니라 consolidated remediation workflow를 reproducible하게 남기는 것이다.

## 왜 이 capstone이 필요한가

개별 랩만 보면 "JWT 검증을 왜 해야 하는가", "SSRF를 왜 막아야 하는가", "CVE를 왜 지금 올려야 하는가"는 각각 설명할 수 있습니다.
하지만 실제 운영에서는 이 질문이 한 backlog에 동시에 올라옵니다. 그래서 capstone은 category별 정답을 더 만드는 대신,
서로 다른 판단을 같은 remediation board에 실어도 설명이 무너지지 않는지를 확인해야 합니다.

## 성공 기준

- `review`가 stable JSON shape를 출력한다.
- `demo`가 `.artifacts/capstone/demo/`에 7개 artifact를 생성한다.
- secure baseline bundle은 빈 finding 결과를 유지한다.
- foundations vocabulary와 같은 control ID, priority, action이 다시 나온다.
