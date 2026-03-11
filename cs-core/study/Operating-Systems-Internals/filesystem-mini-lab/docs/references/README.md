# References

## 핵심 참고 자료

- Operating Systems: Three Easy Pieces, File Systems chapter
- Modern Operating Systems, file-system implementation overview
- ext3/ext4 journaling high-level notes

## 왜 이 자료를 참고했는가

- OSTEP은 inode, directory, journaling을 가장 작은 모델로 설명할 때 기준이 된다.
- Modern Operating Systems는 metadata 구조를 breadth 관점으로 다시 연결할 때 도움이 된다.
- ext3/ext4 자료는 prepared/committed recovery 직관을 잡는 데 참고했다.

## 현재 프로젝트에 남긴 흔적

- disk image는 교육용 재현성을 위해 JSON 하나로 단순화했다.
- root-only 제약을 둬서 directory traversal보다 inode/block/journal 관계를 먼저 보이게 했다.
