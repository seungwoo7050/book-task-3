# 05 CSPM Rule Engine 읽기 지도

Terraform plan과 운영 snapshot을 함께 읽어 triage 가능한 misconfiguration finding으로 바꾸는 규칙 엔진이다.

이 문서는 본문으로 바로 들어가기 전에 무엇을 붙들고 읽어야 하는지 정리해 두는 입구다. 먼저 질문과 흐름을 잡고 내려가면 phase 사이 점프가 훨씬 덜 갑작스럽다.

## 먼저 붙들 질문
- Terraform plan에서 어떤 resource-level 규칙을 먼저 고정했는가?
- 왜 access key snapshot을 같은 engine 안으로 끌어들였는가?
- secure fixture 0건이 rule 품질에 왜 중요한가?

## 이 글은 이렇게 흘러간다
1. 시작점: 문제 정의와 이 프로젝트가 고정하려는 입력/출력 경계
2. Phase 1. Terraform plan 규칙부터 세웠다: 정적 plan JSON만으로 설명 가능한 misconfiguration을 먼저 잡는다.
3. Phase 2. access key snapshot으로 입력 범위를 넓혔다: CSPM이 선언형 plan만 읽는 정적 분석에 머무르지 않도록 한다.
4. Phase 3. secure fixture 0건을 품질 기준으로 삼았다: 불필요한 finding이 나오지 않는 기준선을 만든다.
5. 마무리: 다음 프로젝트로 이어지는 질문과 남은 한계

## 특히 눈여겨볼 장면
- Terraform plan에서 resource를 꺼내 규칙을 적용하는 기본 loop를 첫 장면으로 둔다.
- snapshot 기반 access key rule을 추가하는 순간 CSPM의 입력 범위가 넓어지는 장면을 강조한다.
- secure fixture 0건과 finding schema가 품질 기준이라는 점으로 마무리한다.

## 먼저 열 문서
- [10-development-timeline.md](10-development-timeline.md): plan과 snapshot에서 triage finding 뽑기

## 근거로 삼은 파일
- `README.md`
- `problem/README.md`
- `python/README.md`
- `docs/concepts/rule-design.md`
- `python/src/cspm_rule_engine/scanner.py`
- `python/src/cspm_rule_engine/cli.py`
- `python/tests/test_scanner.py`
