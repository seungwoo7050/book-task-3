# bithumb 서버 캡스톤 답안지

이 문서는 캡스톤 해답을 control plane 소스와 종단 테스트만으로 읽히게 정리한 답안지다. 정답의 핵심은 개별 보안 검사기를 나열하는 것이 아니라, 스캔 요청 생성부터 finding 저장, 예외 승인, remediation dry-run, markdown 보고서 생성까지를 하나의 운영 API로 연결하는 것이다.

| lab | 해답 요약 | 검증 |
| --- | --- | --- |
| [10-cloud-security-control-plane-python](10-cloud-security-control-plane-python_answer.md) | 시작 위치의 구현을 완성해 실제 AWS 계정과 연동하지 않습니다와 외부 큐 시스템, 운영용 인증, 멀티테넌시는 다루지 않습니다를 한 흐름으로 설명하고 검증한다. 핵심은 create_app와 _database_url, _lake_dir 흐름을 구현하고 테스트를 통과시키는 것이다. | `cd /Users/woopinbell/work/book-task-3/bithumb/02-capstone/10-cloud-security-control-plane/python && PYTHONPATH=src python3 -m pytest` |

## 읽는 방법

각 행은 실제 lab 답안지로 직접 연결된다. 상세 해설은 각 leaf `_answer.md`에서 확인한다.
