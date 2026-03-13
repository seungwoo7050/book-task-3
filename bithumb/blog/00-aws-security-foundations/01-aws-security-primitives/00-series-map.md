# 01 AWS Security Primitives 읽기 지도

IAM을 외우는 대신 결과가 어떻게 만들어지는지 설명 가능한 JSON으로 남기는 가장 작은 평가 엔진이다.

이 문서는 본문으로 바로 들어가기 전에 무엇을 붙들고 읽어야 하는지 정리해 두는 입구다. 먼저 질문과 흐름을 잡고 내려가면 phase 사이 점프가 훨씬 덜 갑작스럽다.

## 먼저 붙들 질문
- allow/deny 결과를 블랙박스가 아니라 statement-level evidence로 설명하려면 무엇이 먼저 필요했는가?
- 왜 deny precedence를 테스트로 잠가야 했는가?
- CLI JSON이 이후 IAM analyzer의 입력 감각으로 어떻게 이어졌는가?

## 이 글은 이렇게 흘러간다
1. 시작점: 문제 정의와 이 프로젝트가 고정하려는 입력/출력 경계
2. Phase 1. statement match를 순수 함수로 고정했다: policy JSON과 request JSON을 같은 규칙으로 비교할 수 있는 최소 엔진을 세운다.
3. Phase 2. deny precedence를 Decision에 박았다: 매칭 결과를 모아서 실제 IAM-like 우선순위로 결론 내린다.
4. Phase 3. CLI가 matches[]까지 드러내도록 마감했다: 엔진 내부의 설명을 외부 JSON 인터페이스로 고정한다.
5. 마무리: 다음 프로젝트로 이어지는 질문과 남은 한계

## 특히 눈여겨볼 장면
- statement match와 최종 decision을 분리한 순간을 먼저 보여 준다.
- deny precedence를 로직과 테스트가 함께 고정하는 장면을 중간 축으로 둔다.
- CLI JSON이 이후 analyzer의 설명 계층이 되는 지점으로 닫는다.

## 먼저 열 문서
- [10-development-timeline.md](10-development-timeline.md): statement match에서 explainable decision까지

## 근거로 삼은 파일
- `README.md`
- `problem/README.md`
- `python/README.md`
- `docs/concepts/iam-basics.md`
- `python/src/aws_security_primitives/engine.py`
- `python/src/aws_security_primitives/cli.py`
- `python/tests/test_engine.py`
