# 09 Exception and Evidence Manager

## 프로젝트 한줄 소개

finding, 예외, 증적, 감사 이력을 작은 모델로 연결하는 거버넌스 프로젝트입니다.

## 왜 배우는가

보안 운영은 finding을 많이 만드는 것만으로 끝나지 않습니다. 예외가 언제까지 유효한지, 누가 승인했는지, 어떤 증적이 연결됐는지 설명할 수 있어야 실제 운영 흐름에 가까워집니다.

## 현재 구현 범위

- exception, evidence, audit trail을 모델링합니다.
- 예외 승인과 만료, 증적 연결 흐름을 다룹니다.
- append-only 성격의 감사 기록을 남깁니다.

## 빠른 시작

아래 명령은 레포 루트 기준입니다.

```bash
make venv
PYTHONPATH=01-cloud-security-core/09-exception-and-evidence-manager/python/src .venv/bin/python -m exception_evidence_manager.cli
```

## 검증 명령

```bash
PYTHONPATH=01-cloud-security-core/09-exception-and-evidence-manager/python/src .venv/bin/python -m pytest 01-cloud-security-core/09-exception-and-evidence-manager/python/tests
```

## 먼저 읽을 파일

- [problem/README.md](problem/README.md)
- [docs/README.md](docs/README.md)
- [python/README.md](python/README.md)
- [notion/README.md](notion/README.md)

## 포트폴리오 확장 힌트

예외를 단순 메모로 처리하지 않고, scope·expiry·approver·evidence를 명시적으로 나눴다는 점을 설명하면 거버넌스 감각을 보여 주기 좋습니다.

## 알려진 한계

- 영속화는 캡스톤에서 DB로 넘깁니다.
- 외부 티켓 시스템이나 승인 워크플로 도구와는 연동하지 않습니다.
