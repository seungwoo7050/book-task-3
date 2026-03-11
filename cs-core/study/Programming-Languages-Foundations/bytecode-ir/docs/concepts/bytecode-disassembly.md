# 바이트코드 디스어셈블리

disassembler는 단순 디버그 출력이 아니라 compiler가 어떤 lowering을 했는지 고정하는 계약입니다.

## 왜 stable text가 필요한가

- golden test로 lowering 결과를 바로 비교할 수 있습니다.
- AST가 같아도 compiler 구현이 바뀌면 instruction sequence가 어떻게 달라졌는지 추적하기 쉽습니다.
- 학습 노트와 README에서 VM 동작을 설명할 때 스크린샷 없이도 재현 가능한 근거가 됩니다.

## 현재 disassembly가 남기는 정보

- function 이름
- arity
- local slot 개수
- capture 이름 목록
- instruction offset
- opcode와 argument
