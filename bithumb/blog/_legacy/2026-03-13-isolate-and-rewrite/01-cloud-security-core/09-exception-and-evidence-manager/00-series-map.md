# 09 Exception and Evidence Manager - Series Map

이 시리즈는 `notion/` 없이 `README.md`, `problem/README.md`, `python/README.md`, `manager.py`, `cli.py`, `test_manager.py`, 실제 재검증 명령만으로 다시 읽은 학습 로그입니다.

## 이 시리즈가 답하는 질문

- finding suppression을 단순 mute가 아니라 승인, 만료, 증적, audit trail이 있는 관리 대상으로 어떻게 모델링할까
- 작은 메모리 모델이어도 이후 capstone DB 구조에 옮길 수 있는 경계를 어디까지 나눠야 할까

## 실제 구현 표면

- exception은 `scope_type`, `scope_id`, `reason`, `expires_at`, `approved_by`, `status`를 가진 별도 레코드입니다.
- evidence는 finding과 분리된 append-only 목록입니다.
- audit event는 생성, 승인, 증적 추가를 별도 event type으로 남깁니다.

## 대표 검증 엔트리

- `PYTHONPATH=01-cloud-security-core/09-exception-and-evidence-manager/python/src .venv/bin/python -m exception_evidence_manager.cli`
- `PYTHONPATH=01-cloud-security-core/09-exception-and-evidence-manager/python/src .venv/bin/python -m pytest 01-cloud-security-core/09-exception-and-evidence-manager/python/tests`

## 읽는 순서

1. [프로젝트 README](../../../01-cloud-security-core/09-exception-and-evidence-manager/README.md)
2. [문제 정의](../../../01-cloud-security-core/09-exception-and-evidence-manager/problem/README.md)
3. [실행 진입점](../../../01-cloud-security-core/09-exception-and-evidence-manager/python/README.md)
4. [대표 테스트](../../../01-cloud-security-core/09-exception-and-evidence-manager/python/tests/test_manager.py)
5. [핵심 구현](../../../01-cloud-security-core/09-exception-and-evidence-manager/python/src/exception_evidence_manager/manager.py)
6. [개발 타임라인](10-development-timeline.md)

## 근거 파일

- [README.md](../../../01-cloud-security-core/09-exception-and-evidence-manager/README.md)
- [problem/README.md](../../../01-cloud-security-core/09-exception-and-evidence-manager/problem/README.md)
- [python/README.md](../../../01-cloud-security-core/09-exception-and-evidence-manager/python/README.md)
- [manager.py](../../../01-cloud-security-core/09-exception-and-evidence-manager/python/src/exception_evidence_manager/manager.py)
- [cli.py](../../../01-cloud-security-core/09-exception-and-evidence-manager/python/src/exception_evidence_manager/cli.py)
- [test_manager.py](../../../01-cloud-security-core/09-exception-and-evidence-manager/python/tests/test_manager.py)

## Git Anchor

- `2026-03-10 a4b4aae docs: enhance bithumb`
- `2026-03-11 a9c65b3 Track 2에 대한 전반적인 개선 완료 (infobank, bithumb, game-server)`
