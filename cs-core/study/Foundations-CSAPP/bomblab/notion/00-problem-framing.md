# 00. 문제 정의

## 문제를 어떻게 이해했는가

`bomblab`의 본질은 "정답 문자열 찾기"가 아니라 "바이너리에서 의미를 읽는 절차"다.
그래서 이 저장소에서도 공식 bomb를 그대로 복제하기보다,
공식 문제 경계와 공개 가능한 companion mini-bomb을 분리하는 방향을 택했다.

## 저장소 기준 성공 조건

- 공식 self-study bomb 복원 경로가 유지된다
- 공개 문서가 reverse-engineering workflow를 설명한다
- companion mini-bomb이 phase 패턴을 코드와 테스트로 다시 보여 준다
- 비공개 bomb 정답집처럼 보이는 내용은 남기지 않는다

## 선수 지식

- x86-64 호출 규약
- `gdb`, `objdump`, `strings`, `nm`
- 배열, jump table, 재귀, 연결 리스트, 트리 패턴

## 이 프로젝트를 하며 얻고 싶은 것

정답을 한 번 맞히는 능력보다,
낯선 기계어를 구조 단위로 읽는 습관을 얻는 것이 더 중요했다.
