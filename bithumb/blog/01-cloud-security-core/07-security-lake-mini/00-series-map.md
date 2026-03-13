# 07 Security Lake Mini 읽기 지도

CloudTrail fixture를 local lake에 적재하고 preset detection query로 alert를 만드는 최소 security lake 실습이다.

이 문서는 본문으로 바로 들어가기 전에 무엇을 붙들고 읽어야 하는지 정리해 두는 입구다. 먼저 질문과 흐름을 잡고 내려가면 phase 사이 점프가 훨씬 덜 갑작스럽다.

## 먼저 붙들 질문
- security lake를 로컬로 축소할 때 무엇을 먼저 고정해야 하는가?
- 왜 SQL query preset이 alert taxonomy 역할을 하는가?
- alert 순서를 테스트로 잠가야 하는 이유는 무엇인가?

## 이 글은 이렇게 흘러간다
1. 시작점: 문제 정의와 이 프로젝트가 고정하려는 입력/출력 경계
2. Phase 1. CloudTrail fixture를 local lake로 적재했다: CloudTrail 이벤트를 DuckDB/Parquet lake 산출물로 바꾼다.
3. Phase 2. SQL query를 alert taxonomy로 썼다: 이벤트 이름 기반의 suspicious activity를 `LAKE-*` control로 매핑한다.
4. Phase 3. CLI와 테스트로 alert 순서를 잠갔다: 로컬에서 같은 입력을 주면 같은 alert 집합이 재현되게 한다.
5. 마무리: 다음 프로젝트로 이어지는 질문과 남은 한계

## 특히 눈여겨볼 장면
- 적재 단계와 detection query를 분리해서 보이되, 한 CLI로 다시 묶이는 흐름을 보여 준다.
- SQL `CASE` 매핑이 왜 alert taxonomy가 되는지 설명한다.
- alert 순서를 테스트로 잠그는 장면을 끝에 둔다.

## 먼저 열 문서
- [10-development-timeline.md](10-development-timeline.md): local lake에서 detection query를 굴리기

## 근거로 삼은 파일
- `README.md`
- `problem/README.md`
- `python/README.md`
- `docs/concepts/lake-thinking.md`
- `python/src/security_lake_mini/lake.py`
- `python/src/security_lake_mini/cli.py`
- `python/tests/test_lake.py`
