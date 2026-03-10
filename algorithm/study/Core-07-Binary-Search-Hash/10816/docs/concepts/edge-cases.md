# 경계 사례 점검 — BOJ 10816 Number Card 2

## 1. 없는 숫자 쿼리
`Counter[x]` → 0 (KeyError 없음).

## 2. 모든 카드가 같은 숫자
`Counter({x: N})`, 해당 숫자 쿼리 → N.

## 3. 음수
`Counter`는 음수 키도 정상 처리.

## 핵심 주의점
- 출력 형식: 공백 구분 (줄바꿈 아님)
- `sys.stdout.write` 또는 `' '.join()`
