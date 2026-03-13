# 10 Cloud Security Control Plane 읽기 지도

앞선 아홉 개 프로젝트의 판단 로직을 scan, ingestion, exception, remediation, report 흐름으로 묶어 내는 통합 capstone이다.

이 문서는 본문으로 바로 들어가기 전에 무엇을 붙들고 읽어야 하는지 정리해 두는 입구다. 먼저 질문과 흐름을 잡고 내려가면 phase 사이 점프가 훨씬 덜 갑작스럽다.

## 먼저 붙들 질문
- 통합 capstone에서 먼저 세워야 할 경계는 API인가, scanner 로직인가?
- 왜 worker 계층을 따로 두고 pending/completed 상태를 만들었는가?
- demo capture와 fallback 경로가 왜 capstone의 신뢰도를 높였는가?

## 이 글은 이렇게 흘러간다
1. 시작점: 문제 정의와 이 프로젝트가 고정하려는 입력/출력 경계
2. Phase 1. API 표면과 상태 저장소 경계를 먼저 세웠다: 여러 보안 입력이 한 서비스 안으로 들어오는 기본 통로를 만든다.
3. Phase 2. worker가 scanner와 저장소를 연결했다: scan 요청과 remediation 요청이 상태 전이를 거쳐 결과를 저장하게 만든다.
4. Phase 3. remediation과 report로 운영 흐름을 닫았다: finding이 예외와 조치안과 보고서까지 이어지는 마지막 경로를 만든다.
5. Phase 4. demo capture와 fallback으로 재현성을 마감했다: 사람이 수동으로 API를 두드리지 않아도 end-to-end 시나리오를 다시 만들 수 있게 한다.
6. 마무리: 다음 프로젝트로 이어지는 질문과 남은 한계

## 특히 눈여겨볼 장면
- API 표면과 session factory를 먼저 보여 주고, 왜 control plane이 얇은 통합 계층인지 설명한다.
- worker가 scan/remediation 요청을 처리하는 구조를 중간 축으로 둔다.
- demo capture와 report 생성을 마지막에 두어 end-to-end 검증이 어떻게 남는지 보여 준다.

## 먼저 열 문서
- [10-development-timeline.md](10-development-timeline.md): 아홉 개의 판단 로직을 control plane으로 묶기

## 근거로 삼은 파일
- `README.md`
- `problem/README.md`
- `python/README.md`
- `docs/concepts/architecture.md`
- `docs/demo-walkthrough.md`
- `python/src/cloud_security_control_plane/app.py`
- `python/src/cloud_security_control_plane/cli.py`
- `python/src/cloud_security_control_plane/db.py`
- `python/src/cloud_security_control_plane/workers.py`
- `python/src/cloud_security_control_plane/scanners.py`
- `python/src/cloud_security_control_plane/reporting.py`
- `python/src/cloud_security_control_plane/demo_capture.py`
- `python/tests/test_api.py`
- `.artifacts/capstone/demo/02-worker-response.json`
- `.artifacts/capstone/demo/08-report.md`
