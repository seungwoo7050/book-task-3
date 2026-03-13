# 08 Container Guardrails - Series Map

이 시리즈는 `notion/` 없이 `README.md`, `problem/README.md`, `python/README.md`, `scanner.py`, `cli.py`, `test_scanner.py`, 실제 재검증 명령만으로 다시 읽은 학습 로그입니다.

## 이 시리즈가 답하는 질문

- 클러스터 없이 manifest와 image metadata만으로도 어떤 컨테이너 위험을 설명할 수 있을까
- Kubernetes 설정과 이미지 메타데이터를 같은 finding 집합으로 어떻게 묶을까

## 실제 구현 표면

- manifest에서 `hostPath`, `latest` tag, `privileged`, `runAsUser=0`, `ALL` capability를 찾습니다.
- image metadata에서도 `latest`, root 실행, broad capability를 같은 방식으로 읽습니다.
- insecure fixture와 secure fixture를 함께 둬서 static analysis 범위를 분명히 유지합니다.

## 대표 검증 엔트리

- `PYTHONPATH=01-cloud-security-core/08-container-guardrails/python/src .venv/bin/python -m container_guardrails.cli 01-cloud-security-core/08-container-guardrails/problem/data/insecure_k8s.yaml 01-cloud-security-core/08-container-guardrails/problem/data/insecure_image.json`
- `PYTHONPATH=01-cloud-security-core/08-container-guardrails/python/src .venv/bin/python -m pytest 01-cloud-security-core/08-container-guardrails/python/tests`

## 읽는 순서

1. [프로젝트 README](../../../01-cloud-security-core/08-container-guardrails/README.md)
2. [문제 정의](../../../01-cloud-security-core/08-container-guardrails/problem/README.md)
3. [실행 진입점](../../../01-cloud-security-core/08-container-guardrails/python/README.md)
4. [대표 테스트](../../../01-cloud-security-core/08-container-guardrails/python/tests/test_scanner.py)
5. [핵심 구현](../../../01-cloud-security-core/08-container-guardrails/python/src/container_guardrails/scanner.py)
6. [개발 타임라인](10-development-timeline.md)

## 근거 파일

- [README.md](../../../01-cloud-security-core/08-container-guardrails/README.md)
- [problem/README.md](../../../01-cloud-security-core/08-container-guardrails/problem/README.md)
- [python/README.md](../../../01-cloud-security-core/08-container-guardrails/python/README.md)
- [scanner.py](../../../01-cloud-security-core/08-container-guardrails/python/src/container_guardrails/scanner.py)
- [cli.py](../../../01-cloud-security-core/08-container-guardrails/python/src/container_guardrails/cli.py)
- [test_scanner.py](../../../01-cloud-security-core/08-container-guardrails/python/tests/test_scanner.py)

## Git Anchor

- `2026-03-10 a4b4aae docs: enhance bithumb`
- `2026-03-11 a9c65b3 Track 2에 대한 전반적인 개선 완료 (infobank, bithumb, game-server)`
