# 06 Remediation Pack Runner 읽기 지도

finding을 곧바로 실행하는 대신, 사람이 검토할 수 있는 dry-run 조치안으로 바꾸는 단계다.

이 문서는 본문으로 바로 들어가기 전에 무엇을 붙들고 읽어야 하는지 정리해 두는 입구다. 먼저 질문과 흐름을 잡고 내려가면 phase 사이 점프가 훨씬 덜 갑작스럽다.

## 먼저 붙들 질문
- 왜 remediation의 첫 산출물을 실행 결과가 아닌 plan 문서로 봤는가?
- control별 remediation mode 분리가 왜 중요했는가?
- approval 상태 전이를 별도 함수로 분리한 이유는 무엇인가?

## 이 글은 이렇게 흘러간다
1. 시작점: 문제 정의와 이 프로젝트가 고정하려는 입력/출력 경계
2. Phase 1. remediation 출력 shape부터 고정했다: finding을 받아 사람이 검토할 plan 문서로 바꾸는 최소 구조를 세운다.
3. Phase 2. remediation mode를 control별로 갈랐다: 위험 종류에 따라 조치 전략이 달라진다는 점을 코드로 드러낸다.
4. Phase 3. approval 상태 전이를 별도 함수로 분리했다: plan 생성과 승인 처리를 분리해 추후 orchestration에 연결하기 쉽게 만든다.
5. 마무리: 다음 프로젝트로 이어지는 질문과 남은 한계

## 특히 눈여겨볼 장면
- 실행 대신 제안이라는 목표 전환을 처음에 분명히 잡는다.
- control별 remediation mode 분기와 사람이 읽을 patch/command 초안에 집중한다.
- approval 상태 전이를 마지막에 붙여 capstone worker 연결점을 보여 준다.

## 먼저 열 문서
- [10-development-timeline.md](10-development-timeline.md): finding을 실행이 아닌 조치안으로 바꾸기

## 근거로 삼은 파일
- `README.md`
- `problem/README.md`
- `python/README.md`
- `docs/concepts/dry-run-remediation.md`
- `python/src/remediation_pack_runner/runner.py`
- `python/src/remediation_pack_runner/cli.py`
- `python/tests/test_runner.py`
