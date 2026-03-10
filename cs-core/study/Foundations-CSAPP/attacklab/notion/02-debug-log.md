# 02. 디버그 기록

## 실제로 다시 확인한 포인트

### 1. little-endian 주소 인코딩

주소를 사람이 읽는 순서 그대로 써 넣으면 payload가 바로 깨진다.
hex byte 배열은 항상 little-endian 순서로 다시 확인해야 했다.

### 2. cookie 문자열 배치

phase 3와 phase 5에서는 "함수를 부른다"보다 "문자열이 안전한 위치에 있는가"가 더 자주 문제였다.
문자열이 shellcode나 gadget 체인과 겹치지 않도록 배치해야 했다.

### 3. gadget 순서와 레지스터 이동

phase 4와 phase 5는 gadget 목록보다 역할 순서를 먼저 적는 편이 낫다.
어떤 값을 어느 레지스터로 옮길지부터 정리해야 체인이 다시 보인다.

### 4. 공개 범위 판단

공개 self-study target 샘플과 비공개 course target 정보를 섞지 않는 것이 중요했다.
문서와 sample data를 쓸 때도 이 경계를 계속 의식했다.
