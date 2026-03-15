# security-core 서버 개발 필수 문제지

`security-core`는 서버 개발자가 구현 전에 판단 기준부터 갖추기 위해 보는 트랙입니다. 여기서는 웹 백엔드와 게임 서버 모두에서 직접 재사용할 가능성이 높은 방어 판단 문제만 남깁니다.

| lab | 한 줄 문제 요약 | 검증 시작점 |
| --- | --- | --- |
| [02-auth-threat-modeling-python](02-auth-threat-modeling-python.md) | 시작 위치의 구현을 완성해 secure baseline scenario는 0 finding이어야 합니다, insecure scenario는 기대한 AUTH-* control ID만 반환해야 합니다, check-scenarios <manifest>가 시나리오별 matched 여부와 finding 목록을 JSON으로 출력해야 합니다를 한 흐름으로 설명하고 검증한다. | `make test-unit && make demo-auth` |
| [03-owasp-backend-mitigations-python](03-owasp-backend-mitigations-python.md) | 시작 위치의 구현을 완성해 secure baseline case는 0 finding이어야 합니다, insecure case는 기대한 OWASP-* control ID만 반환해야 합니다, check-cases <manifest>가 case별 matched 여부와 finding 목록을 JSON으로 출력해야 합니다를 한 흐름으로 설명하고 검증한다. | `make test-unit && make demo-owasp` |
| [04-dependency-vulnerability-workflow-python](04-dependency-vulnerability-workflow-python.md) | 시작 위치의 구현을 완성해 각 advisory가 deterministic priority와 action으로 변환되어야 합니다, 각 item의 score와 reason code가 설명 가능해야 합니다, triage <bundle>가 expected item과 실제 결과를 비교해 summary를 출력해야 합니다를 한 흐름으로 설명하고 검증한다. | `make test-unit && make demo-dependency` |

## 스포일러 경계

각 lab의 정답 코드, 공식 구현 진입점, 해설은 같은 이름의 sibling `_answer.md` 문서에서 확인한다.
