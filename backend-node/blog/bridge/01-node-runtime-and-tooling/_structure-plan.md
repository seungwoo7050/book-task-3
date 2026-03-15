# 01-node-runtime-and-tooling Structure Plan

## 한 줄 초점
- 실제 파일과 env를 다루는 첫 Node CLI에서, 구현 계약과 재현 문서가 어디서 맞고 어디서 어긋나는지를 설명한다.

## 독자 질문
- 왜 이 프로젝트를 Node API 소개가 아니라 런타임 입력 계약의 시작점으로 읽어야 하는가?
- line-oriented parser, summary shape, `REPORT_FORMAT`, argv 검증은 각각 어떤 책임을 가지는가?
- 구현은 건강한데 README/스크립트 예제가 깨지는 상황을 어떻게 읽어야 하는가?

## 본문 구성
1. 문제 재정의
   파일과 env를 믿지 않는 CLI라는 관점으로 프로젝트를 다시 잡는다.
2. parser
   stream + `readline`과 line-numbered parse error를 본다.
3. summary
   `5 requests / 3 users / 2 errors` 같은 숫자가 어떻게 만들어지는지 본다.
4. CLI 계약
   `REPORT_FORMAT`와 파일 경로 검증을 본다.
5. 재검증과 불일치
   direct 실행은 통과하지만 `pnpm start -- ...`와 `run-example.sh`는 깨지는 점을 닫는다.

## 반드시 연결할 증거
- `node/src/request-report.ts`
  parser와 summary
- `node/src/cli.ts`
  env/argv 계약
- `node/tests/request-report.test.ts`
  성공/실패 고정
- `problem/script/run-example.sh`
  현재 재현 스크립트 한계

## 서술 원칙
- 기존 blog 문장을 입력으로 삼지 않는다.
- Node API 나열보다 입력을 어떻게 의심하는지가 먼저 보이게 쓴다.
- 구현 성공과 문서 표면 실패를 섞지 않고 분리한다.

## 이번 턴의 결론 문장
- `01-node-runtime-and-tooling`은 작은 로그 CLI를 통해, 실제 런타임 입력을 다루는 코드와 그것을 재현하는 문서가 둘 다 별도 계약이라는 사실을 처음 보여 주는 bridge 프로젝트다.
