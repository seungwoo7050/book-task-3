# backend-node 서버 개발 필수 문제지

`backend-node`는 Books API를 중심으로 웹 백엔드 구조를 익히는 트랙이라, 서버 공통 필수 기준으로 남는 항목이 많지 않습니다.
이 폴더에는 웹 백엔드와 게임 서버를 함께 놓고 봐도 운영성 측면에서 직접성이 높은 문제만 남깁니다.
이 트랙의 종합 과제는 [`../problem-subject-capstone/README.md`](../problem-subject-capstone/README.md)로 분리합니다.

| lab | 한 줄 문제 요약 | 검증 시작점 |
| --- | --- | --- |
| [08-production-readiness-nestjs](08-production-readiness-nestjs.md) | 시작 위치의 구현을 완성해 health/live와 health/ready를 분리할 것, config loader와 structured logging을 문서화할 것, 테스트와 Docker/CI 예시를 함께 제공할 것을 한 흐름으로 설명하고 검증한다. | `cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/applied/08-production-readiness/nestjs && npm run test -- --run` |

## 스포일러 경계

각 lab의 정답 코드, 공식 구현 진입점, 해설은 같은 이름의 sibling `_answer.md` 문서에서 확인한다.
