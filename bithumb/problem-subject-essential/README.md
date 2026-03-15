# bithumb 서버 개발 필수 문제지

`bithumb`는 클라우드 보안 운영과 AWS provider 문맥이 강한 트랙입니다.
이번 기준에서는 웹 백엔드와 게임 서버를 함께 놓고 봐도 곧바로 공통 필수로 묶을 문제는 따로 두지 않습니다.
이 트랙의 종합 과제는 [`../problem-subject-capstone/README.md`](../problem-subject-capstone/README.md)로 분리합니다.

## 현재 essential이 없는 이유

- AWS 보안 판단과 운영 자동화 자체는 중요하지만, 공통 서버 필수보다 provider-specific 도메인 문맥이 더 강합니다.
- 그래서 이 주제는 "필수 없음"이 아니라 "공통 서버 essential 축으로는 비워 둠"에 가깝습니다.

## 대신 어디서 시작할까

| lab | 한 줄 문제 요약 | 검증 시작점 |
| --- | --- | --- |
| [elective-path-python](elective-path-python.md) | 시작 위치의 구현을 완성해 실제 AWS API나 계정 상태를 조회하지 않습니다와 학습 범위는 statement 단위 match와 우선순위 설명까지로 제한합니다를 한 흐름으로 설명하고 검증한다. | `cd /Users/woopinbell/work/book-task-3/bithumb/00-aws-security-foundations/01-aws-security-primitives/python && PYTHONPATH=src python3 -m pytest` |
| [problem-subject-capstone-readmemd-python](problem-subject-capstone-readmemd-python.md) | 시작 위치의 구현을 완성해 실제 AWS 계정과 연동하지 않습니다와 외부 큐 시스템, 운영용 인증, 멀티테넌시는 다루지 않습니다를 한 흐름으로 설명하고 검증한다. | `cd /Users/woopinbell/work/book-task-3/bithumb/02-capstone/10-cloud-security-control-plane/python && PYTHONPATH=src python3 -m pytest` |

## 스포일러 경계

각 lab의 정답 코드, 공식 구현 진입점, 해설은 같은 이름의 sibling `_answer.md` 문서에서 확인한다.
