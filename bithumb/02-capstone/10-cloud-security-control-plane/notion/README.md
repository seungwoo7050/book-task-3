# 10 Cloud Security Control Plane notion 기록

## 이 문서 묶음이 하는 일

이 `notion/`은 앞선 아홉 개 프로젝트의 판단 엔진과 데이터 모델이 하나의 서비스로 통합되는 과정을 현재 코드 기준으로 다시 정리한 기록입니다.
특히 [05-reproduction-guide.md](05-reproduction-guide.md)는 이 저장소에서 가장 강한 end-to-end 재현 문서가 되도록 구성했습니다. 테스트, 데모, Docker/PostgreSQL 경로와 SQLite fallback, 산출물 위치를 모두 한 문서에서 확인할 수 있게 했습니다.

## 이 문서를 읽을 때 잡아야 할 질문

- 왜 API, worker, DB, lake, report를 분리해야 하는가?
- 앞선 01~09 프로젝트의 어떤 로직이 실제로 재사용되는가?
- 학습용 capstone에서 “완전한 재현성”은 무엇을 뜻하는가?

## 추천 읽기 순서

학습자가 가장 빨리 손에 잡히는 재현 경로를 보려면 `05-reproduction-guide.md`를 초반에 읽는 편이 좋습니다.

1. [00-problem-framing.md](00-problem-framing.md): 문제와 경계를 먼저 확인합니다.
2. [05-reproduction-guide.md](05-reproduction-guide.md): 가장 짧은 재현 경로와 기대 결과를 확인합니다.
3. [01-approach-log.md](01-approach-log.md): 현재 구현 방향을 왜 택했는지 읽습니다.
4. [02-debug-log.md](02-debug-log.md): 어디서 자주 막히는지와 어떤 테스트가 근거인지 확인합니다.
5. [03-retrospective.md](03-retrospective.md): 지금 구현이 무엇을 증명했고 무엇을 의도적으로 비워 두었는지 읽습니다.
6. [04-knowledge-index.md](04-knowledge-index.md): 다음 프로젝트로 이어지는 개념과 근거 파일을 모아 봅니다.

## 이 버전의 근거

- 현재 문제 설명: [../problem/README.md](../problem/README.md)
- 현재 구현 안내: [../python/README.md](../python/README.md)
- 앱 진입점: [../python/src/cloud_security_control_plane/app.py](../python/src/cloud_security_control_plane/app.py)
- CLI 진입점: [../python/src/cloud_security_control_plane/cli.py](../python/src/cloud_security_control_plane/cli.py)
- 데모 캡처 스크립트: [../python/src/cloud_security_control_plane/demo_capture.py](../python/src/cloud_security_control_plane/demo_capture.py)
- 통합 검증: [../python/tests/test_api.py](../python/tests/test_api.py)
- 데모 워크스루: [../docs/demo-walkthrough.md](../docs/demo-walkthrough.md)
- 이전 장문 기록: [../notion-archive/essay.md](../notion-archive/essay.md)
