# rollbacklab Notes

이 문서 묶음은 rollback을 구현할 때 가장 먼저 보게 되는 세 단어를 짧게 정리한다.

- `prediction`: 미래 frame의 missing input을 어떻게 채우는가
- `snapshot`: 어느 frame으로 되돌아갈 수 있는가
- `resimulation`: correction 이후 현재 frame까지 다시 계산할 수 있는가

이번 프로젝트는 위 세 가지를 headless simulation 안에만 남긴다. transport, room lifecycle, reconnect는 다음 capstone으로 넘긴다.
