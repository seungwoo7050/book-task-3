# 03 Retrospective

## 이번 설계에서 좋았던 점

- directory tree를 생략해도 allocation과 recovery 핵심은 충분히 보였다.
- crash stage를 테스트 인터페이스로 드러내니 prepared discard와 committed replay가 훨씬 분명해졌다.
- JSON image라서 문서와 테스트가 같은 상태를 쉽게 공유할 수 있었다.

## 아쉬운 점

- 파일 내용을 block 단위로 append하지 않고 whole-write로 단순화했다.
- directory hierarchy가 없어서 path lookup 복잡도는 아직 나오지 않는다.

## 다음 확장 후보

- subdirectory path lookup
- append/write offset 모델
- metadata-only와 data journal 비교
