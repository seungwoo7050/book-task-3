# 0x15 String Matching — 문제 프레이밍# 0x15 String Matching — 문제 프레이밍













문자열 검색은 에디터, grep, DNA 서열 분석 등 어디서나 쓰인다. $O(n+m)$ 선형 매칭의 두 가지 접근.## 왜 이 프로젝트인가`KMP` 모드: prefix function `pi[]` 기반 매칭. `RABIN` 모드: rolling hash 기반 매칭. 둘 다 매칭 위치 리스트 출력.## 프로젝트 구조CLRS Ch 32 문자열 매칭. KMP와 Rabin-Karp 두 알고리즘을 하나의 CLI로 비교.## 첫인상
## 첫인상

CLRS Ch 32 문자열 매칭. KMP와 Rabin-Karp 두 알고리즘을 하나의 CLI에서 비교.

## 프로젝트 구조

KMP 모드: prefix function `pi[]` 계산 후 매칭. Rabin-Karp 모드: rolling hash 기반 매칭. 출력은 매칭 위치 리스트.

## 왜 이 프로젝트인가

문자열 검색의 양대 산맥. KMP는 최악 $O(n+m)$ 보장, Rabin-Karp는 해시 기반으로 다중 패턴 확장에 유리.
