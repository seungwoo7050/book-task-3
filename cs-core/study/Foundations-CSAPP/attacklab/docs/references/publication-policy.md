# Attack Lab 공개 정책

## 왜 Bomb Lab보다 더 엄격한가

Attack Lab은 보안 실습이고, payload 정보가 외부 타깃 재사용 자료처럼 보일 위험이 더 큽니다.
그래서 공개 저장소에서는 설명 수준과 자산 범위를 더 엄격히 잡아야 합니다.

## 공개 가능한 것

- 문제 계약 요약과 로컬 복원 절차
- gadget farm 경계 설명과 `farm.c`
- companion verifier 구현과 테스트
- 공개 self-study target에 대한 최소한의 검증 기록
- stack layout, code injection, ROP, defense model 설명

## 공개하지 않는 것

- 공식 `ctarget`, `rtarget`, `hex2raw`
- 비공개 course target의 cookie 파일
- 비공개 타깃에 직접 재사용 가능한 raw exploit 문자열
- 제3자 타깃에 대한 운영형 exploit 가이드

## 저장소에서 실제로 택한 방식

- 공식 target은 `problem/official/` 아래 로컬에서만 복원한다
- 공개 트리에는 companion verifier와 설명 문서만 남긴다
- `notion/`도 공개 저장소 안에 있지만, raw exploit dump는 쓰지 않는다
