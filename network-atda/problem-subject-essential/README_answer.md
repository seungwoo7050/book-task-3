# network-atda 핵심 답안지

이 문서는 network-atda 핵심 과제를 source-first로 요약한 답안지다. 상세 해설은 각 leaf 답안지에 있지만, 공식 답이 어떤 소스와 테스트로 고정되는지는 여기서 바로 볼 수 있다.

## 기본기

| lab | 해답 요약 | 검증 |
| --- | --- | --- |
| [rdt-protocol](rdt-protocol_answer.md) | 시작 위치의 구현을 완성해 정확한 전달: 모든 데이터가 순서대로 손상 없이 수신됩니다, 손실 처리: loss가 발생하면 재전송으로 복구합니다, 손상 처리: checksum으로 손상된 패킷을 감지합니다를 한 흐름으로 설명하고 검증한다. 핵심은 gbn_send_receive와 main, rdt_send_receive 흐름을 구현하고 테스트를 통과시키는 것이다. | `make -C /Users/woopinbell/work/book-task-3/network-atda/study/02-Reliable-Transport/rdt-protocol/problem test` |
| [web-server](web-server_answer.md) | 시작 위치의 구현을 완성해 정상 200 응답: 요청한 파일이 있을 때 유효한 HTTP/1.1 200 OK 응답을 돌려줍니다, 정상 404 응답: 없는 파일 요청에 404 Not Found 페이지를 반환합니다, 연결 처리: 요청을 처리한 뒤 연결을 적절히 닫고 서버는 계속 살아 있습니다를 한 흐름으로 설명하고 검증한다. 핵심은 get_content_type와 handle_client, main 흐름을 구현하고 테스트를 통과시키는 것이다. | `make -C /Users/woopinbell/work/book-task-3/network-atda/study/01-Application-Protocols-and-Sockets/web-server/problem test` |

## 읽는 방법

각 행은 실제 lab 답안지로 직접 연결된다. 상세 해설은 각 leaf `_answer.md`에서 확인한다.
