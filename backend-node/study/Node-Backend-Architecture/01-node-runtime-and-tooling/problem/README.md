# Problem

## 목표

Node.js 런타임이 제공하는 환경 변수, 파일 시스템, path, stream 기초를
작은 도구 프로그램으로 익힌다.

## 과제

1. NDJSON 로그 파일을 스트림으로 읽어 메모리 전체 적재 없이 처리한다.
2. 상태 코드, 경로별 호출 수, 고유 사용자 수를 요약한다.
3. `REPORT_FORMAT=text|json` 환경 변수에 따라 출력 형식을 바꾼다.
4. 잘못된 인자나 깨진 JSON 줄이 들어와도 어떤 입력에서 실패했는지 드러낸다.

## 제공 자료

- `problem/data/request-log.ndjson`: 샘플 로그 파일
- `problem/code/starter.ts`: 타입과 함수 골격
- `problem/script/run-example.sh`: 예시 실행 명령

## 최소 성공 기준

- CLI가 파일을 읽고 text/json 두 형식으로 출력한다.
- 구현이 `fs`, `path`, `readline`, `process.env`를 모두 사용한다.
- 테스트가 요약 계산과 CLI 동작을 검증한다.
