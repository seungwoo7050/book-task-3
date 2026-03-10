# HTTP forwarding에서 놓치기 쉬운 기준선

## 이 프로젝트가 지원하는 범위

이 저장소의 프록시는 full HTTP proxy가 아닙니다.
학습 목표를 분명하게 하기 위해 다음 기준선만 다룹니다.

- absolute-form `GET` 요청
- outbound 쪽은 `HTTP/1.0`
- 필요한 proxy header는 명시적으로 재작성

이 범위를 정확히 제한하는 것이 오히려 과제를 더 잘 설명합니다.

## URI 파싱에서 반드시 뽑아야 하는 것

예시:

```text
GET http://127.0.0.1:18080/cacheable/basic HTTP/1.1
```

여기서 뽑아야 하는 값:

- host
- port, 없으면 `80`
- path, 없으면 `/`

이 셋을 정확히 못 나누면, 뒤 연결 단계에서 오류가 연쇄적으로 생깁니다.

## header 재작성 정책

outbound request에는 항상 다음이 들어갑니다.

- `Host`
- 고정된 CS:APP `User-Agent`
- `Connection: close`
- `Proxy-Connection: close`

클라이언트가 보낸 같은 이름의 header는 그대로 믿지 않고, proxy가 다시 씁니다.

## 왜 이렇게 단순화하는가

이 프로젝트의 목적은 "임의 HTTP 클라이언트를 완벽히 중계하는 것"이 아니라,
"프록시가 어떤 최소 계약을 지켜야 하는가"를 배우는 것입니다.

그래서 connection reuse 같은 문제를 일부러 제외하고,
one request per upstream connection 모델로 고정합니다.

## 에러 처리에서 확인할 것

- malformed request line
- unsupported method
- upstream connection failure

이 세 경우만 제대로 잡아도, 과제 수준에서는 충분히 robust한 편입니다.
