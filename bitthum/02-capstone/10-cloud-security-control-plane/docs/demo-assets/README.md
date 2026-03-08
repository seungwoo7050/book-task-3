# Demo Assets

공개 레포에서는 generated artifact를 그대로 추적하지 않는다. 대신 이 디렉터리에 마지막 검증 실행에서
뽑아낸 대표 샘플을 남긴다.

- [findings-snapshot.json](findings-snapshot.json)
- [remediation-snapshot.json](remediation-snapshot.json)
- [report-excerpt.md](report-excerpt.md)

실제 전체 산출물은 아래 명령으로 다시 만들 수 있다.

```bash
cd study2
make demo-capstone
```
