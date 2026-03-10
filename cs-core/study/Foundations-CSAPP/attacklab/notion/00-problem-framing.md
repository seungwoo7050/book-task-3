# 00. 문제 정의

## 문제를 어떻게 이해했는가

`attacklab`은 exploit 문자열을 외우는 과제가 아니라,
"어떤 제약에서 어떤 payload 구조가 필요한가"를 이해하는 프로젝트라고 봤다.

그래서 저장소도 공식 target 복원 경계와 companion verifier를 분리했다.

## 저장소 기준 성공 조건

- 공식 self-study target 복원 경로가 유지된다
- code injection과 ROP의 차이가 공개 문서에서 설명된다
- companion verifier가 phase 1~5 구조를 검증한다
- 비공개 target에 재사용 가능한 exploit dump는 남기지 않는다

## 선수 지식

- stack frame과 little-endian 표현
- buffer overflow 기본 구조
- ASLR, W^X, gadget chain
- 인자 전달 레지스터와 반환 흐름

## 이 프로젝트를 하며 얻고 싶은 것

보안 주제도 공개 저장소에 안전하게 남길 수 있다는 감각,
그리고 payload를 "바이트 구조"로 설명하는 습관을 얻는 것이 목표였다.
