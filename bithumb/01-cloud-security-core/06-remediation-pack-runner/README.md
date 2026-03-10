# 06 Remediation Pack Runner

## 프로젝트 한줄 소개

finding을 즉시 실행이 아닌 검토 가능한 dry-run 조치안으로 바꾸는 프로젝트입니다.

## 왜 배우는가

탐지로 끝나는 보안 도구는 운영에 바로 연결되기 어렵습니다. 이 프로젝트는 어떤 finding은 자동 수정 후보가 되고 어떤 것은 승인과 절차가 필요하다는 점을 코드로 구분하게 만듭니다.

## 현재 구현 범위

- finding 입력을 remediation plan으로 변환합니다.
- dry-run 중심의 제안과 approval 흐름을 구분합니다.
- 실행 가능한 패치가 아니라 검토 가능한 제안 문서를 만듭니다.

## 빠른 시작

아래 명령은 레포 루트 기준입니다.

```bash
make venv
PYTHONPATH=01-cloud-security-core/06-remediation-pack-runner/python/src .venv/bin/python -m remediation_pack_runner.cli 01-cloud-security-core/06-remediation-pack-runner/problem/data/sample_finding.json
```

## 검증 명령

```bash
PYTHONPATH=01-cloud-security-core/06-remediation-pack-runner/python/src .venv/bin/python -m pytest 01-cloud-security-core/06-remediation-pack-runner/python/tests
```

## 먼저 읽을 파일

- [problem/README.md](problem/README.md)
- [docs/README.md](docs/README.md)
- [python/README.md](python/README.md)
- [notion/README.md](notion/README.md)

## 포트폴리오 확장 힌트

자동 수정 여부만 강조하지 말고, 왜 dry-run과 수동 승인 단계를 분리했는지 보여 주는 편이 실무 감각을 더 잘 드러냅니다.

## 알려진 한계

- 실제 apply는 하지 않습니다.
- rollback orchestration이나 외부 승인 시스템 연동은 다루지 않습니다.
