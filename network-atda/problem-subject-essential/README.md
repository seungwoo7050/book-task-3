# network-atda 핵심 문제지

여기서 `essential`은 네트워크와 서버를 함께 읽을 때 가장 먼저 잡아야 하는 바닥 문제라는 뜻입니다. 최소 서버 루프와 신뢰 전송 상태 기계처럼, 이후 모든 과제가 기대는 개념만 남깁니다.

## 기본기

| lab | 한 줄 문제 요약 | 검증 시작점 |
| --- | --- | --- |
| [rdt-protocol](rdt-protocol.md) | 시작 위치의 구현을 완성해 정확한 전달: 모든 데이터가 순서대로 손상 없이 수신됩니다, 손실 처리: loss가 발생하면 재전송으로 복구합니다, 손상 처리: checksum으로 손상된 패킷을 감지합니다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/network-atda/study/02-Reliable-Transport/rdt-protocol/problem test` |
| [web-server](web-server.md) | 시작 위치의 구현을 완성해 정상 200 응답: 요청한 파일이 있을 때 유효한 HTTP/1.1 200 OK 응답을 돌려줍니다, 정상 404 응답: 없는 파일 요청에 404 Not Found 페이지를 반환합니다, 연결 처리: 요청을 처리한 뒤 연결을 적절히 닫고 서버는 계속 살아 있습니다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/network-atda/study/01-Application-Protocols-and-Sockets/web-server/problem test` |

## 스포일러 경계

각 lab의 정답 코드, 공식 구현 진입점, 해설은 같은 이름의 sibling `_answer.md` 문서에서 확인한다.
