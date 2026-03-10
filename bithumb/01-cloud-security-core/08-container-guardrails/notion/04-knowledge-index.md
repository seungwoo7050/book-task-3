# 지식 인덱스

## 이번 프로젝트에서 굳혀야 할 개념

- manifest 수준에서도 탐지 가능한 보안 위험이 생각보다 많습니다.
- image metadata와 manifest는 서로 다른 시점의 증거입니다.
- secure fixture 0건 검증은 scanner 신뢰성의 출발점입니다.
- Kubernetes YAML을 읽는 능력과 보안 rule을 연결하는 연습이 중요합니다.

## 로컬 근거 파일

- 개념 요약: [../docs/concepts/container-guardrails.md](../docs/concepts/container-guardrails.md)
- 구현 진입점: [../python/src/container_guardrails/scanner.py](../python/src/container_guardrails/scanner.py)
- CLI 진입점: [../python/src/container_guardrails/cli.py](../python/src/container_guardrails/cli.py)
- 검증 코드: [../python/tests/test_scanner.py](../python/tests/test_scanner.py)
- 입력 fixture: [../problem/data/](../problem/data/)

## 재현 체크포인트

- insecure fixture에서 `K8S-001`~`K8S-005`, `IMG-001`~`IMG-003`이 모두 나오는지 확인합니다.
- secure manifest와 secure image metadata는 빈 리스트를 반환해야 합니다.
- manifest finding과 image finding이 같은 출력 구조를 쓰는지 봅니다.

## 다음 프로젝트로 이어지는 질문

- `10-cloud-security-control-plane`은 같은 scanner를 K8s ingestion API 뒤에서 재사용합니다.
- `05-cspm-rule-engine`과 함께 보면 “설정에서 위험을 찾는다”는 공통 사고방식을 비교할 수 있습니다.

## 참고 자료

- 공식 링크 정리: [../docs/references/README.md](../docs/references/README.md)
- 이전 서술형 기록: [../notion-archive/essay.md](../notion-archive/essay.md)
- 이전 작업 로그: [../notion-archive/dev-timeline.md](../notion-archive/dev-timeline.md)
