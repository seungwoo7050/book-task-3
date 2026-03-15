# bithumb 서버 캡스톤 문제지

`bithumb`의 capstone은 앞선 AWS security/core 프로젝트에서 만든 판단 로직을 API, worker, state store, report 흐름으로 다시 묶어 local control plane을 설명하게 만드는 종합 과제입니다.

| lab | 한 줄 문제 요약 | 검증 시작점 |
| --- | --- | --- |
| [10-cloud-security-control-plane-python](10-cloud-security-control-plane-python.md) | 시작 위치의 구현을 완성해 실제 AWS 계정과 연동하지 않습니다와 외부 큐 시스템, 운영용 인증, 멀티테넌시는 다루지 않습니다를 한 흐름으로 설명하고 검증한다. | `cd /Users/woopinbell/work/book-task-3/bithumb/02-capstone/10-cloud-security-control-plane/python && PYTHONPATH=src python3 -m pytest` |

## 스포일러 경계

각 lab의 정답 코드, 공식 구현 진입점, 해설은 같은 이름의 sibling `_answer.md` 문서에서 확인한다.
