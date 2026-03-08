# 01 VDOM Foundations

상태: `verified`

이 프로젝트는 React internals 트랙의 시작점이다. 목표는 Virtual DOM의 최소 핵심을 직접 구현하면서 다음 단계인 reconciliation이 왜 필요한지 체감하는 것이다.

## 왜 주니어 경로에 필요한가

프레임워크를 사용하는 입장만으로는 React의 갱신 모델과 제약을 설명하기 어렵다. 이 단계는 JSX가 어떤 데이터 구조로 바뀌고, 그 구조가 실제 DOM으로 물질화되는지를 가장 작은 단위에서 확인하게 한다.

## Prerequisite

- HTML DOM 기본
- TypeScript 기초
- 함수 호출과 재귀 흐름 이해

## 이 프로젝트에서 답해야 하는 질문

- VNode는 왜 `{ type, props }` 형태로 표현하는가
- 문자열과 숫자 child를 왜 `TEXT_ELEMENT`로 감싸는가
- 실제 DOM 생성과 prop 반영은 어떤 순서로 처리해야 하는가
- 동기 재귀 `render`의 한계는 무엇인가

## 구조

- `problem/`: 레거시 문제 명세, 스켈레톤 코드, 적응된 스크립트
- `ts/`: 현재 실행 가능한 TypeScript 구현과 테스트
- `docs/`: 공개 개념 문서와 provenance 기록
- `notion/`: 로컬 전용 과정 로그와 회고

## 빠른 검증

```bash
cd study
npm install
npm run verify:vdom
```

## 검증 메모

- 검증 일시: 2026-03-07
- 새 워크스페이스 기준 결과: `2`개 테스트 파일, `27`개 테스트 통과
- 타입체크: `npm run typecheck:vdom` 통과

## 제공 자산과 작성 자산

- 제공 자산: `problem/original/README.md`, `problem/code/*`
- 적응 자산: `problem/script/Makefile`
- 작성 자산: `ts/*`, `docs/*`

## 읽기 순서

1. [problem/README.md](problem/README.md)
2. [docs/README.md](docs/README.md)
3. [ts/README.md](ts/README.md)

## 현재 한계

- 전체 트리를 매번 동기적으로 렌더한다.
- 변경 집합을 계산하지 않으므로 최소 DOM 갱신이 없다.
- 상태와 effect, 스케줄러, 이벤트 위임은 아직 없다.

## 다음 단계로 이어지는 질문

동기 전체 렌더의 한계를 해결하려면 "무엇이 바뀌었는지"와 "언제 commit할지"를 분리해서 다뤄야 한다. 그 질문이 `02-render-pipeline`으로 이어진다.
