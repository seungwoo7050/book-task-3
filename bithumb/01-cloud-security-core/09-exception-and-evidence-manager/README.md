# 09 Exception and Evidence Manager

## 풀려는 문제

보안 운영은 finding을 많이 만드는 것만으로 끝나지 않습니다.
예외가 왜 허용됐는지, 언제 만료되는지, 어떤 증적이 붙었는지, 누가 승인했는지를 설명할 수 있어야 합니다.

## 내가 낸 답

- exception, evidence, audit trail을 별도 레코드로 나누는 메모리 모델을 구현합니다.
- 예외 승인과 만료, 증적 연결 흐름을 상태 변화로 표현합니다.
- append-only 감사 기록을 남겨 변경 이유를 추적 가능하게 만듭니다.
- 캡스톤 DB 모델로 옮기기 쉬운 최소 필드 집합을 먼저 고정합니다.

## 입력과 출력

- 입력: finding 관련 이벤트, 예외 요청 정보, 증적 메타데이터
- 출력: 예외 상태, 연결된 증적, audit event 개수와 기록

## 검증 방법

```bash
make venv
PYTHONPATH=01-cloud-security-core/09-exception-and-evidence-manager/python/src .venv/bin/python -m exception_evidence_manager.cli
PYTHONPATH=01-cloud-security-core/09-exception-and-evidence-manager/python/src .venv/bin/python -m pytest 01-cloud-security-core/09-exception-and-evidence-manager/python/tests
```

## 현재 상태

- `verified`
- 메모리 모델이지만 승인, 만료, 증적 연결, audit 흐름이 테스트로 고정되어 있습니다.
- 10번 캡스톤의 exception/audit DB 모델이 이 구조를 확장합니다.

## 한계와 다음 단계

- 영속 저장은 캡스톤에서 DB로 확장합니다.
- 외부 티켓 시스템, 승인 워크플로 도구와의 연동은 범위 밖입니다.

## 더 깊게 읽을 문서

- [problem/README.md](problem/README.md)
- [python/README.md](python/README.md)
- [docs/README.md](docs/README.md)
- [notion/README.md](notion/README.md)
