# 00-language-and-typescript Structure Plan

## 한 줄 초점
- TypeScript 문법 소개가 아니라, 이후 Node 프로젝트들이 기대할 입력 정규화와 오류 계약의 출발점을 설명한다.

## 독자 질문
- 외부 입력을 언제 `NormalizedBook` 같은 내부 상태로 바꿔야 하는가?
- 배치 비동기 실패를 전체 예외 대신 항목별 결과로 돌려주는 이유는 무엇인가?
- CLI는 왜 출력 함수가 아니라 stderr와 exit code 계약이 되는가?

## 본문 구성
1. 문제 재정의
   bridge 첫 장면이 왜 문법 복습이 아니라 신뢰 경계 세우기인지 설명한다.
2. 정규화 경계
   `normalizeTags`, `toNormalizedBook`, summary fallback을 본다.
3. 비동기 helper
   `fetchInventorySnapshot`의 항목별 실패 흡수를 본다.
4. CLI 계약
   `parseArgs`, `runCli`, stdout/stderr/exit code를 본다.
5. 현재 한계와 검증
   inventory helper가 CLI에 연결되지 않은 점, year 메시지 어긋남, `run-example.sh` 경로 가정을 닫는다.

## 반드시 연결할 증거
- `ts/src/catalog.ts`
  정규화와 inventory helper
- `ts/src/cli.ts`
  플래그 파싱과 exit code
- `ts/tests/catalog.test.ts`
  성공/실패 계약
- `problem/script/run-example.sh`
  현재 재현 스크립트 한계

## 서술 원칙
- 기존 blog 문장을 입력으로 삼지 않는다.
- 타입 문법 자체보다 경계 설계가 바뀌는 순간을 강조한다.
- 작은 구현의 불일치와 스크립트 한계도 숨기지 않는다.

## 이번 턴의 결론 문장
- `00-language-and-typescript`는 언어 입문장이 아니라, 이후 모든 Node 백엔드 프로젝트의 입력 정리 방식과 오류 표면을 미리 연습하는 브리지다.
