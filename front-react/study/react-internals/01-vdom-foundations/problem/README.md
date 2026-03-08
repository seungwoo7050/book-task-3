# Problem Index

프로비넌스: `adapted`

이 디렉터리는 `legacy/virtual-dom/problem`에서 가져온 과제 자산을 새 학습 구조에 맞게 재배치한 곳이다.

## 포함된 자산

- [original/README.md](original/README.md): 레거시 원문 문제 명세
- `code/`: 제공 스켈레톤 TypeScript 파일
- `script/Makefile`: 새 워크스페이스 경로에 맞춘 적응 스크립트
- `data/`: 이 프로젝트는 별도 입력 데이터가 없으므로 빈 디렉터리만 유지

## 문제 범위

이 과제는 아래 다섯 API를 구현 대상으로 둔다.

- `createElement`
- `createTextElement`
- `createDom`
- `updateDom`
- `render`

## 실행 원칙

이 디렉터리는 문제 자산 보존이 목적이다. 실제 검증은 `study/` 워크스페이스에서 수행한다.

```bash
cd study
npm run test:vdom
npm run typecheck:vdom
```

## 제공 파일

- `code/element.ts`
- `code/dom-utils.ts`
- `code/types.ts`
