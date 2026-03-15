# bithumb 서버 개발 필수 답안지

이 트랙에는 `problem-subject-essential` 전용 runtime이 없다. 그래서 이 답안지는 "필수 문제를 어디서부터 실제 코드로 풀기 시작해야 하는가"를 source-only 기준으로 정리한다. 이 저장소에서 필수 해답의 실제 시작점은 AWS 보안 기초 패키지들과 그것을 하나의 제어평면으로 통합한 캡스톤 코드다.

## 대신 어디서 시작할까

| lab | 해답 요약 | 검증 |
| --- | --- | --- |
| [elective-path-python](elective-path-python_answer.md) | 시작 위치의 구현을 완성해 실제 AWS API나 계정 상태를 조회하지 않습니다와 학습 범위는 statement 단위 match와 우선순위 설명까지로 제한합니다를 한 흐름으로 설명하고 검증한다. 핵심은 explain와 _as_list, StatementResult 흐름을 구현하고 테스트를 통과시키는 것이다. | `cd /Users/woopinbell/work/book-task-3/bithumb/00-aws-security-foundations/01-aws-security-primitives/python && PYTHONPATH=src python3 -m pytest` |
| [problem-subject-capstone-readmemd-python](problem-subject-capstone-readmemd-python_answer.md) | 시작 위치의 구현을 완성해 실제 AWS 계정과 연동하지 않습니다와 외부 큐 시스템, 운영용 인증, 멀티테넌시는 다루지 않습니다를 한 흐름으로 설명하고 검증한다. 핵심은 create_app와 _database_url, _lake_dir 흐름을 구현하고 테스트를 통과시키는 것이다. | `cd /Users/woopinbell/work/book-task-3/bithumb/02-capstone/10-cloud-security-control-plane/python && PYTHONPATH=src python3 -m pytest` |

## 읽는 방법

각 행은 실제 lab 답안지로 직접 연결된다. 상세 해설은 각 leaf `_answer.md`에서 확인한다.
